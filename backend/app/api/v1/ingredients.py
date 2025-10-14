"""
Ingredient Recognition Endpoints
Handle image uploads and ingredient recognition
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import time
from loguru import logger

from app.schemas.ingredient_schema import (
    IngredientRecognitionResponse,
    SubstitutionRequest,
    SubstitutionResponse
)
from app.services.gemini_service import gemini_service
from app.services.image_processor import image_processor
from app.services.substitution_service import substitution_service
from app.utils.validators import validate_image_file
from app.utils.error_handlers import ImageProcessingError, IngredientRecognitionError

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.post("/recognize-image", response_model=IngredientRecognitionResponse)
async def recognize_ingredients_from_image(
    file: UploadFile = File(..., description="Image file containing ingredients")
):
    """
    Recognize ingredients from uploaded image using Gemini Vision
    
    - **file**: Image file (JPEG, PNG, WebP)
    - Returns list of recognized ingredients with confidence scores
    """
    start_time = time.time()
    
    try:
        # Validate image file
        await validate_image_file(file)
        
        # Read file contents
        image_bytes = await file.read()
        
        # Process image
        processed_bytes, metadata = image_processor.validate_and_process_image(image_bytes)
        
        logger.info(f"Processing image: {metadata}")
        
        # Recognize ingredients using Gemini Vision
        ingredients = await gemini_service.recognize_ingredients_from_image(processed_bytes)
        
        processing_time = int((time.time() - start_time) * 1000)  # ms
        
        return IngredientRecognitionResponse(
            success=True,
            ingredients=ingredients,
            total_found=len(ingredients),
            processing_time_ms=processing_time,
            message=f"Successfully recognized {len(ingredients)} ingredients"
        )
        
    except (ImageProcessingError, IngredientRecognitionError) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error in ingredient recognition: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/substitutions", response_model=SubstitutionResponse)
async def get_ingredient_substitutions(request: SubstitutionRequest):
    """
    Get substitution suggestions for an ingredient
    
    - **ingredient**: Ingredient to substitute
    - **context**: Optional context (e.g., "baking", "vegan")
    - **recipe_type**: Optional recipe type for better suggestions
    """
    try:
        # Build context
        full_context = request.context or ""
        if request.recipe_type:
            full_context += f" {request.recipe_type}"
        
        # Get substitutions
        substitutions = await substitution_service.get_substitutions(
            request.ingredient,
            full_context.strip() if full_context else None
        )
        
        return SubstitutionResponse(
            success=True,
            original_ingredient=request.ingredient,
            substitutions=substitutions,
            context=full_context if full_context else None
        )
        
    except Exception as e:
        logger.error(f"Failed to get substitutions: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get substitutions: {str(e)}"
        )


@router.post("/recognize-text")
async def recognize_ingredients_from_text(
    ingredients_text: str = Form(..., description="Comma-separated ingredient list")
):
    """
    Parse ingredients from text input
    
    - **ingredients_text**: Comma or newline separated ingredients
    - Returns cleaned and parsed ingredient list
    """
    try:
        # Split by comma or newline
        if '\n' in ingredients_text:
            ingredients = [ing.strip() for ing in ingredients_text.split('\n')]
        else:
            ingredients = [ing.strip() for ing in ingredients_text.split(',')]
        
        # Clean up
        ingredients = [ing for ing in ingredients if ing]
        
        return {
            "success": True,
            "ingredients": ingredients,
            "total_found": len(ingredients)
        }
        
    except Exception as e:
        logger.error(f"Failed to parse ingredients: {e}")
        raise HTTPException(status_code=400, detail="Invalid ingredient text")

