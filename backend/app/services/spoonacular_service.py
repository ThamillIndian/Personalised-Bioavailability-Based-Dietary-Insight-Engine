"""
Spoonacular API Service
Integration with Spoonacular for recipe data and nutritional information
"""

import httpx
from typing import List, Dict, Optional, Any
from loguru import logger

from app.config import settings
from app.models.recipe import Recipe, Ingredient, RecipeInstruction, NutritionInfo
from app.utils.error_handlers import ExternalAPIError, RecipeNotFoundError


class SpoonacularService:
    """Service for Spoonacular API operations"""
    
    def __init__(self):
        """Initialize Spoonacular service"""
        self.base_url = settings.SPOONACULAR_BASE_URL
        self.api_key = settings.SPOONACULAR_API_KEY
        
        if not self.api_key or self.api_key == "your-spoonacular-api-key":
            logger.warning("⚠️ Spoonacular API key not configured")
        else:
            logger.info("✅ Spoonacular service initialized")
    
    async def search_recipes_by_ingredients(
        self,
        ingredients: List[str],
        number: int = 10,
        ranking: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Search recipes by ingredients using Spoonacular
        
        Args:
            ingredients: List of ingredient names
            number: Number of recipes to return
            ranking: Ranking strategy (1=minimize missing, 2=maximize used)
            
        Returns:
            List of recipe data from Spoonacular
            
        Raises:
            ExternalAPIError: If API call fails
        """
        if not self.api_key or self.api_key == "your-spoonacular-api-key":
            logger.warning("Spoonacular API not configured, returning empty results")
            return []
        
        try:
            endpoint = f"{self.base_url}/recipes/findByIngredients"
            params = {
                "apiKey": self.api_key,
                "ingredients": ",".join(ingredients),
                "number": number,
                "ranking": ranking,
                "ignorePantry": False
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(endpoint, params=params, timeout=10.0)
                response.raise_for_status()
                
                recipes = response.json()
                logger.info(f"✅ Found {len(recipes)} recipes from Spoonacular")
                return recipes
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Spoonacular API error: {e.response.status_code}")
            raise ExternalAPIError(
                "Spoonacular",
                f"API returned status {e.response.status_code}",
                details={"status_code": e.response.status_code}
            )
        except Exception as e:
            logger.error(f"Failed to search recipes: {e}")
            raise ExternalAPIError("Spoonacular", str(e))
    
    async def get_recipe_information(self, recipe_id: int) -> Dict[str, Any]:
        """
        Get detailed recipe information
        
        Args:
            recipe_id: Spoonacular recipe ID
            
        Returns:
            Detailed recipe data
            
        Raises:
            RecipeNotFoundError: If recipe not found
            ExternalAPIError: If API call fails
        """
        if not self.api_key or self.api_key == "your-spoonacular-api-key":
            raise ExternalAPIError("Spoonacular", "API key not configured")
        
        try:
            endpoint = f"{self.base_url}/recipes/{recipe_id}/information"
            params = {
                "apiKey": self.api_key,
                "includeNutrition": True
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(endpoint, params=params, timeout=10.0)
                
                if response.status_code == 404:
                    raise RecipeNotFoundError(str(recipe_id))
                
                response.raise_for_status()
                return response.json()
                
        except RecipeNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get recipe info: {e}")
            raise ExternalAPIError("Spoonacular", str(e))
    
    async def get_recipe_nutrition(self, recipe_id: int) -> Optional[NutritionInfo]:
        """
        Get nutritional information for a recipe
        
        Args:
            recipe_id: Spoonacular recipe ID
            
        Returns:
            NutritionInfo object or None
        """
        if not self.api_key or self.api_key == "your-spoonacular-api-key":
            return None
        
        try:
            endpoint = f"{self.base_url}/recipes/{recipe_id}/nutritionWidget.json"
            params = {"apiKey": self.api_key}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(endpoint, params=params, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                
                # Parse nutrition data
                return NutritionInfo(
                    calories=int(data.get("calories", 0)),
                    protein=float(data.get("protein", "0g").replace("g", "")),
                    carbs=float(data.get("carbs", "0g").replace("g", "")),
                    fat=float(data.get("fat", "0g").replace("g", ""))
                )
                
        except Exception as e:
            logger.warning(f"Failed to get nutrition info: {e}")
            return None
    
    def convert_spoonacular_to_recipe(self, spoon_data: Dict[str, Any]) -> Recipe:
        """
        Convert Spoonacular recipe data to our Recipe model
        
        Args:
            spoon_data: Raw data from Spoonacular API
            
        Returns:
            Recipe object
        """
        # Extract ingredients
        ingredients = []
        for ing in spoon_data.get("extendedIngredients", []):
            ingredients.append(Ingredient(
                name=ing.get("nameClean") or ing.get("name", ""),
                quantity=ing.get("amount"),
                unit=ing.get("unit"),
                category=ing.get("aisle", "other")
            ))
        
        # Extract instructions
        instructions = []
        if spoon_data.get("analyzedInstructions"):
            for step in spoon_data["analyzedInstructions"][0].get("steps", []):
                instructions.append(RecipeInstruction(
                    step_number=step.get("number", 0),
                    instruction=step.get("step", ""),
                    duration_minutes=None
                ))
        elif spoon_data.get("instructions"):
            # Fallback: split text instructions
            text_instructions = spoon_data["instructions"].split(".")
            for i, instruction in enumerate(text_instructions, 1):
                if instruction.strip():
                    instructions.append(RecipeInstruction(
                        step_number=i,
                        instruction=instruction.strip(),
                        duration_minutes=None
                    ))
        
        # Extract dietary tags
        dietary_tags = []
        if spoon_data.get("vegetarian"):
            dietary_tags.append("vegetarian")
        if spoon_data.get("vegan"):
            dietary_tags.append("vegan")
        if spoon_data.get("glutenFree"):
            dietary_tags.append("gluten-free")
        if spoon_data.get("dairyFree"):
            dietary_tags.append("dairy-free")
        
        # Extract nutrition
        nutrition = None
        if spoon_data.get("nutrition"):
            nutrients = {n["name"]: n["amount"] for n in spoon_data["nutrition"].get("nutrients", [])}
            nutrition = NutritionInfo(
                calories=int(nutrients.get("Calories", 0)),
                protein=nutrients.get("Protein", 0),
                carbs=nutrients.get("Carbohydrates", 0),
                fat=nutrients.get("Fat", 0),
                fiber=nutrients.get("Fiber", 0),
                sugar=nutrients.get("Sugar", 0)
            )
        
        # Create Recipe object
        return Recipe(
            id=None,  # Will be generated or assigned by database
            title=spoon_data.get("title", "Untitled Recipe"),
            description=spoon_data.get("summary", ""),
            cuisine_type=spoon_data.get("cuisines", [""])[0] if spoon_data.get("cuisines") else None,
            difficulty="medium",  # Spoonacular doesn't provide this
            prep_time=spoon_data.get("preparationMinutes", 15),
            cook_time=spoon_data.get("cookingMinutes", 30),
            servings=spoon_data.get("servings", 4),
            image_url=spoon_data.get("image"),
            ingredients=ingredients,
            instructions=instructions,
            dietary_tags=dietary_tags,
            nutrition=nutrition
        )


# Global service instance
spoonacular_service = SpoonacularService()

