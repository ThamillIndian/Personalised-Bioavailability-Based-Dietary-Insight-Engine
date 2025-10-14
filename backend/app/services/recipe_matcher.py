"""
Recipe Matching Algorithm
Smart algorithm to match recipes with available ingredients
This is the SECRET SAUCE that makes the app intelligent! 🧠
"""

from typing import List, Dict, Tuple
from loguru import logger

from app.models.recipe import Recipe, RecipeMatch
from app.utils.helpers import (
    fuzzy_match_ingredients,
    find_best_ingredient_match,
    calculate_match_percentage
)


class RecipeMatcher:
    """
    Advanced recipe matching algorithm
    
    Scoring formula:
    - Base match: percentage of recipe ingredients the user has
    - Fuzzy matching: partial matches get bonus points
    - Critical ingredients: missing critical ingredients = penalty
    - Dietary compliance: must match 100% or recipe is filtered out
    - User preferences: recipes matching preferences get boost
    """
    
    # Matching thresholds
    FUZZY_MATCH_THRESHOLD = 0.7  # 70% similarity for fuzzy match
    MIN_MATCH_PERCENTAGE = 10.0  # Minimum 10% ingredients matched (show recipes with at least 1 ingredient match)
    
    # Scoring weights
    WEIGHT_EXACT_MATCH = 1.0
    WEIGHT_FUZZY_MATCH = 0.8
    WEIGHT_CRITICAL_PENALTY = 20.0
    WEIGHT_PREFERENCE_BOOST = 10.0
    
    @classmethod
    def match_recipes(
        cls,
        recipes: List[Recipe],
        user_ingredients: List[str],
        dietary_restrictions: List[str] = None,
        max_cook_time: int = None,
        difficulty: str = None
    ) -> List[RecipeMatch]:
        """
        Match recipes against user ingredients and preferences
        
        Args:
            recipes: List of available recipes
            user_ingredients: Ingredients user has
            dietary_restrictions: User's dietary restrictions
            max_cook_time: Maximum cooking time in minutes
            difficulty: Preferred difficulty level
            
        Returns:
            List of RecipeMatch objects, sorted by match score
        """
        logger.info(f"🔍 Matching {len(recipes)} recipes against {len(user_ingredients)} ingredients")
        
        matched_recipes = []
        
        for recipe in recipes:
            # Pre-filter by dietary restrictions
            if dietary_restrictions:
                if not cls._check_dietary_compliance(recipe, dietary_restrictions):
                    continue
            
            # Pre-filter by cook time
            if max_cook_time and recipe.total_time > max_cook_time:
                continue
            
            # Pre-filter by difficulty
            if difficulty and recipe.difficulty != difficulty.lower():
                continue
            
            # Calculate match score
            match_result = cls._calculate_recipe_match(
                recipe,
                user_ingredients,
                dietary_restrictions or []
            )
            
            # Only include recipes with minimum match percentage
            if match_result["match_percentage"] >= cls.MIN_MATCH_PERCENTAGE:
                recipe_match = RecipeMatch(
                    recipe=recipe,
                    match_percentage=match_result["match_percentage"],
                    matched_ingredients=match_result["matched"],
                    missing_ingredients=match_result["missing"],
                    can_make_with_substitutions=match_result["can_substitute"]
                )
                matched_recipes.append(recipe_match)
        
        # Sort by match percentage (highest first)
        matched_recipes.sort(key=lambda x: x.match_percentage, reverse=True)
        
        logger.info(f"✅ Found {len(matched_recipes)} matching recipes")
        
        return matched_recipes
    
    @classmethod
    def _calculate_recipe_match(
        cls,
        recipe: Recipe,
        user_ingredients: List[str],
        dietary_restrictions: List[str]
    ) -> Dict:
        """
        Calculate detailed match score for a recipe
        
        Returns:
            Dict with match_percentage, matched, missing, and can_substitute
        """
        recipe_ingredients = recipe.ingredient_names
        
        if not recipe_ingredients:
            return {
                "match_percentage": 0.0,
                "matched": [],
                "missing": [],
                "can_substitute": False
            }
        
        matched_ingredients = []
        missing_ingredients = []
        fuzzy_matched = []
        
        # Check each recipe ingredient
        for recipe_ing in recipe_ingredients:
            # Try exact match first
            exact_match = cls._find_exact_match(recipe_ing, user_ingredients)
            
            if exact_match:
                matched_ingredients.append(recipe_ing)
            else:
                # Try fuzzy match
                fuzzy_match, score = find_best_ingredient_match(
                    recipe_ing,
                    user_ingredients,
                    threshold=cls.FUZZY_MATCH_THRESHOLD
                )
                
                if fuzzy_match:
                    matched_ingredients.append(recipe_ing)
                    fuzzy_matched.append((recipe_ing, fuzzy_match, score))
                else:
                    missing_ingredients.append(recipe_ing)
        
        # Calculate base match percentage
        exact_matches = len(matched_ingredients) - len(fuzzy_matched)
        fuzzy_count = len(fuzzy_matched)
        
        # Weighted score
        score = (
            exact_matches * cls.WEIGHT_EXACT_MATCH +
            fuzzy_count * cls.WEIGHT_FUZZY_MATCH
        )
        
        match_percentage = (score / len(recipe_ingredients)) * 100
        
        # Check for critical missing ingredients
        critical_missing = cls._check_critical_ingredients(recipe, missing_ingredients)
        if critical_missing:
            # Apply penalty for missing critical ingredients
            match_percentage = max(0, match_percentage - cls.WEIGHT_CRITICAL_PENALTY)
        
        # Dietary compliance boost
        if dietary_restrictions:
            if cls._check_dietary_compliance(recipe, dietary_restrictions):
                match_percentage = min(100, match_percentage + cls.WEIGHT_PREFERENCE_BOOST)
        
        # Determine if can be made with substitutions
        can_substitute = (
            len(missing_ingredients) <= 2 and
            not critical_missing and
            match_percentage >= 60
        )
        
        return {
            "match_percentage": round(match_percentage, 1),
            "matched": matched_ingredients,
            "missing": missing_ingredients,
            "can_substitute": can_substitute
        }
    
    @staticmethod
    def _find_exact_match(target: str, candidates: List[str]) -> bool:
        """Check for exact match (case-insensitive)"""
        target_lower = target.lower().strip()
        return any(target_lower == c.lower().strip() for c in candidates)
    
    @staticmethod
    def _check_critical_ingredients(recipe: Recipe, missing: List[str]) -> bool:
        """
        Check if any critical ingredients are missing
        Critical = main protein, base ingredients
        """
        critical_keywords = [
            "chicken", "beef", "pork", "fish", "tofu",
            "flour", "rice", "pasta", "bread"
        ]
        
        for missing_ing in missing:
            ing_lower = missing_ing.lower()
            if any(keyword in ing_lower for keyword in critical_keywords):
                return True
        
        return False
    
    @staticmethod
    def _check_dietary_compliance(
        recipe: Recipe,
        restrictions: List[str]
    ) -> bool:
        """
        Check if recipe complies with dietary restrictions
        
        Args:
            recipe: Recipe to check
            restrictions: List of dietary restrictions
            
        Returns:
            True if recipe is compliant, False otherwise
        """
        if not restrictions:
            return True
        
        recipe_tags = [tag.lower() for tag in recipe.dietary_tags]
        
        for restriction in restrictions:
            restriction_lower = restriction.lower().strip()
            
            # Recipe must have the dietary tag to be compliant
            if restriction_lower not in recipe_tags:
                return False
        
        return True
    
    @classmethod
    def rank_by_user_preferences(
        cls,
        matches: List[RecipeMatch],
        favorite_cuisines: List[str] = None,
        skill_level: str = "beginner"
    ) -> List[RecipeMatch]:
        """
        Re-rank matches based on user preferences
        
        Args:
            matches: Initial recipe matches
            favorite_cuisines: User's favorite cuisine types
            skill_level: User's cooking skill level
            
        Returns:
            Re-ranked recipe matches
        """
        for match in matches:
            boost = 0.0
            
            # Cuisine preference boost
            if favorite_cuisines and match.recipe.cuisine_type:
                if match.recipe.cuisine_type.lower() in [c.lower() for c in favorite_cuisines]:
                    boost += 5.0
            
            # Skill level matching
            skill_difficulty_map = {
                "beginner": "easy",
                "intermediate": "medium",
                "advanced": "hard"
            }
            
            if match.recipe.difficulty == skill_difficulty_map.get(skill_level):
                boost += 3.0
            
            # Apply boost
            match.match_percentage = min(100, match.match_percentage + boost)
        
        # Re-sort
        matches.sort(key=lambda x: x.match_percentage, reverse=True)
        
        return matches


# Global matcher instance
recipe_matcher = RecipeMatcher()

