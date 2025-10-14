"""
Recipe-related request/response schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from app.models.recipe import Recipe, RecipeMatch


class DietaryRestriction(str, Enum):
    """Valid dietary restrictions for recipe filtering"""
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten-free"
    DAIRY_FREE = "dairy-free"
    NUT_FREE = "nut-free"
    EGG_FREE = "egg-free"
    SOY_FREE = "soy-free"
    LOW_CARB = "low-carb"
    KETO = "keto"
    PALEO = "paleo"
    PESCATARIAN = "pescatarian"
    HALAL = "halal"
    KOSHER = "kosher"


class CuisineType(str, Enum):
    """Valid cuisine types available in the recipe database"""
    ITALIAN = "Italian"
    INDIAN = "Indian"
    MEXICAN = "Mexican"
    JAPANESE = "Japanese"
    THAI = "Thai"
    CHINESE = "Chinese"
    GREEK = "Greek"
    FRENCH = "French"
    AMERICAN = "American"
    MEDITERRANEAN = "Mediterranean"
    MIDDLE_EASTERN = "Middle Eastern"
    HAWAIIAN = "Hawaiian"


class DifficultyLevel(str, Enum):
    """Valid difficulty levels for recipes"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class RecipeSearchRequest(BaseModel):
    """🍳 Search recipes by ingredients and preferences - Form Interface"""
    
    model_config = {
        "json_schema_extra": {
            "title": "Recipe Search Form",
            "description": "Fill out this form to find recipes based on your available ingredients and preferences",
            "examples": [
                {
                    "ingredients": ["chicken breast", "tomato", "onion", "garlic"],
                    "dietary_restrictions": ["gluten-free"],
                    "cuisine_type": "Indian",
                    "max_prep_time": 30,
                    "max_cook_time": 45,
                    "difficulty": "medium",
                    "limit": 5
                },
                {
                    "ingredients": ["pasta", "cheese", "tomato"],
                    "dietary_restrictions": ["vegetarian"],
                    "cuisine_type": "Italian",
                    "difficulty": "easy",
                    "limit": 3
                }
            ]
        }
    }
    
    # Required field - will show as text input
    ingredients: List[str] = Field(
        min_items=1,
        title="Available Ingredients",
        description="📝 Enter the ingredients you have available (e.g., chicken, tomato, onion). Separate multiple ingredients with commas or add them one by one.",
        example=["chicken breast", "tomato", "onion", "garlic"],
        json_schema_extra={
            "input_type": "text",
            "placeholder": "chicken, tomato, onion, garlic"
        }
    )
    
    # Optional multi-select dropdown
    dietary_restrictions: Optional[List[DietaryRestriction]] = Field(
        None,
        title="Dietary Restrictions",
        description="🥗 Select any dietary restrictions that apply (you can choose multiple)",
        example=[DietaryRestriction.VEGETARIAN],
        json_schema_extra={
            "input_type": "checkbox",
            "help_text": "Choose all that apply"
        }
    )
    
    # Optional single-select dropdown
    cuisine_type: Optional[CuisineType] = Field(
        None,
        title="Preferred Cuisine",
        description="🌍 Choose your preferred cuisine type",
        example=CuisineType.ITALIAN,
        json_schema_extra={
            "input_type": "select",
            "placeholder": "Select cuisine type"
        }
    )
    
    # Optional number input with constraints
    max_prep_time: Optional[int] = Field(
        None,
        gt=0,
        le=480,  # 8 hours max
        title="Maximum Prep Time",
        description="⏱️ Maximum preparation time in minutes (leave empty for no limit)",
        example=30,
        json_schema_extra={
            "input_type": "number",
            "min": 1,
            "max": 480,
            "step": 5,
            "placeholder": "30"
        }
    )
    
    # Optional number input with constraints
    max_cook_time: Optional[int] = Field(
        None,
        gt=0,
        le=480,  # 8 hours max
        title="Maximum Cook Time",
        description="🍳 Maximum cooking time in minutes (leave empty for no limit)",
        example=45,
        json_schema_extra={
            "input_type": "number",
            "min": 1,
            "max": 480,
            "step": 5,
            "placeholder": "45"
        }
    )
    
    # Optional single-select dropdown
    difficulty: Optional[DifficultyLevel] = Field(
        None,
        title="Difficulty Level",
        description="🎯 Choose your preferred cooking difficulty level",
        example=DifficultyLevel.MEDIUM,
        json_schema_extra={
            "input_type": "select",
            "placeholder": "Select difficulty"
        }
    )
    
    # Required number input with constraints
    limit: int = Field(
        10,
        ge=1,
        le=50,
        title="Number of Results",
        description="📊 How many recipes would you like to see? (1-50)",
        example=5,
        json_schema_extra={
            "input_type": "number",
            "min": 1,
            "max": 50,
            "step": 1,
            "placeholder": "10"
        }
    )


class RecipeSearchResponse(BaseModel):
    """Response from recipe search"""
    success: bool = True
    recipes: List[RecipeMatch]
    total_found: int
    query_info: dict


class RecipeDetailResponse(BaseModel):
    """Response with single recipe detail"""
    success: bool = True
    recipe: Recipe


class RecipeListResponse(BaseModel):
    """Response with list of recipes"""
    success: bool = True
    recipes: List[Recipe]
    total: int
    page: int = 1
    page_size: int = 10


class FavoriteRequest(BaseModel):
    """Request to add/remove favorite"""
    recipe_id: str
    user_id: str  # Can be session ID or user ID


class RatingRequest(BaseModel):
    """Request to rate a recipe"""
    recipe_id: str
    user_id: str
    rating: int = Field(ge=1, le=5)
    review: Optional[str] = None


class RatingResponse(BaseModel):
    """Response after rating"""
    success: bool = True
    message: str
    average_rating: Optional[float] = None
    total_ratings: Optional[int] = None


class RecipeRecommendationRequest(BaseModel):
    """Request for personalized recommendations"""
    user_id: str
    limit: int = Field(5, ge=1, le=20)
    based_on_favorites: bool = True
    based_on_ratings: bool = True

