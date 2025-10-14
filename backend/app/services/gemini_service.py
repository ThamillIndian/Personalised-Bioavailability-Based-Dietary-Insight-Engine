"""
Gemini AI Service
Handles image recognition, substitutions, and AI-powered suggestions using Google Gemini
"""

import google.generativeai as genai
from typing import List, Dict, Optional
from PIL import Image
import io
import json
from loguru import logger

from app.config import settings
from app.schemas.ingredient_schema import RecognizedIngredient, SubstitutionOption
from app.utils.error_handlers import IngredientRecognitionError, ExternalAPIError


class GeminiService:
    """Service for Gemini AI operations"""
    
    def __init__(self):
        """Initialize Gemini service"""
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your-gemini-api-key":
            logger.warning("⚠️ Gemini API key not configured")
            self.model = None
            return
        
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
            logger.info(f"✅ Gemini service initialized with model: {settings.GEMINI_MODEL}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {e}")
            self.model = None
    
    async def recognize_ingredients_from_image(self, image_bytes: bytes) -> List[RecognizedIngredient]:
        """
        Recognize ingredients from uploaded image using Gemini Vision
        
        Args:
            image_bytes: Image file bytes
            
        Returns:
            List of recognized ingredients with confidence scores
            
        Raises:
            IngredientRecognitionError: If recognition fails
        """
        if not self.model:
            raise IngredientRecognitionError(
                "Gemini service not available. Please configure GEMINI_API_KEY."
            )
        
        try:
            # Open and validate image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert RGBA to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Craft detailed prompt for ingredient recognition
            prompt = """
You are a professional chef analyzing ingredients in an image.

Carefully examine this image and identify ALL visible food ingredients.

Return ONLY a valid JSON array (no markdown, no code blocks) in this exact format:
[
  {
    "name": "ingredient name in lowercase",
    "confidence": 0.95,
    "quantity_estimate": "approximate amount if visible",
    "category": "vegetable/protein/grain/dairy/spice/other"
  }
]

Rules:
- Only include actual food ingredients (no utensils, containers, or background items)
- Use common ingredient names (e.g., "tomato" not "roma tomato")
- Confidence should be between 0.0 and 1.0
- If quantity is not visible, use null
- Categories: vegetable, fruit, protein, grain, dairy, spice, oil, other

Return ONLY the JSON array, nothing else.
"""
            
            # Generate content
            response = self.model.generate_content([prompt, image])
            
            # Parse response
            ingredients = self._parse_ingredient_response(response.text)
            
            logger.info(f"✅ Recognized {len(ingredients)} ingredients from image")
            return ingredients
            
        except Exception as e:
            logger.error(f"❌ Ingredient recognition failed: {e}")
            raise IngredientRecognitionError(
                f"Failed to recognize ingredients: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def _parse_ingredient_response(self, response_text: str) -> List[RecognizedIngredient]:
        """Parse Gemini response into structured ingredients"""
        try:
            # Clean response - remove markdown code blocks if present
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            
            cleaned_text = cleaned_text.strip()
            
            # Parse JSON
            data = json.loads(cleaned_text)
            
            # Convert to RecognizedIngredient objects
            ingredients = []
            for item in data:
                try:
                    ingredient = RecognizedIngredient(
                        name=item.get("name", "").lower().strip(),
                        confidence=float(item.get("confidence", 0.8)),
                        quantity_estimate=item.get("quantity_estimate"),
                        category=item.get("category")
                    )
                    if ingredient.name:  # Only add if name is not empty
                        ingredients.append(ingredient)
                except Exception as e:
                    logger.warning(f"Skipping invalid ingredient: {item}, error: {e}")
                    continue
            
            return ingredients
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini JSON response: {e}")
            logger.debug(f"Raw response: {response_text}")
            
            # Fallback: try to extract ingredients from natural language
            return self._fallback_ingredient_extraction(response_text)
    
    def _fallback_ingredient_extraction(self, text: str) -> List[RecognizedIngredient]:
        """Fallback extraction if JSON parsing fails"""
        # Simple extraction - look for common ingredient words
        common_ingredients = [
            "tomato", "onion", "garlic", "chicken", "beef", "pork", "rice",
            "pasta", "potato", "carrot", "celery", "bell pepper", "cheese",
            "milk", "egg", "flour", "sugar", "salt", "pepper", "oil"
        ]
        
        found_ingredients = []
        text_lower = text.lower()
        
        for ingredient in common_ingredients:
            if ingredient in text_lower:
                found_ingredients.append(
                    RecognizedIngredient(
                        name=ingredient,
                        confidence=0.7,
                        quantity_estimate=None,
                        category="other"
                    )
                )
        
        return found_ingredients
    
    async def get_ingredient_substitutions(
        self,
        ingredient: str,
        context: Optional[str] = None
    ) -> List[SubstitutionOption]:
        """
        Get substitution suggestions for an ingredient
        
        Args:
            ingredient: Ingredient to substitute
            context: Cooking context (e.g., "baking", "vegan", "allergy")
            
        Returns:
            List of substitution options
            
        Raises:
            ExternalAPIError: If Gemini API fails
        """
        if not self.model:
            raise ExternalAPIError(
                "Gemini",
                "Service not available. Please configure GEMINI_API_KEY."
            )
        
        try:
            context_str = f" for {context}" if context else ""
            
            prompt = f"""
Suggest substitutes for "{ingredient}"{context_str}.

Return ONLY a valid JSON array (no markdown) in this format:
[
  {{
    "substitute": "ingredient name",
    "ratio": "substitution ratio (e.g., '1:1', '1/2 cup per cup')",
    "notes": "any important notes about the substitution"
  }}
]

Provide 3-5 practical substitutions. Return ONLY the JSON array.
"""
            
            response = self.model.generate_content(prompt)
            substitutions = self._parse_substitution_response(response.text)
            
            logger.info(f"✅ Found {len(substitutions)} substitutions for {ingredient}")
            return substitutions
            
        except Exception as e:
            logger.error(f"❌ Substitution lookup failed: {e}")
            raise ExternalAPIError(
                "Gemini",
                f"Failed to get substitutions: {str(e)}"
            )
    
    def _parse_substitution_response(self, response_text: str) -> List[SubstitutionOption]:
        """Parse substitution response"""
        try:
            # Clean response
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            
            cleaned_text = cleaned_text.strip()
            
            # Parse JSON
            data = json.loads(cleaned_text)
            
            # Convert to SubstitutionOption objects
            substitutions = []
            for item in data:
                try:
                    sub = SubstitutionOption(
                        substitute=item.get("substitute", ""),
                        ratio=item.get("ratio", "1:1"),
                        notes=item.get("notes")
                    )
                    substitutions.append(sub)
                except Exception as e:
                    logger.warning(f"Skipping invalid substitution: {item}")
                    continue
            
            return substitutions
            
        except Exception as e:
            logger.error(f"Failed to parse substitution response: {e}")
            # Return empty list as fallback
            return []
    
    async def get_chat_response(self, prompt: str, conversation_id: str = None) -> str:
        """
        Get AI chat response for recipe assistance
        
        Args:
            prompt: The complete prompt with context and user question
            conversation_id: Optional conversation ID for context
            
        Returns:
            AI assistant's response
            
        Raises:
            ExternalAPIError: If Gemini API fails
        """
        if not self.model:
            raise ExternalAPIError(
                "Gemini",
                "Service not available. Please configure GEMINI_API_KEY."
            )
        
        try:
            # Add conversation context if available
            if conversation_id:
                # In a real implementation, you'd retrieve conversation history
                # For now, we'll use the prompt as-is
                pass
            
            response = self.model.generate_content(prompt)
            
            # Clean and validate response
            response_text = response.text.strip()
            
            # Ensure response is not too long (max 500 characters for chat)
            if len(response_text) > 500:
                response_text = response_text[:497] + "..."
            
            logger.info(f"✅ Chat response generated for conversation {conversation_id}")
            return response_text
            
        except Exception as e:
            logger.error(f"❌ Chat response failed: {e}")
            raise ExternalAPIError(
                "Gemini",
                f"Failed to get chat response: {str(e)}"
            )
    
    async def get_cooking_tip(self, question: str) -> str:
        """
        Get cooking tips and advice
        
        Args:
            question: User's cooking question
            
        Returns:
            AI-generated advice
        """
        if not self.model:
            return "AI service not available. Please configure GEMINI_API_KEY."
        
        try:
            prompt = f"""
You are a professional chef assistant. Answer this cooking question concisely and helpfully:

{question}

Provide a clear, practical answer in 2-3 sentences.
"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Failed to get cooking tip: {e}")
            return "Sorry, I couldn't generate advice at this time."


# Global service instance
gemini_service = GeminiService()

