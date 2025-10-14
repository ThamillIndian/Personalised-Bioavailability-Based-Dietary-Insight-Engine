"""
LangChain Service for AI Chat with Conversation Memory
Enhanced chatbot with conversation history and context awareness
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from loguru import logger

try:
    from langchain.memory import ConversationBufferMemory
    from langchain.schema import HumanMessage, AIMessage, BaseMessage
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.runnables.history import RunnableWithMessageHistory
    from langchain_core.chat_history import BaseChatMessageHistory
    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain not available, falling back to basic chat")
    LANGCHAIN_AVAILABLE = False

from app.config import settings
from app.utils.error_handlers import ExternalAPIError


class ConversationMemory:
    """In-memory conversation storage with LangChain integration"""
    
    def __init__(self):
        self.conversations: Dict[str, ConversationBufferMemory] = {}
    
    def get_conversation(self, conversation_id: str) -> ConversationBufferMemory:
        """Get or create conversation memory for a conversation ID"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = ConversationBufferMemory(
                return_messages=True,
                memory_key="chat_history",
                output_key="output",
                # Limit memory for speed:
                max_token_limit=500,  # Reduce from unlimited
                k=3  # Keep only last 3 exchanges
            )
        return self.conversations[conversation_id]
    
    def add_message(self, conversation_id: str, role: str, content: str):
        """Add a message to conversation history"""
        memory = self.get_conversation(conversation_id)
        
        if role == "user":
            memory.chat_memory.add_user_message(content)
        elif role == "assistant":
            memory.chat_memory.add_ai_message(content)
    
    def get_history(self, conversation_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get conversation history as list of messages"""
        if conversation_id not in self.conversations:
            return []
        
        memory = self.conversations[conversation_id]
        messages = memory.chat_memory.messages
        
        # Convert to dict format and limit
        history = []
        for msg in messages[-limit:]:
            if isinstance(msg, HumanMessage):
                history.append({
                    "role": "user",
                    "content": msg.content,
                    "timestamp": datetime.utcnow().isoformat()
                })
            elif isinstance(msg, AIMessage):
                history.append({
                    "role": "assistant",
                    "content": msg.content,
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        return history
    
    def clear_conversation(self, conversation_id: str):
        """Clear conversation history"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]


class LangChainChatService:
    """Enhanced chat service with LangChain conversation memory"""
    
    def __init__(self):
        self.memory = ConversationMemory()
        self.llm = None
        self.chain = None
        self._initialize_llm()
        self._create_chain()
    
    def _initialize_llm(self):
        """Initialize Google Generative AI with LangChain"""
        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not available, using fallback mode")
            return
            
        try:
            if not settings.GEMINI_API_KEY:
                logger.warning("GEMINI_API_KEY not found, chat service will be limited")
                return
            
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",  # Keep Flash 2.0 as requested
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.2,  # Lower = faster, more focused responses
                max_output_tokens=150,  # Reduce from 500 to 150 for speed
                convert_system_message_to_human=True,
                # Add request options for speed
                request_options={
                    "timeout": None,  # No timeout as requested
                    "max_retries": 1,  # Reduce retries for speed
                }
            )
            
            logger.info("✅ LangChain Google Generative AI initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize LangChain LLM: {e}")
            self.llm = None
    
    def _create_chain(self):
        """Create LangChain conversation chain with memory"""
        if not LANGCHAIN_AVAILABLE or not self.llm:
            return
        
        try:
            # Simplified prompt for speed:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful recipe assistant. Answer briefly and practically."),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ])
            
            # Create chain with memory
            self.chain = prompt | self.llm
            
            logger.info("✅ Optimized LangChain conversation chain created")
            
        except Exception as e:
            logger.error(f"❌ Failed to create LangChain chain: {e}")
            self.chain = None
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for the AI assistant"""
        return """
You are a recipe assistant. Give short, helpful answers (max 100 words).

Answer cooking questions, suggest substitutions, give tips.
Be friendly and practical. Keep responses concise.
"""
    
    async def get_chat_response(
        self, 
        user_message: str, 
        conversation_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get AI response with conversation memory
        
        Args:
            user_message: User's question or message
            conversation_id: Conversation ID for memory
            context: Optional context (page, recipe, etc.)
            
        Returns:
            AI assistant's response
            
        Raises:
            ExternalAPIError: If LangChain or Gemini fails
        """
        if not LANGCHAIN_AVAILABLE or not self.chain:
            # Fallback to basic Gemini service
            logger.info("Using fallback Gemini service")
            from app.services.gemini_service import gemini_service
            prompt = self._build_fallback_prompt(user_message, context)
            return await gemini_service.get_chat_response(prompt, conversation_id)
        
        try:
            memory = self.memory.get_conversation(conversation_id)
            
            # Simplified input - no complex context building
            input_text = user_message
            if context and context.get("recipe_title"):
                input_text = f"Recipe: {context['recipe_title']} | Question: {user_message}"
            
            # Get response with minimal processing
            response = await self.chain.ainvoke({
                "input": input_text,
                "chat_history": memory.chat_memory.messages[-2:]  # Only last exchange
            })
            
            response_text = response.content.strip()
            
            # Quick truncation
            if len(response_text) > 200:
                response_text = response_text[:197] + "..."
            
            # Store in memory
            self.memory.add_message(conversation_id, "user", user_message)
            self.memory.add_message(conversation_id, "assistant", response_text)
            
            logger.info(f"✅ Optimized LangChain response generated for conversation {conversation_id}")
            return response_text
            
        except Exception as e:
            logger.error(f"❌ LangChain chat failed: {e}")
            # Fast fallback
            from app.services.gemini_service import gemini_service
            return await gemini_service.get_chat_response(user_message, conversation_id)
    
    def _build_context_info(self, context: Dict[str, Any]) -> str:
        """Build context information string"""
        if not context:
            return ""
        
        parts = []
        if context.get("recipe_title"):
            parts.append(f"Recipe: {context['recipe_title']}")
        if context.get("current_ingredients"):
            ingredients = ", ".join(context["current_ingredients"][:3])  # Limit to 3
            parts.append(f"Have: {ingredients}")
        
        return " | ".join(parts)  # Shorter format
    
    def _build_fallback_prompt(self, user_message: str, context: Optional[Dict[str, Any]]) -> str:
        """Build fallback prompt for basic Gemini service"""
        # Simplified prompt for speed
        prompt = "Recipe assistant: Answer briefly and practically.\n\n"
        
        if context and context.get("recipe_title"):
            prompt += f"Recipe: {context['recipe_title']}\n"
        
        prompt += f"Question: {user_message}\n\nAnswer:"
        
        return prompt
    
    def get_conversation_history(self, conversation_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.memory.get_history(conversation_id, limit)
    
    def clear_conversation(self, conversation_id: str):
        """Clear conversation history"""
        self.memory.clear_conversation(conversation_id)
    
    def get_suggestions(self, conversation_id: str, context: Optional[Dict[str, Any]] = None) -> List[str]:
        """Get context-aware suggestions based on conversation history"""
        history = self.memory.get_history(conversation_id, 10)
        
        # Analyze recent conversation topics
        recent_topics = self._analyze_conversation_topics(history)
        
        # Generate suggestions based on topics and context
        suggestions = []
        
        if "calories" in recent_topics or "nutrition" in recent_topics:
            suggestions.extend([
                "How to reduce calories in this recipe?",
                "What's the protein content?",
                "How to make this more nutritious?"
            ])
        
        if "substitution" in recent_topics or "ingredient" in recent_topics:
            suggestions.extend([
                "What other ingredients can I use?",
                "How to make this without dairy?",
                "What's a good vegetarian alternative?"
            ])
        
        if "cooking" in recent_topics or "technique" in recent_topics:
            suggestions.extend([
                "How to improve my cooking technique?",
                "What's the best way to cook this?",
                "How to make this faster?"
            ])
        
        # Add context-specific suggestions
        if context:
            if context.get("page") == "recipe_detail":
                suggestions.extend([
                    "How to make this spicier?",
                    "What sides go well with this?",
                    "How to meal prep this?"
                ])
        
        # Default suggestions if none specific
        if not suggestions:
            suggestions = [
                "What's a good beginner recipe?",
                "How to meal prep efficiently?",
                "What ingredients should I always have?",
                "How to reduce cooking time?"
            ]
        
        return suggestions[:4]  # Return max 4 suggestions
    
    def _analyze_conversation_topics(self, history: List[Dict[str, Any]]) -> List[str]:
        """Analyze conversation history to identify topics"""
        topics = []
        
        for message in history[-5:]:  # Analyze last 5 messages
            content = message.get("content", "").lower()
            
            if any(word in content for word in ["calorie", "nutrition", "healthy", "diet"]):
                topics.append("nutrition")
            
            if any(word in content for word in ["substitute", "replace", "instead", "alternative"]):
                topics.append("substitution")
            
            if any(word in content for word in ["cook", "bake", "fry", "boil", "technique"]):
                topics.append("cooking")
            
            if any(word in content for word in ["gluten", "dairy", "vegan", "vegetarian"]):
                topics.append("dietary")
        
        return list(set(topics))  # Remove duplicates


# Global instance
langchain_service = LangChainChatService()
