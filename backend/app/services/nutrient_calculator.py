"""
Nutrient Calculator Service
Paritizes Pre_capstone behavior: loads Anuvaad + Food Composition datasets
and calculates base nutrients from ingredient names and quantities.
"""

import os
import logging
from typing import Dict, List, Optional, Tuple

import pandas as pd

from app.schemas.nutrition_schema import IngredientInfo

logger = logging.getLogger(__name__)


class NutrientCalculator:
    def __init__(self):
        self.anuvaad_data: Optional[pd.DataFrame] = None
        self.food_composition_data: Optional[pd.DataFrame] = None
        self.nutrient_columns: List[str] = []
        self._load_datasets()

    def _load_datasets(self) -> None:
        try:
            # Prefer Anuvaad with bioavailability cols
            preferred = "data/Anuvaad_INDB_2024.11_with_bioavailability_columns.xlsx"
            fallbacks = [
                "data/Anuvaad_INDB_2024.11_with_all_RD_factors.xlsx",
                "data/Anuvaad_INDB_2024.11_with_Indian_RD_factors.xlsx",
            ]
            if os.path.exists(preferred):
                self.anuvaad_data = pd.read_excel(preferred)
                logger.info(f"Loaded Anuvaad dataset: {self.anuvaad_data.shape}")
            else:
                for path in fallbacks:
                    if os.path.exists(path):
                        self.anuvaad_data = pd.read_excel(path)
                        logger.info(f"Loaded Anuvaad dataset from {path}: {self.anuvaad_data.shape}")
                        break

            food_comp_path = "data/Food Composition.csv"
            if os.path.exists(food_comp_path):
                self.food_composition_data = pd.read_csv(food_comp_path)
                logger.info(
                    f"Loaded Food Composition dataset: {self.food_composition_data.shape}"
                )

            if self.anuvaad_data is not None:
                self._identify_nutrient_columns()
            else:
                logger.error("No Anuvaad dataset found! Nutrient calculation may be empty.")
        except Exception as e:
            logger.error(f"Error loading nutrient datasets: {e}")

    def _identify_nutrient_columns(self) -> None:
        if self.anuvaad_data is None:
            return
        exclude = {"food_code", "food_name", "primarysource", "servings_unit"}
        self.nutrient_columns = [
            c
            for c in self.anuvaad_data.columns
            if c not in exclude and not str(c).startswith("unit_serving_")
        ]
        logger.info(f"Identified {len(self.nutrient_columns)} nutrient columns")

    def _alternative_names(self, ingredient_name: str) -> str:
        alternatives = {
            "rice": "rice|chawal|basmati",
            "wheat": "wheat|gehun|atta",
            "lentils": "lentil|dal|toor|moong|masoor",
            "chickpeas": "chickpea|chana|kabuli",
            "kidney beans": "kidney|rajma|red bean",
            "onion": "onion|pyaaz",
            "tomato": "tomato|tamatar",
            "potato": "potato|aloo",
            "chicken": "chicken|murgh",
            "paneer": "paneer|cottage cheese",
            "yogurt": "yogurt|curd|dahi",
            "milk": "milk|doodh",
            "oil": "oil|tel|ghee|butter",
            "ginger": "ginger|adrak",
            "garlic": "garlic|lehsun",
            "spinach": "spinach|palak",
            "cauliflower": "cauliflower|gobi|phool gobi",
        }
        for key, patt in alternatives.items():
            if key in ingredient_name.lower():
                return patt
        return ingredient_name

    def _find_food(self, name: str) -> Optional[pd.Series]:
        if self.anuvaad_data is None:
            return None
        try:
            df = self.anuvaad_data
            exact = df[df["food_name"].str.lower() == name.lower()]
            if not exact.empty:
                return exact.iloc[0]
            contains = df[df["food_name"].str.lower().str.contains(name.lower(), na=False)]
            if not contains.empty:
                return contains.iloc[0]
            alt = df[df["food_name"].str.lower().str.contains(self._alternative_names(name), na=False)]
            if not alt.empty:
                return alt.iloc[0]
            logger.warning(f"Food not found: {name}")
            return None
        except Exception as e:
            logger.error(f"Error finding food {name}: {e}")
            return None

    def _calc_for_item(self, food: pd.Series, qty_g: float) -> Dict[str, float]:
        out: Dict[str, float] = {}
        try:
            scale = qty_g / 100.0
            for col in self.nutrient_columns:
                if col in food.index and pd.notna(food[col]):
                    try:
                        out[col] = float(food[col]) * scale
                    except (ValueError, TypeError):
                        continue
            return out
        except Exception as e:
            logger.error(f"Error calculating nutrients for item: {e}")
            return {}

    def calculate_nutrients(self, ingredients: List[IngredientInfo]) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        try:
            for ing in ingredients:
                food = self._find_food(ing.name)
                if food is None:
                    continue
                vals = self._calc_for_item(food, ing.quantity_g)
                for k, v in vals.items():
                    totals[k] = totals.get(k, 0.0) + v
            return {k: round(v, 2) for k, v in totals.items()}
        except Exception as e:
            logger.error(f"Error calculating nutrients: {e}")
            return {}


nutrient_calculator = NutrientCalculator()


