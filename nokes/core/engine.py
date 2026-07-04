"""Main Nokes AI engine"""

import json
from typing import Optional
from loguru import logger
from nokes.core.llm_provider import LLMProvider, get_llm_provider
from nokes.memory.retriever import MemoryRetriever
from nokes.models.chat import ChatMessage, ChatResponse


class NokesEngine:
    """Main AI engine orchestrating LLM and memory"""

    def __init__(
        self,
        llm_provider: str = "openai",
        model: Optional[str] = None,
        enable_memory: bool = True,
    ):
        """Initialize Nokes engine

        Args:
            llm_provider: LLM provider (openai, anthropic)
            model: Specific model to use
            enable_memory: Whether to enable memory system
        """
        self.llm = get_llm_provider(llm_provider, model)
        self.memory = MemoryRetriever() if enable_memory else None
        self.conversation_history = []
        logger.info(f"Nokes Engine initialized with {llm_provider}")

    async def chat(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        use_memory: bool = True,
    ) -> ChatResponse:
        """Process user message and generate response

        Args:
            message: User message
            system_prompt: Optional system prompt override
            use_memory: Whether to use memory context

        Returns:
            ChatResponse with AI response and metadata
        """
        logger.info(f"Processing message: {message[:100]}...")

        # Retrieve relevant memory context
        memory_context = ""
        if self.memory and use_memory:
            relevant_docs = await self.memory.search(message, top_k=3)
            memory_context = "\n".join([doc for doc in relevant_docs]) if relevant_docs else ""
            logger.debug(f"Retrieved {len(relevant_docs)} memory documents")

        # Build conversation context
        messages = self._build_messages(message, memory_context, system_prompt)

        # Generate response
        response_text = await self.llm.generate(
            messages=messages,
            max_tokens=2000,
        )

        # Store in history and memory
        chat_msg = ChatMessage(role="user", content=message)
        self.conversation_history.append(chat_msg)

        if self.memory:
            await self.memory.add_document(message, metadata={"type": "user_message"})
            await self.memory.add_document(
                response_text, metadata={"type": "ai_response"}
            )

        response = ChatResponse(
            content=response_text,
            memory_context=memory_context if use_memory else "",
            conversation_turn=len(self.conversation_history),
        )

        logger.info(f"Generated response: {response_text[:100]}...")
        return response

    def _build_messages(self, user_message: str, memory_context: str, system_prompt: Optional[str]) -> list:
        """Build message list for LLM"""
        system = system_prompt or self._get_default_system_prompt()
        if memory_context:
            system += f"\n\nRelevant Context:\n{memory_context}"

        messages = [{"role": "system", "content": system}]

        # Add recent conversation history
        for msg in self.conversation_history[-10:]:
            messages.append({"role": msg.role, "content": msg.content})

        # Add current message
        messages.append({"role": "user", "content": user_message})

        return messages

    def _get_default_system_prompt(self) -> str:
        """Get default system prompt"""
        return """You are Nokes, an advanced AI assistant created to be helpful, harmless, and honest.

Your capabilities include:
- Natural conversation and dialogue
- Answering questions accurately
- Helping with analysis and problem-solving
- Providing detailed explanations
- Writing and creative tasks

Always be respectful, accurate, and clear in your responses."""

    async def analyze_text(self, text: str, analysis_type: str = "general") -> dict:
        """Analyze text content

        Args:
            text: Text to analyze
            analysis_type: Type of analysis (general, sentiment, entities, etc.)

        Returns:
            Analysis results
        """
        logger.info(f"Analyzing text with type: {analysis_type}")

        prompt = self._get_analysis_prompt(text, analysis_type)
        messages = [{"role": "system", "content": "You are an expert text analyst. Return results as JSON."}, {"role": "user", "content": prompt}]

        response = await self.llm.generate(messages=messages, max_tokens=1000)

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = {"raw_analysis": response}

        logger.info(f"Analysis complete: {result}")
        return result

    def _get_analysis_prompt(self, text: str, analysis_type: str) -> str:
        """Get analysis prompt based on type"""
        prompts = {
            "sentiment": f"Analyze the sentiment of this text and return JSON with keys 'sentiment' (positive/negative/neutral), 'score' (0-1), and 'explanation':\n\n{text}",
            "entities": f"Extract named entities from this text and return JSON with arrays of 'persons', 'organizations', 'locations', 'other':\n\n{text}",
            "summary": f"Summarize this text in 2-3 sentences and return JSON with key 'summary':\n\n{text}",
            "general": f"Provide a comprehensive analysis of this text and return JSON with relevant insights:\n\n{text}",
        }
        return prompts.get(analysis_type, prompts["general"])

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        logger.info("Conversation history cleared")
