"""
Health Check Endpoint
System status and service availability
"""

from fastapi import APIRouter
from datetime import datetime
from loguru import logger

from app.schemas.response_schema import HealthCheckResponse
from app.config import settings
from app.database import check_database_connection
from app.services.gemini_service import gemini_service
from app.services.spoonacular_service import spoonacular_service

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint
    Returns system status and service availability
    """
    # Check database connection
    db_connected = await check_database_connection()
    
    # Check services
    gemini_available = gemini_service.model is not None
    spoonacular_available = (
        spoonacular_service.api_key and
        spoonacular_service.api_key != "your-spoonacular-api-key"
    )
    
    services = {
        "database": db_connected,
        "gemini_ai": gemini_available,
        "spoonacular": spoonacular_available
    }
    
    # Overall status
    all_services_healthy = all(services.values())
    status = "healthy" if all_services_healthy else "degraded"
    
    logger.info(f"Health check: {status} - Services: {services}")
    
    return HealthCheckResponse(
        status=status,
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow().isoformat(),
        database_connected=db_connected,
        services=services
    )

