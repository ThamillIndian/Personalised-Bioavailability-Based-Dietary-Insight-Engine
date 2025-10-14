"""
Recipe Endpoints
Search, filter, and retrieve recipes
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from uuid import UUID
from loguru import logger

from app.schemas.recipe_schema import (
    RecipeSearchRequest,
    RecipeSearchResponse,
    RecipeDetailResponse,
    RecipeListResponse
)
from app.models.recipe import Recipe
from app.services.recipe_matcher import recipe_matcher
from app.utils.validators import validate_ingredients, validate_dietary_restrictions
from app.utils.error_handlers import ValidationError, RecipeNotFoundError

router = APIRouter(prefix="/recipes", tags=["Recipes"])

# Import seed recipes
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from data.seed_recipes import SEED_RECIPES


@router.post("/search", response_model=RecipeSearchResponse)
async def search_recipes(request: RecipeSearchRequest):
    """
    🍳 Search Recipes - Interactive Form Interface
    
    **📝 How to Use This Form:**
    1. **Available Ingredients**: Enter the ingredients you have (required)
    2. **Dietary Restrictions**: Check boxes for any dietary needs (optional)
    3. **Preferred Cuisine**: Select from dropdown menu (optional)
    4. **Time Limits**: Set maximum prep/cook times in minutes (optional)
    5. **Difficulty**: Choose your cooking skill level (optional)
    6. **Results**: Specify how many recipes to show (1-50)
    
    **🎯 Form Features:**
    - ✅ **Text Input**: For ingredients list
    - ✅ **Checkboxes**: For multiple dietary restrictions
    - ✅ **Dropdowns**: For cuisine type and difficulty
    - ✅ **Number Inputs**: With min/max validation
    - ✅ **Help Text**: Clear descriptions for each field
    - ✅ **Examples**: Pre-filled sample data
    
    **📋 Available Options:**
    - **Dietary Restrictions**: vegetarian, vegan, gluten-free, dairy-free, nut-free, egg-free, soy-free, low-carb, keto, paleo, pescatarian, halal, kosher
    - **Cuisine Types**: Italian, Indian, Mexican, Japanese, Thai, Chinese, Greek, French, American, Mediterranean, Middle Eastern, Hawaiian
    - **Difficulty Levels**: Easy, Medium, Hard
    """
    try:
        # Validate ingredients
        cleaned_ingredients = validate_ingredients(request.ingredients)
        
        # Convert enum dietary restrictions to strings for validation
        dietary_restrictions_str = None
        if request.dietary_restrictions:
            dietary_restrictions_str = [restriction.value for restriction in request.dietary_restrictions]
            dietary_restrictions_str = validate_dietary_restrictions(dietary_restrictions_str)
        
        logger.info(f"Searching recipes with {len(cleaned_ingredients)} ingredients")
        
        # Get all recipes (from seed data or database)
        all_recipes = SEED_RECIPES
        
        # Filter by cuisine if specified
        if request.cuisine_type:
            all_recipes = [
                r for r in all_recipes
                if r.cuisine_type and r.cuisine_type.lower() == request.cuisine_type.value.lower()
            ]
        
        # Match recipes
        matched_recipes = recipe_matcher.match_recipes(
            recipes=all_recipes,
            user_ingredients=cleaned_ingredients,
            dietary_restrictions=dietary_restrictions_str,
            max_cook_time=request.max_cook_time,
            difficulty=request.difficulty.value if request.difficulty else None
        )
        
        # Limit results
        matched_recipes = matched_recipes[:request.limit]
        
        return RecipeSearchResponse(
            success=True,
            recipes=matched_recipes,
            total_found=len(matched_recipes),
            query_info={
                "ingredients_count": len(cleaned_ingredients),
                "dietary_restrictions": dietary_restrictions_str or [],
                "cuisine_type": request.cuisine_type.value if request.cuisine_type else None,
                "filters_applied": {
                    "max_prep_time": request.max_prep_time,
                    "max_cook_time": request.max_cook_time,
                    "difficulty": request.difficulty.value if request.difficulty else None
                }
            }
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Recipe search failed: {e}")
        raise HTTPException(status_code=500, detail="Recipe search failed")


@router.get("/{recipe_id}", response_model=RecipeDetailResponse)
async def get_recipe_detail(recipe_id: str):
    """
    Get detailed information for a specific recipe
    
    - **recipe_id**: Recipe ID or index
    """
    try:
        # Try to find recipe by ID or index
        all_recipes = SEED_RECIPES
        
        # Try as index first
        try:
            index = int(recipe_id)
            if 0 <= index < len(all_recipes):
                return RecipeDetailResponse(
                    success=True,
                    recipe=all_recipes[index]
                )
        except ValueError:
            pass
        
        # Try as UUID
        try:
            uuid_id = UUID(recipe_id)
            for recipe in all_recipes:
                if recipe.id == uuid_id:
                    return RecipeDetailResponse(
                        success=True,
                        recipe=recipe
                    )
        except ValueError:
            pass
        
        # Not found
        raise RecipeNotFoundError(recipe_id)
        
    except RecipeNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        logger.error(f"Failed to get recipe detail: {e}")
        raise HTTPException(status_code=500, detail="Failed to get recipe")


@router.get("/", response_model=RecipeListResponse)
async def list_recipes(
    page: int = Query(
        1, 
        ge=1, 
        description="📄 Page number for pagination",
        example=1
    ),
    page_size: int = Query(
        10, 
        ge=1, 
        le=50, 
        description="📊 Number of recipes per page (1-50)",
        example=10
    ),
    cuisine: Optional[str] = Query(
        None, 
        description="🌍 Filter by cuisine type. Available options: Italian, Indian, Mexican, Japanese, Thai, Chinese, Greek, French, American, Mediterranean, Middle Eastern, Hawaiian",
        example="Italian"
    ),
    difficulty: Optional[str] = Query(
        None, 
        description="🎯 Filter by difficulty level. Available options: easy, medium, hard",
        example="medium"
    ),
    dietary_tags: Optional[str] = Query(
        None, 
        description="🥗 Filter by dietary tags (comma-separated). Available options: vegetarian, vegan, gluten-free, dairy-free, nut-free, egg-free, soy-free, low-carb, keto, paleo, pescatarian, halal, kosher",
        example="vegetarian,gluten-free"
    )
):
    """
    📚 List All Recipes - Browse Recipe Collection
    
    **🎯 What This Endpoint Does:**
    Browse and filter through all available recipes in the database with pagination support.
    
    **📝 How to Use:**
    1. **Pagination**: Set page number and items per page
    2. **Filters**: Use any combination of cuisine, difficulty, or dietary tags
    3. **Browse**: Explore recipes without needing specific ingredients
    
    **🌍 Available Cuisine Types:**
    Italian, Indian, Mexican, Japanese, Thai, Chinese, Greek, French, American, Mediterranean, Middle Eastern, Hawaiian
    
    **🎯 Available Difficulty Levels:**
    - **easy**: Simple recipes for beginners
    - **medium**: Moderate complexity recipes  
    - **hard**: Advanced cooking techniques required
    
    **🥗 Available Dietary Tags:**
    vegetarian, vegan, gluten-free, dairy-free, nut-free, egg-free, soy-free, low-carb, keto, paleo, pescatarian, halal, kosher
    
    **💡 Example Usage:**
    - Browse all recipes: `/recipes/`
    - Italian recipes only: `/recipes/?cuisine=Italian`
    - Easy vegetarian recipes: `/recipes/?difficulty=easy&dietary_tags=vegetarian`
    - Gluten-free with pagination: `/recipes/?dietary_tags=gluten-free&page=2&page_size=5`
    """
    try:
        recipes = SEED_RECIPES
        
        # Apply filters
        if cuisine:
            recipes = [r for r in recipes if r.cuisine_type and r.cuisine_type.lower() == cuisine.lower()]
        
        if difficulty:
            recipes = [r for r in recipes if r.difficulty == difficulty.lower()]
        
        if dietary_tags:
            tags = [tag.strip().lower() for tag in dietary_tags.split(',')]
            recipes = [
                r for r in recipes
                if any(tag in [t.lower() for t in r.dietary_tags] for tag in tags)
            ]
        
        # Pagination
        total = len(recipes)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_recipes = recipes[start_idx:end_idx]
        
        return RecipeListResponse(
            success=True,
            recipes=paginated_recipes,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Failed to list recipes: {e}")
        raise HTTPException(status_code=500, detail="Failed to list recipes")


@router.get("/options")
async def get_recipe_options():
    """
    📋 Get Available Recipe Options
    
    Returns all available options for filtering recipes including cuisine types, 
    difficulty levels, and dietary restrictions.
    
    **🎯 Use this endpoint to:**
    - Get all available cuisine types
    - See all difficulty levels
    - View all dietary restriction options
    - Build dynamic filter interfaces
    """
    from app.schemas.recipe_schema import DietaryRestriction, CuisineType, DifficultyLevel
    
    return {
        "success": True,
        "options": {
            "cuisine_types": [cuisine.value for cuisine in CuisineType],
            "difficulty_levels": [difficulty.value for difficulty in DifficultyLevel],
            "dietary_restrictions": [restriction.value for restriction in DietaryRestriction],
            "total_recipes": len(SEED_RECIPES)
        },
        "usage": {
            "cuisine_examples": ["Italian", "Indian", "Mexican"],
            "difficulty_examples": ["easy", "medium", "hard"],
            "dietary_examples": ["vegetarian", "gluten-free", "vegan"]
        }
    }


@router.get("/filter/by-nutrition")
async def filter_by_nutrition(
    max_calories: Optional[int] = Query(None, description="Maximum calories"),
    min_protein: Optional[float] = Query(None, description="Minimum protein (g)"),
    max_carbs: Optional[float] = Query(None, description="Maximum carbs (g)"),
    max_fat: Optional[float] = Query(None, description="Maximum fat (g)")
):
    """
    Filter recipes by nutritional requirements
    
    - **max_calories**: Maximum calories per serving
    - **min_protein**: Minimum protein in grams
    - **max_carbs**: Maximum carbs in grams
    - **max_fat**: Maximum fat in grams
    """
    try:
        recipes = SEED_RECIPES
        filtered = []
        
        for recipe in recipes:
            if not recipe.nutrition:
                continue
            
            # Apply filters
            if max_calories and recipe.nutrition.calories and recipe.nutrition.calories > max_calories:
                continue
            if min_protein and recipe.nutrition.protein and recipe.nutrition.protein < min_protein:
                continue
            if max_carbs and recipe.nutrition.carbs and recipe.nutrition.carbs > max_carbs:
                continue
            if max_fat and recipe.nutrition.fat and recipe.nutrition.fat > max_fat:
                continue
            
            filtered.append(recipe)
        
        return {
            "success": True,
            "recipes": filtered,
            "total_found": len(filtered)
        }
        
    except Exception as e:
        logger.error(f"Nutrition filter failed: {e}")
        raise HTTPException(status_code=500, detail="Filter failed")

