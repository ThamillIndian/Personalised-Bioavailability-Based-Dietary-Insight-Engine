"""
Input Validators
Custom validation functions for request data
"""

from typing import List
from fastapi import UploadFile
from app.config import settings
from app.utils.error_handlers import ValidationError


async def validate_image_file(file: UploadFile) -> None:
    """
    Validate uploaded image file
    
    Args:
        file: Uploaded file from request
        
    Raises:
        ValidationError: If file is invalid
    """
    # Check content type
    if file.content_type not in settings.allowed_image_types_list:
        raise ValidationError(
            f"Invalid file type. Allowed types: {', '.join(settings.allowed_image_types_list)}",
            details={"provided_type": file.content_type}
        )
    
    # Read file to check size
    contents = await file.read()
    file_size = len(contents)
    
    if file_size > settings.max_image_size_bytes:
        raise ValidationError(
            f"File too large. Maximum size: {settings.MAX_IMAGE_SIZE_MB}MB",
            details={
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "max_size_mb": settings.MAX_IMAGE_SIZE_MB
            }
        )
    
    # Reset file pointer for further processing
    await file.seek(0)


def validate_ingredients(ingredients: List[str]) -> List[str]:
    """
    Validate and clean ingredient list
    
    Args:
        ingredients: List of ingredient names
        
    Returns:
        List[str]: Cleaned ingredient list
        
    Raises:
        ValidationError: If ingredients are invalid
    """
    if not ingredients:
        raise ValidationError("At least one ingredient is required")
    
    if len(ingredients) > 50:
        raise ValidationError(
            "Too many ingredients. Maximum: 50",
            details={"provided_count": len(ingredients)}
        )
    
    # Clean and deduplicate
    cleaned = []
    seen = set()
    
    for ingredient in ingredients:
        cleaned_ingredient = ingredient.strip().lower()
        
        if not cleaned_ingredient:
            continue
        
        if len(cleaned_ingredient) < 2:
            continue
        
        if len(cleaned_ingredient) > 100:
            raise ValidationError(
                f"Ingredient name too long: '{ingredient}'",
                details={"max_length": 100}
            )
        
        if cleaned_ingredient not in seen:
            cleaned.append(cleaned_ingredient)
            seen.add(cleaned_ingredient)
    
    if not cleaned:
        raise ValidationError("No valid ingredients provided after cleaning")
    
    return cleaned


def validate_dietary_restrictions(restrictions: List[str]) -> List[str]:
    """
    Validate dietary restrictions
    
    Args:
        restrictions: List of dietary restrictions
        
    Returns:
        List[str]: Validated restrictions
    """
    valid_restrictions = {
        "vegetarian", "vegan", "gluten-free", "dairy-free",
        "nut-free", "egg-free", "soy-free", "low-carb",
        "keto", "paleo", "pescatarian", "halal", "kosher"
    }
    
    validated = []
    for restriction in restrictions:
        cleaned = restriction.strip().lower()
        if cleaned in valid_restrictions:
            validated.append(cleaned)
    
    return validated


def validate_difficulty(difficulty: str) -> str:
    """
    Validate recipe difficulty level
    
    Args:
        difficulty: Difficulty level
        
    Returns:
        str: Validated difficulty
        
    Raises:
        ValidationError: If difficulty is invalid
    """
    valid_difficulties = {"easy", "medium", "hard"}
    cleaned = difficulty.strip().lower()
    
    if cleaned not in valid_difficulties:
        raise ValidationError(
            f"Invalid difficulty level. Must be one of: {', '.join(valid_difficulties)}",
            details={"provided": difficulty}
        )
    
    return cleaned

