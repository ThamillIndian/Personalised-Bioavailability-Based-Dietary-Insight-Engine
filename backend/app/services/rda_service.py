"""
RDA coverage calculator service
"""

import os
import csv
from typing import Dict, Tuple


class RDACalculator:
    def __init__(self, csv_path: str = "data/rda_values.csv"):
        self.data = self._load(csv_path)

    def _load(self, path: str) -> Dict:
        d: Dict[Tuple[str, str], Dict[str, float]] = {}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    key = (row["age_group"], row["gender"])
                    d[key] = {}
                    for k, v in row.items():
                        if k in ("age_group", "gender"):
                            continue
                        try:
                            d[key][k] = float(v)
                        except Exception:
                            d[key][k] = 0.0
        else:
            d[("19-30_years", "male")] = {"protein_g": 56.0, "energy_kcal": 2400.0}
        return d

    def _age_group(self, age: int) -> str:
        if age <= 3: return "1-3_years"
        if age <= 8: return "4-8_years"
        if age <= 13: return "9-13_years"
        if age <= 18: return "14-18_years"
        if age <= 30: return "19-30_years"
        if age <= 50: return "31-50_years"
        if age <= 70: return "51-70_years"
        return "70+_years"

    def _gender(self, weight: float, height: float) -> str:
        bmi = weight / ((height / 100.0) ** 2)
        return "male" if bmi > 25 else "female"

    def coverage(self, nutrients: Dict[str, float], age: int, weight: float, height: float) -> Dict[str, str]:
        key = (self._age_group(age), self._gender(weight, height))
        rda = self.data.get(key) or self.data.get(("19-30_years", "male"), {})
        out: Dict[str, str] = {}
        for name, value in nutrients.items():
            rkey = self._map(name)
            if rkey and rkey in rda and rda[rkey] > 0:
                out[name] = f"{(value / rda[rkey]) * 100:.1f}%"
            else:
                out[name] = "N/A"
        return out

    def _map(self, n: str) -> str:
        m = {
            # macros
            "protein_g": "protein_g",
            "fat_g": "fat_g",
            "carb_g": "carb_g",
            "fiber_g": "fiber_g",
            "energy_kcal": "energy_kcal",
            # minerals
            "calcium_mg": "calcium_mg",
            "iron_mg": "iron_mg",
            "zinc_mg": "zinc_mg",
            "magnesium_mg": "magnesium_mg",
            "phosphorus_mg": "phosphorus_mg",
            "potassium_mg": "potassium_mg",
            "sodium_mg": "sodium_mg",
            "copper_mg": "copper_mg",
            "manganese_mg": "manganese_mg",
            "selenium_ug": "selenium_ug",
            "chromium_mg": "chromium_mg",
            "molybdenum_mg": "molybdenum_mg",
            # vitamins
            "vitamin_a_ug": "vitamin_a_ug",
            "vitamin_c_mg": "vitamin_c_mg",
            "vitamin_d_ug": "vitamin_d_ug",
            "vitamin_e_mg": "vitamin_e_mg",
            "vitamin_k_ug": "vitamin_k_ug",
            "vitamin_b1_mg": "vitamin_b1_mg",
            "vitamin_b2_mg": "vitamin_b2_mg",
            "vitamin_b3_mg": "vitamin_b3_mg",
            "vitamin_b5_mg": "vitamin_b5_mg",
            "vitamin_b6_mg": "vitamin_b6_mg",
            "vitamin_b7_ug": "vitamin_b7_ug",
            "vitamin_b9_ug": "vitamin_b9_ug",
            "vitamin_b12_ug": "vitamin_b12_ug",
            # common aliases mapping could be added in caller
        }
        return m.get(n, "")


rda_calculator = RDACalculator()


