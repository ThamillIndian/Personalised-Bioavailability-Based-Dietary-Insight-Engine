"""
Favorites and Ratings Endpoints
User interactions with recipes
"""

from fastapi import APIRouter, HTTPException
from typing import List
from loguru import logger

from app.schemas.recipe_schema import (
    FavoriteRequest,
    RatingRequest,
    RatingResponse
)
from app.database import db

router = APIRouter(prefix="/favorites", tags=["Favorites & Ratings"])


# In-memory storage for demo (replace with Supabase in production)
FAVORITES_STORE = {}
RATINGS_STORE = {}


@router.post("/")
async def add_favorite(request: FavoriteRequest):
    """
    Add a recipe to user's favorites
    
    - **recipe_id**: Recipe ID to favorite
    - **user_id**: User ID or session ID
    """
    try:
        user_id = request.user_id
        recipe_id = request.recipe_id
        
        # Initialize user favorites if not exists
        if user_id not in FAVORITES_STORE:
            FAVORITES_STORE[user_id] = []
        
        # Add to favorites if not already there
        if recipe_id not in FAVORITES_STORE[user_id]:
            FAVORITES_STORE[user_id].append(recipe_id)
            logger.info(f"User {user_id} favorited recipe {recipe_id}")
            
            return {
                "success": True,
                "message": "Recipe added to favorites",
                "total_favorites": len(FAVORITES_STORE[user_id])
            }
        else:
            return {
                "success": True,
                "message": "Recipe already in favorites",
                "total_favorites": len(FAVORITES_STORE[user_id])
            }
            
    except Exception as e:
        logger.error(f"Failed to add favorite: {e}")
        raise HTTPException(status_code=500, detail="Failed to add favorite")


@router.get("/{user_id}")
async def get_user_favorites(user_id: str):
    """
    Get all favorites for a user
    
    - **user_id**: User ID or session ID
    """
    try:
        favorites = FAVORITES_STORE.get(user_id, [])
        
        return {
            "success": True,
            "user_id": user_id,
            "favorites": favorites,
            "total": len(favorites)
        }
        
    except Exception as e:
        logger.error(f"Failed to get favorites: {e}")
        raise HTTPException(status_code=500, detail="Failed to get favorites")


@router.delete("/")
async def remove_favorite(request: FavoriteRequest):
    """
    Remove a recipe from user's favorites
    
    - **recipe_id**: Recipe ID to unfavorite
    - **user_id**: User ID or session ID
    """
    try:
        user_id = request.user_id
        recipe_id = request.recipe_id
        
        if user_id in FAVORITES_STORE:
            if recipe_id in FAVORITES_STORE[user_id]:
                FAVORITES_STORE[user_id].remove(recipe_id)
                logger.info(f"User {user_id} unfavorited recipe {recipe_id}")
                
                return {
                    "success": True,
                    "message": "Recipe removed from favorites",
                    "total_favorites": len(FAVORITES_STORE[user_id])
                }
        
        return {
            "success": True,
            "message": "Recipe not in favorites",
            "total_favorites": len(FAVORITES_STORE.get(user_id, []))
        }
        
    except Exception as e:
        logger.error(f"Failed to remove favorite: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove favorite")


@router.post("/ratings", response_model=RatingResponse)
async def rate_recipe(request: RatingRequest):
    """
    Rate a recipe
    
    - **recipe_id**: Recipe ID to rate
    - **user_id**: User ID or session ID
    - **rating**: Rating from 1-5 stars
    - **review**: Optional text review
    """
    try:
        recipe_id = request.recipe_id
        user_id = request.user_id
        
        # Initialize recipe ratings if not exists
        if recipe_id not in RATINGS_STORE:
            RATINGS_STORE[recipe_id] = []
        
        # Add or update rating
        existing_rating = None
        for i, r in enumerate(RATINGS_STORE[recipe_id]):
            if r["user_id"] == user_id:
                existing_rating = i
                break
        
        rating_data = {
            "user_id": user_id,
            "rating": request.rating,
            "review": request.review
        }
        
        if existing_rating is not None:
            RATINGS_STORE[recipe_id][existing_rating] = rating_data
            message = "Rating updated"
        else:
            RATINGS_STORE[recipe_id].append(rating_data)
            message = "Rating added"
        
        # Calculate average rating
        ratings = [r["rating"] for r in RATINGS_STORE[recipe_id]]
        average = sum(ratings) / len(ratings) if ratings else 0
        
        logger.info(f"User {user_id} rated recipe {recipe_id}: {request.rating} stars")
        
        return RatingResponse(
            success=True,
            message=message,
            average_rating=round(average, 2),
            total_ratings=len(ratings)
        )
        
    except Exception as e:
        logger.error(f"Failed to rate recipe: {e}")
        raise HTTPException(status_code=500, detail="Failed to rate recipe")


@router.get("/ratings/{recipe_id}")
async def get_recipe_ratings(recipe_id: str):
    """
    Get all ratings for a recipe
    
    - **recipe_id**: Recipe ID
    """
    try:
        ratings = RATINGS_STORE.get(recipe_id, [])
        
        # Calculate average
        if ratings:
            average = sum(r["rating"] for r in ratings) / len(ratings)
        else:
            average = 0
        
        return {
            "success": True,
            "recipe_id": recipe_id,
            "average_rating": round(average, 2),
            "total_ratings": len(ratings),
            "ratings": ratings
        }
        
    except Exception as e:
        logger.error(f"Failed to get ratings: {e}")
        raise HTTPException(status_code=500, detail="Failed to get ratings")

