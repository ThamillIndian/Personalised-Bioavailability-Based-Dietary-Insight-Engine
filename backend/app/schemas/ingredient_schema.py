"""
Ingredient-related request/response schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class RecognizedIngredient(BaseModel):
    """Ingredient recognized from image"""
    name: str
    confidence: float = Field(ge=0.0, le=1.0)
    quantity_estimate: Optional[str] = None
    category: Optional[str] = None


class IngredientRecognitionResponse(BaseModel):
    """Response from ingredient recognition"""
    success: bool = True
    ingredients: List[RecognizedIngredient]
    total_found: int
    processing_time_ms: int
    message: Optional[str] = None


class SubstitutionRequest(BaseModel):
    """Request for ingredient substitution"""
    ingredient: str
    context: Optional[str] = None  # e.g., "baking", "cooking", "vegan"
    recipe_type: Optional[str] = None


class SubstitutionOption(BaseModel):
    """Single substitution option"""
    substitute: str
    ratio: str  # e.g., "1:1", "1/2 cup per cup"
    notes: Optional[str] = None


class SubstitutionResponse(BaseModel):
    """Response with substitution options"""
    success: bool = True
    original_ingredient: str
    substitutions: List[SubstitutionOption]
    context: Optional[str] = None

