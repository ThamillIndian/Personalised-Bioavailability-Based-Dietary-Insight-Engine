"""
User Models
Models for user preferences, favorites, and ratings
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4


class UserPreferences(BaseModel):
    """User dietary preferences and restrictions"""
    user_id: UUID
    dietary_restrictions: List[str] = Field(default_factory=list)
    favorite_cuisines: List[str] = Field(default_factory=list)
    disliked_ingredients: List[str] = Field(default_factory=list)
    cooking_skill_level: str = "beginner"  # beginner, intermediate, advanced
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Favorite(BaseModel):
    """User favorite recipe"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: UUID
    recipe_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Rating(BaseModel):
    """Recipe rating by user"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: UUID
    recipe_id: UUID
    rating: int = Field(ge=1, le=5)  # 1-5 stars
    review: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

