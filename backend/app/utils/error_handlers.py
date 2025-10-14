"""
Custom Exception Handlers
Centralized error handling for the application
"""

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from typing import Optional


class AppException(Exception):
    """Base exception for application errors"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[dict] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ImageProcessingError(AppException):
    """Raised when image processing fails"""
    
    def __init__(self, message: str = "Failed to process image", details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class IngredientRecognitionError(AppException):
    """Raised when ingredient recognition fails"""
    
    def __init__(self, message: str = "Failed to recognize ingredients", details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class RecipeNotFoundError(AppException):
    """Raised when recipe is not found"""
    
    def __init__(self, recipe_id: str):
        super().__init__(
            message=f"Recipe with ID '{recipe_id}' not found",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"recipe_id": recipe_id}
        )


class ExternalAPIError(AppException):
    """Raised when external API call fails"""
    
    def __init__(self, service: str, message: str, details: Optional[dict] = None):
        super().__init__(
            message=f"{service} API error: {message}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details={"service": service, **(details or {})}
        )


class ValidationError(AppException):
    """Raised when input validation fails"""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom application exceptions"""
    logger.error(f"AppException: {exc.message} | Details: {exc.details}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "message": exc.message,
                "details": exc.details
            }
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTP exceptions"""
    logger.warning(f"HTTPException: {exc.detail} | Status: {exc.status_code}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "message": exc.detail,
                "status_code": exc.status_code
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other exceptions"""
    logger.exception(f"Unhandled exception: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "message": "An unexpected error occurred. Please try again later.",
                "type": type(exc).__name__
            }
        }
    )

