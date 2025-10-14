"""
Substitution Service
Handles ingredient substitutions and alternatives
"""

from typing import List, Dict
from loguru import logger

from app.services.gemini_service import gemini_service
from app.schemas.ingredient_schema import SubstitutionOption


class SubstitutionService:
    """Service for ingredient substitutions"""
    
    # Common substitutions database (fallback if AI is unavailable)
    COMMON_SUBSTITUTIONS = {
        "butter": [
            {"substitute": "coconut oil", "ratio": "1:1", "notes": "Best for baking"},
            {"substitute": "olive oil", "ratio": "3/4 cup per cup", "notes": "For savory dishes"},
            {"substitute": "applesauce", "ratio": "1:1", "notes": "Low-fat option for baking"},
        ],
        "egg": [
            {"substitute": "flax egg", "ratio": "1 tbsp flax + 3 tbsp water", "notes": "Let sit 5 min"},
            {"substitute": "applesauce", "ratio": "1/4 cup per egg", "notes": "For baking"},
            {"substitute": "banana", "ratio": "1/4 cup mashed per egg", "notes": "Adds sweetness"},
        ],
        "milk": [
            {"substitute": "almond milk", "ratio": "1:1", "notes": "Dairy-free"},
            {"substitute": "oat milk", "ratio": "1:1", "notes": "Creamy texture"},
            {"substitute": "coconut milk", "ratio": "1:1", "notes": "Rich and creamy"},
        ],
        "sugar": [
            {"substitute": "honey", "ratio": "3/4 cup per cup", "notes": "Reduce liquid by 1/4 cup"},
            {"substitute": "maple syrup", "ratio": "3/4 cup per cup", "notes": "Natural sweetener"},
            {"substitute": "stevia", "ratio": "1 tsp per cup", "notes": "Zero calorie"},
        ],
        "flour": [
            {"substitute": "almond flour", "ratio": "1:1", "notes": "Gluten-free, denser"},
            {"substitute": "coconut flour", "ratio": "1/4 cup per cup", "notes": "Very absorbent"},
            {"substitute": "oat flour", "ratio": "1:1", "notes": "Gluten-free"},
        ],
        "soy sauce": [
            {"substitute": "tamari", "ratio": "1:1", "notes": "Gluten-free"},
            {"substitute": "coconut aminos", "ratio": "1:1", "notes": "Soy-free"},
            {"substitute": "worcestershire sauce", "ratio": "1:1", "notes": "Different flavor profile"},
        ],
    }
    
    @classmethod
    async def get_substitutions(
        cls,
        ingredient: str,
        context: str = None
    ) -> List[SubstitutionOption]:
        """
        Get substitution options for an ingredient
        
        Args:
            ingredient: Ingredient to substitute
            context: Context for substitution (baking, vegan, etc.)
            
        Returns:
            List of substitution options
        """
        # Try AI-powered substitutions first
        try:
            ai_substitutions = await gemini_service.get_ingredient_substitutions(
                ingredient,
                context
            )
            
            if ai_substitutions:
                logger.info(f"✅ Got {len(ai_substitutions)} AI substitutions for {ingredient}")
                return ai_substitutions
                
        except Exception as e:
            logger.warning(f"AI substitution failed: {e}, falling back to database")
        
        # Fallback to common substitutions
        ingredient_lower = ingredient.lower().strip()
        
        if ingredient_lower in cls.COMMON_SUBSTITUTIONS:
            subs = cls.COMMON_SUBSTITUTIONS[ingredient_lower]
            return [SubstitutionOption(**sub) for sub in subs]
        
        # Try partial matching
        for key in cls.COMMON_SUBSTITUTIONS:
            if key in ingredient_lower or ingredient_lower in key:
                subs = cls.COMMON_SUBSTITUTIONS[key]
                return [SubstitutionOption(**sub) for sub in subs]
        
        logger.warning(f"No substitutions found for {ingredient}")
        return []
    
    @classmethod
    def get_substitutions_for_dietary_restriction(
        cls,
        ingredient: str,
        restriction: str
    ) -> List[SubstitutionOption]:
        """
        Get substitutions based on dietary restriction
        
        Args:
            ingredient: Ingredient to substitute
            restriction: Dietary restriction (vegan, gluten-free, etc.)
            
        Returns:
            Filtered substitution options
        """
        # This would filter substitutions by dietary restriction
        # For now, use context-aware substitutions
        restriction_context = {
            "vegan": "plant-based vegan alternative",
            "vegetarian": "vegetarian alternative",
            "gluten-free": "gluten-free alternative",
            "dairy-free": "dairy-free alternative",
            "keto": "low-carb keto alternative",
            "paleo": "paleo-friendly alternative"
        }
        
        context = restriction_context.get(restriction.lower(), restriction)
        
        # This would typically call get_substitutions with the context
        # For now, return empty (would be implemented based on requirements)
        return []


# Global service instance
substitution_service = SubstitutionService()

