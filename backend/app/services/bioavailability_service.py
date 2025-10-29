"""
Bioavailability computation service
"""

import os
import logging
from typing import Dict, List
import pandas as pd

from app.schemas.nutrition_schema import IngredientInfo, CookingMethod, StressLevel
from app.services.nutrient_calculator import nutrient_calculator

logger = logging.getLogger(__name__)


class BioavailabilityEngine:
    def __init__(self, data_dir: str = "data"):
        self.retention_factors = None
        self.digestibility_scores = None
        self._load(data_dir)

    def _load(self, data_dir: str):
        try:
            rf = os.path.join(data_dir, "retention_factors.csv")
            dg = os.path.join(data_dir, "digestibility_scores.csv")
            if os.path.exists(rf):
                self.retention_factors = pd.read_csv(rf)
                logger.info(f"Loaded retention_factors: {self.retention_factors.shape}")
            if os.path.exists(dg):
                self.digestibility_scores = pd.read_csv(dg)
                logger.info(f"Loaded digestibility_scores: {self.digestibility_scores.shape}")
        except Exception as e:
            logger.error(f"Failed loading nutrition factors: {e}")

    def compute(self,
                ingredients: List[IngredientInfo],
                cooking_method: CookingMethod,
                stress_level: StressLevel,
                age: int,
                post_workout: bool) -> Dict[str, Dict[str, float]]:
        # Use dataset-driven base nutrients
        base = nutrient_calculator.calculate_nutrients(ingredients)

        adjusted: Dict[str, float] = {}
        for nutrient, value in base.items():
            r = self._retention(cooking_method, nutrient)
            d = self._digestibility(ingredients, nutrient)
            p = self._physio(stress_level, age, post_workout, nutrient)
            adjusted[nutrient] = round(value * r * d * p, 2)

        return {
            "base_nutrients": base,
            "adjusted_nutrients": adjusted,
            "adjustment_factors": {
                "cooking_method": cooking_method.value,
                "stress_level": stress_level.value,
                "age": age,
                "post_workout": post_workout,
            }
        }

    def _estimate_base(self, ings: List[IngredientInfo]) -> Dict[str, float]:
        # Legacy heuristic (unused); kept for reference
        return {}

    def _retention(self, method: CookingMethod, nutrient: str) -> float:
        if self.retention_factors is None:
            return 0.85
        typ = self._nutrient_type(nutrient)
        df = self.retention_factors
        row = df[(df["cooking_method"] == method.value) & (df["nutrient_type"] == typ)]
        return float(row.iloc[0]["retention_factor"]) if not row.empty else 0.85

    def _digestibility(self, ings: List[IngredientInfo], nutrient: str) -> float:
        if self.digestibility_scores is None:
            return 0.8
        total = sum(i.quantity_g for i in ings) or 1.0
        wsum = 0.0
        for i in ings:
            cat_key = (i.category or "Unknown").strip().lower()
            row = self.digestibility_scores[self.digestibility_scores["food_category"].str.lower() == cat_key]
            if row.empty:
                row = self.digestibility_scores[self.digestibility_scores["food_category"].str.lower() == "unknown"]
            factor = float(row.iloc[0]["digestibility_factor"]) if not row.empty else 0.8
            wsum += (i.quantity_g / total) * factor
        return wsum

    def _physio(self, stress: StressLevel, age: int, post: bool, nutrient: str) -> float:
        f = 1.0
        f *= 0.85 if stress == StressLevel.high else (0.92 if stress == StressLevel.medium else 1.0)
        f *= 1.1 if age < 18 else (0.9 if age > 65 else 1.0)
        nl = nutrient.lower()
        if post:
            if "protein" in nl:
                f *= 1.15
            elif "carb" in nl:
                f *= 1.1
            elif any(x in nl for x in ["mineral", "calcium", "iron", "zinc"]):
                f *= 1.05
        return f

    def _nutrient_type(self, n: str) -> str:
        n = n.lower()
        if any(x in n for x in ["protein", "amino"]):
            return "Protein"
        if any(x in n for x in ["carb", "sugar", "starch", "fiber"]):
            return "Carbohydrates"
        if any(x in n for x in ["fat", "lipid", "oil"]):
            return "Fat"
        if any(x in n for x in ["vitamin", "folate", "thiamine", "riboflavin", "niacin"]):
            return "Vitamins"
        if any(x in n for x in ["calcium", "iron", "magnesium", "phosphorus", "potassium", "sodium", "zinc"]):
            return "Minerals"
        return "Minerals"


bioavailability_engine = BioavailabilityEngine()


