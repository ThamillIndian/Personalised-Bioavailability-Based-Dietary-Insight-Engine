"""
Chat-related request/response schemas for AI chatbot
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Individual chat message"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Request for AI chat assistance"""
    message: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="User's question or message",
        example="How do I make this recipe gluten-free?"
    )
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Current page/recipe context for better responses",
        example={
            "page": "recipe_detail",
            "recipe_id": "recipe-123",
            "recipe_title": "Chicken Tikka Masala",
            "current_ingredients": ["chicken", "tomato", "onion"]
        }
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Conversation ID for maintaining chat history",
        example="conv_123456"
    )


class ChatResponse(BaseModel):
    """Response from AI chat assistant"""
    success: bool = True
    message: str = Field(..., description="AI assistant's response")
    conversation_id: str = Field(..., description="Conversation ID for tracking")
    context_used: Optional[Dict[str, Any]] = Field(
        None,
        description="Context information used in the response"
    )
    suggestions: Optional[List[str]] = Field(
        None,
        description="Suggested follow-up questions",
        example=[
            "How to make this spicier?",
            "What sides go well with this?",
            "Can I substitute any ingredients?"
        ]
    )
    response_time_ms: Optional[int] = Field(
        None,
        description="Response time in milliseconds"
    )


class ChatHistoryRequest(BaseModel):
    """Request to get chat history"""
    conversation_id: str = Field(..., description="Conversation ID")
    limit: int = Field(50, ge=1, le=100, description="Number of messages to retrieve")


class ChatHistoryResponse(BaseModel):
    """Response with chat history"""
    success: bool = True
    conversation_id: str
    messages: List[ChatMessage]
    total_messages: int


class QuickQuestionsResponse(BaseModel):
    """Response with context-aware quick questions"""
    success: bool = True
    questions: List[str] = Field(
        ...,
        description="Quick questions based on current context",
        example=[
            "How to make this spicier?",
            "What can I substitute for this ingredient?",
            "How many calories in this recipe?",
            "Is this suitable for my diet?"
        ]
    )
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Context used to generate questions"
    )
