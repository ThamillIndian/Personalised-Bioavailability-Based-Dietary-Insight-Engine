"""
Chat API Endpoints
AI-powered recipe assistant using Gemini Flash 2.0
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from loguru import logger
import time
import uuid

from app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    ChatHistoryRequest,
    ChatHistoryResponse,
    QuickQuestionsResponse,
    ChatMessage
)
from app.services.gemini_service import gemini_service
from app.services.langchain_service import langchain_service
from app.utils.error_handlers import ExternalAPIError

router = APIRouter(prefix="/chat", tags=["AI Chat Assistant"])

# In-memory chat history storage (in production, use Redis or database)
chat_history: Dict[str, List[ChatMessage]] = {}


@router.post("/query", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    🤖 Chat with AI Recipe Assistant
    
    Get instant help with recipe queries, nutrition questions, and cooking tips.
    The AI assistant is context-aware and can provide personalized responses.
    
    **Features:**
    - Context-aware responses based on current page/recipe
    - Short, crisp answers (max 2-3 sentences)
    - Fallback support when recipes aren't in database
    - Nutrition tracking and dietary advice
    - Cooking tips and ingredient substitutions
    
    **Example Queries:**
    - "How do I make this recipe gluten-free?"
    - "What's the nutrition in chicken breast?"
    - "How long to cook pasta?"
    - "What can I substitute for butter?"
    - "Is this suitable for diabetics?"
    """
    start_time = time.time()
    
    try:
        # Generate or use existing conversation ID
        conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        
        # Get AI response from LangChain (with conversation memory)
        ai_response = await langchain_service.get_chat_response(
            request.message, 
            conversation_id, 
            request.context
        )
        
        # Calculate response time
        response_time = int((time.time() - start_time) * 1000)
        
        # Store messages in history (LangChain handles this internally, but we keep backup)
        if conversation_id not in chat_history:
            chat_history[conversation_id] = []
        
        # Add user message
        chat_history[conversation_id].append(
            ChatMessage(role="user", content=request.message)
        )
        
        # Add AI response
        chat_history[conversation_id].append(
            ChatMessage(role="assistant", content=ai_response)
        )
        
        # Generate context-aware suggestions using LangChain
        suggestions = langchain_service.get_suggestions(conversation_id, request.context)
        
        logger.info(f"✅ Chat response generated in {response_time}ms")
        
        return ChatResponse(
            success=True,
            message=ai_response,
            conversation_id=conversation_id,
            context_used=request.context,
            suggestions=suggestions,
            response_time_ms=response_time
        )
        
    except ExternalAPIError as e:
        logger.error(f"Gemini API error: {e}")
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {e.message}")
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process chat request")


@router.get("/quick-questions", response_model=QuickQuestionsResponse)
async def get_quick_questions(
    page: Optional[str] = Query(None, description="Current page context"),
    recipe_id: Optional[str] = Query(None, description="Current recipe ID"),
    recipe_title: Optional[str] = Query(None, description="Current recipe title")
):
    """
    💡 Get Context-Aware Quick Questions
    
    Returns suggested questions based on the current page/recipe context.
    These questions help users get started with the AI assistant.
    """
    try:
        context = {
            "page": page,
            "recipe_id": recipe_id,
            "recipe_title": recipe_title
        }
        
        # Use LangChain to get intelligent suggestions
        conversation_id = f"temp_{uuid.uuid4().hex[:8]}"
        questions = langchain_service.get_suggestions(conversation_id, context)
        
        return QuickQuestionsResponse(
            success=True,
            questions=questions,
            context=context
        )
        
    except Exception as e:
        logger.error(f"Quick questions error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get quick questions")


@router.get("/history/{conversation_id}", response_model=ChatHistoryResponse)
async def get_chat_history(
    conversation_id: str,
    limit: int = Query(50, ge=1, le=100, description="Number of messages to retrieve")
):
    """
    📚 Get Chat History
    
    Retrieve previous conversation messages for a given conversation ID.
    Useful for maintaining chat context across sessions.
    """
    try:
        # Get history from LangChain service
        langchain_history = langchain_service.get_conversation_history(conversation_id, limit)
        
        # Convert to ChatMessage format
        messages = []
        for msg in langchain_history:
            messages.append(ChatMessage(
                role=msg["role"],
                content=msg["content"],
                timestamp=msg["timestamp"]
            ))
        
        return ChatHistoryResponse(
            success=True,
            conversation_id=conversation_id,
            messages=messages,
            total_messages=len(langchain_history)
        )
        
    except Exception as e:
        logger.error(f"Chat history error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get chat history")


@router.delete("/history/{conversation_id}")
async def clear_chat_history(conversation_id: str):
    """
    🗑️ Clear Chat History
    
    Clear all conversation history for a given conversation ID.
    Useful for starting fresh conversations.
    """
    try:
        # Clear from LangChain service
        langchain_service.clear_conversation(conversation_id)
        
        # Clear from backup storage
        if conversation_id in chat_history:
            del chat_history[conversation_id]
        
        return {
            "success": True,
            "message": f"Conversation history cleared for {conversation_id}",
            "conversation_id": conversation_id
        }
        
    except Exception as e:
        logger.error(f"Clear chat history error: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear chat history")


