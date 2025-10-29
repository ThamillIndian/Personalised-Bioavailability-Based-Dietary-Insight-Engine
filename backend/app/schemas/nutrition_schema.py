"""
Nutrition schemas for bioavailability and RDA endpoints
"""

from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Dict, Optional


class CookingMethod(str, Enum):
    boiling = "Boiled"
    steaming = "Steamed"
    frying = "Fried"
    baking = "Baked"
    saute = "Sauteed"
    pressure_cook = "Pressure Cooked"
    raw = "Raw"


class StressLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class IngredientInfo(BaseModel):
    name: str
    quantity_g: float = Field(gt=0)
    category: str


class BioavailabilityRequest(BaseModel):
    ingredients: List[IngredientInfo]
    cooking_method: CookingMethod
    stress_level: StressLevel = StressLevel.low
    age: int = Field(ge=1, le=120)
    post_workout: bool = False

    # Optional context (accepted for future physiological adjustments)
    sleep_hours: Optional[float] = None
    meal_time: Optional[str] = None
    time_since_last_meal_min: Optional[int] = None
    hydration_liters: Optional[float] = None
    caffeine_mg: Optional[int] = None
    menstrual_phase: Optional[str] = None


class BioavailabilityResponse(BaseModel):
    success: bool = True
    base_nutrients: Dict[str, float]
    adjusted_nutrients: Dict[str, float]
    adjustment_factors: Dict[str, object]


class RDACoverageRequest(BaseModel):
    adjusted_nutrients: Dict[str, float]
    age: int = Field(ge=1, le=120)
    weight_kg: float = Field(gt=0, le=300)
    height_cm: float = Field(gt=0, le=250)


class RDACoverageResponse(BaseModel):
    success: bool = True
    rda_coverage: Dict[str, str]
    user_profile: Dict[str, object]
    recommendations: List[Dict[str, object]] = []
    recommendation_count: int = 0


