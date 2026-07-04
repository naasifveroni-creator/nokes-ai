"""Memory retrieval system with embeddings"""

from typing import List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cosine_similarity import cosine_similarity
from loguru import logger


class MemoryRetriever:
    """Simple memory system with TF-IDF embeddings"""

    def __init__(self, max_memory: int = 1000):
        self.documents = []
        self.metadata = []
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words="english")
        self.embeddings = None
        self.max_memory = max_memory
        logger.info("Memory retriever initialized")

    async def add_document(self, text: str, metadata: Optional[dict] = None) -> None:
        """Add document to memory

        Args:
            text: Document text
            metadata: Optional metadata dict
        """
        self.documents.append(text)
        self.metadata.append(metadata or {})

        # Keep memory size bounded
        if len(self.documents) > self.max_memory:
            self.documents.pop(0)
            self.metadata.pop(0)

        # Recompute embeddings
        self._compute_embeddings()
        logger.debug(f"Document added. Memory size: {len(self.documents)}")

    async def search(self, query: str, top_k: int = 3) -> List[str]:
        """Search memory for relevant documents

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            List of relevant document texts
        """
        if not self.documents:
            return []

        try:
            query_embedding = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_embedding, self.embeddings)[0]
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            results = [self.documents[i] for i in top_indices if similarities[i] > 0.1]
            logger.debug(f"Memory search returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Memory search error: {e}")
            return []

    def _compute_embeddings(self) -> None:
        """Compute TF-IDF embeddings for all documents"""
        if self.documents:
            self.embeddings = self.vectorizer.fit_transform(self.documents)
        else:
            self.embeddings = None

    def clear(self) -> None:
        """Clear all memory"""
        self.documents.clear()
        self.metadata.clear()
        self.embeddings = None
        logger.info("Memory cleared")

    def get_stats(self) -> dict:
        """Get memory statistics"""
        return {
            "document_count": len(self.documents),
            "max_capacity": self.max_memory,
            "usage_percent": (len(self.documents) / self.max_memory) * 100,
        }
