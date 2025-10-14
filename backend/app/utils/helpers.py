"""
Helper Functions
Utility functions used across the application
"""

from typing import List, Dict, Any
import re
from difflib import SequenceMatcher


def fuzzy_match_ingredients(ingredient1: str, ingredient2: str) -> float:
    """
    Calculate fuzzy match score between two ingredients
    
    Args:
        ingredient1: First ingredient
        ingredient2: Second ingredient
        
    Returns:
        float: Match score between 0 and 1
    """
    # Normalize
    ing1 = ingredient1.lower().strip()
    ing2 = ingredient2.lower().strip()
    
    # Exact match
    if ing1 == ing2:
        return 1.0
    
    # Check if one contains the other
    if ing1 in ing2 or ing2 in ing1:
        return 0.9
    
    # Use SequenceMatcher for fuzzy matching
    return SequenceMatcher(None, ing1, ing2).ratio()


def find_best_ingredient_match(
    target: str,
    candidates: List[str],
    threshold: float = 0.7
) -> tuple[str, float] | tuple[None, float]:
    """
    Find best matching ingredient from candidates
    
    Args:
        target: Target ingredient to match
        candidates: List of candidate ingredients
        threshold: Minimum match score (default 0.7)
        
    Returns:
        Tuple of (best_match, score) or (None, 0.0)
    """
    best_match = None
    best_score = 0.0
    
    for candidate in candidates:
        score = fuzzy_match_ingredients(target, candidate)
        if score > best_score:
            best_score = score
            best_match = candidate
    
    if best_score >= threshold:
        return best_match, best_score
    
    return None, 0.0


def extract_quantity_and_unit(ingredient_text: str) -> Dict[str, Any]:
    """
    Extract quantity and unit from ingredient text
    
    Args:
        ingredient_text: Full ingredient text (e.g., "2 cups flour")
        
    Returns:
        Dict with name, quantity, and unit
    """
    # Pattern to match quantity and unit
    pattern = r'^(\d+(?:\.\d+)?(?:/\d+)?)\s*(\w+)?\s+(.+)$'
    match = re.match(pattern, ingredient_text.strip())
    
    if match:
        quantity = match.group(1)
        unit = match.group(2) or ""
        name = match.group(3)
        
        return {
            "name": name.strip(),
            "quantity": quantity,
            "unit": unit.lower()
        }
    
    return {
        "name": ingredient_text.strip(),
        "quantity": None,
        "unit": None
    }


def calculate_match_percentage(
    recipe_ingredients: List[str],
    user_ingredients: List[str]
) -> float:
    """
    Calculate what percentage of recipe ingredients the user has
    
    Args:
        recipe_ingredients: List of ingredients needed for recipe
        user_ingredients: List of ingredients user has
        
    Returns:
        float: Match percentage (0-100)
    """
    if not recipe_ingredients:
        return 0.0
    
    matched_count = 0
    
    for recipe_ing in recipe_ingredients:
        best_match, score = find_best_ingredient_match(
            recipe_ing,
            user_ingredients,
            threshold=0.7
        )
        if best_match:
            matched_count += 1
    
    return (matched_count / len(recipe_ingredients)) * 100


def format_cooking_time(minutes: int) -> str:
    """
    Format cooking time in human-readable format
    
    Args:
        minutes: Time in minutes
        
    Returns:
        str: Formatted time string
    """
    if minutes < 60:
        return f"{minutes} min"
    
    hours = minutes // 60
    remaining_mins = minutes % 60
    
    if remaining_mins == 0:
        return f"{hours} hr"
    
    return f"{hours} hr {remaining_mins} min"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove special characters
    sanitized = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscores
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized.lower()

