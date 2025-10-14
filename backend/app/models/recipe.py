"""
Recipe Models
Database models for recipes and related data
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4


class Ingredient(BaseModel):
    """Ingredient model"""
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    is_critical: bool = False
    category: Optional[str] = None


class NutritionInfo(BaseModel):
    """Nutritional information model"""
    calories: Optional[int] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    sodium: Optional[float] = None


class RecipeInstruction(BaseModel):
    """Single recipe instruction step"""
    step_number: int
    instruction: str
    duration_minutes: Optional[int] = None


class Recipe(BaseModel):
    """Complete recipe model"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    difficulty: str = "medium"  # easy, medium, hard
    prep_time: int  # minutes
    cook_time: int  # minutes
    servings: int = 4
    image_url: Optional[str] = None
    ingredients: List[Ingredient]
    instructions: List[RecipeInstruction]
    dietary_tags: List[str] = Field(default_factory=list)
    nutrition: Optional[NutritionInfo] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    @property
    def total_time(self) -> int:
        """Calculate total cooking time"""
        return self.prep_time + self.cook_time
    
    @property
    def ingredient_names(self) -> List[str]:
        """Get list of ingredient names"""
        return [ing.name for ing in self.ingredients]


class RecipeMatch(BaseModel):
    """Recipe with match score"""
    recipe: Recipe
    match_percentage: float
    matched_ingredients: List[str]
    missing_ingredients: List[str]
    can_make_with_substitutions: bool = False


class RecipeFilter(BaseModel):
    """Filter criteria for recipe search"""
    ingredients: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    cuisine_type: Optional[str] = None
    max_prep_time: Optional[int] = None
    max_cook_time: Optional[int] = None
    difficulty: Optional[str] = None
    max_calories: Optional[int] = None
    min_protein: Optional[float] = None
    servings: Optional[int] = None

