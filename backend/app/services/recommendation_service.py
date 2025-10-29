"""
Simple recommendation engine for low RDA coverage nutrients
"""

from typing import Dict, List


FOOD_SOURCES: Dict[str, Dict[str, List[str]]] = {
    "protein_g": {
        "high": ["Chicken breast", "Eggs", "Paneer", "Fish", "Greek yogurt"],
        "medium": ["Lentils", "Chickpeas", "Tofu", "Peas"],
    },
    "iron_mg": {
        "high": ["Liver", "Clams", "Pumpkin seeds", "Spinach (with Vitamin C)"],
        "medium": ["Chickpeas", "Kidney beans", "Jaggery"],
    },
    "calcium_mg": {
        "high": ["Milk", "Paneer", "Curd", "Ragi (finger millet)"],
        "medium": ["Almonds", "Sesame seeds", "Tofu (calcium set)"],
    },
    "vitamin_c_mg": {
        "high": ["Amla", "Guava", "Bell peppers", "Citrus fruits"],
        "medium": ["Tomato", "Strawberries", "Broccoli"],
    },
    "zinc_mg": {
        "high": ["Oysters", "Beef", "Pumpkin seeds"],
        "medium": ["Cashews", "Chickpeas", "Yogurt"],
    },
    "fiber_g": {
        "high": ["Oats", "Chia seeds", "Flaxseed", "Pear", "Apple (with skin)"],
        "medium": ["Whole wheat roti", "Vegetables", "Beans"],
    },
    "carb_g": {
        "high": ["Rice", "Roti", "Poha", "Idli", "Banana"],
        "medium": ["Quinoa", "Oats", "Sweet potato"],
    },
    "fat_g": {
        "high": ["Nuts", "Seeds", "Ghee", "Cold-pressed oils"],
        "medium": ["Avocado", "Paneer", "Whole milk"],
    },
    "vitamin_a_ug": {
        "high": ["Carrots", "Sweet potato", "Spinach", "Liver"],
        "medium": ["Pumpkin", "Mango"],
    },
}


def _map_alias(name: str) -> str:
    aliases = {
        "protein": "protein_g",
        "carbs": "carb_g",
        "carbohydrates": "carb_g",
        "fat": "fat_g",
        "fiber": "fiber_g",
        "vitamin_c": "vitamin_c_mg",
        "vitamin_a": "vitamin_a_ug",
        "calcium": "calcium_mg",
        "iron": "iron_mg",
        "zinc": "zinc_mg",
    }
    return aliases.get(name.lower(), name)


def generate_recommendations(rda_coverage: Dict[str, str]) -> List[Dict[str, object]]:
    """Create suggestions for nutrients with coverage < 50%"""
    flagged: List[Dict[str, object]] = []
    for name, pct_str in rda_coverage.items():
        if pct_str == "N/A":
            continue
        try:
            pct = float(pct_str.replace("%", ""))
        except Exception:
            continue
        if pct < 50.0:
            key = name if name in FOOD_SOURCES else _map_alias(name)
            foods = FOOD_SOURCES.get(key, {})
            flagged.append({
                "nutrient": name,
                "coverage": pct_str,
                "suggestions": {
                    "high": foods.get("high", [])[:3],
                    "medium": foods.get("medium", [])[:3],
                }
            })
    flagged.sort(key=lambda x: float(x["coverage"].replace("%", "")) if x["coverage"] != "N/A" else 999)
    return flagged


