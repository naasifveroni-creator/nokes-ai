"""Chat message models"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single chat message"""

    role: str = Field(..., description="Message role: user, assistant, system")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Chat endpoint request"""

    message: str = Field(..., description="User message")
    system_prompt: Optional[str] = Field(None, description="Optional system prompt")
    use_memory: bool = Field(default=True, description="Use memory context")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")


class ChatResponse(BaseModel):
    """Chat endpoint response"""

    content: str = Field(..., description="AI response content")
    memory_context: str = Field(default="", description="Memory context used")
    conversation_turn: int = Field(default=0, description="Conversation turn number")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AnalysisRequest(BaseModel):
    """Text analysis request"""

    text: str = Field(..., description="Text to analyze")
    analysis_type: str = Field(default="general", description="Type of analysis")


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = Field(default="healthy")
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
