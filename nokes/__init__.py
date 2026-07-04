"""Nokes AI - Advanced AI Assistant System"""

__version__ = "0.1.0"
__author__ = "Nokes Team"
__description__ = "Production-ready AI assistant with memory and multi-purpose capabilities"

from nokes.core.engine import NokesEngine
from nokes.models.chat import ChatMessage, ChatResponse

__all__ = ["NokesEngine", "ChatMessage", "ChatResponse"]
