"""
FastAPI Main Application
Smart Recipe Generator Backend
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import time

from app.config import settings
from app.utils.logger import setup_logging
from app.utils.error_handlers import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from app.middleware.cors import setup_cors

# Import routers
from app.api.v1 import health, ingredients, recipes, favorites, chat, nutrition

# Initialize logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    🍳 Smart Recipe Generator API
    
    An intelligent recipe suggestion system that:
    - Recognizes ingredients from images using AI
    - Matches recipes based on available ingredients
    - Provides substitution suggestions
    - Filters by dietary restrictions and preferences
    - Tracks favorites and ratings
    
    Built with FastAPI, Gemini AI, and Spoonacular.
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup CORS
setup_cors(app)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing"""
    start_time = time.time()
    
    # Log request
    logger.info(f"→ {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log response
    logger.info(
        f"← {request.method} {request.url.path} "
        f"[{response.status_code}] {duration:.3f}s"
    )
    
    # Add timing header
    response.headers["X-Process-Time"] = f"{duration:.3f}"
    
    return response


# Include routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(ingredients.router, prefix="/api/v1")
app.include_router(recipes.router, prefix="/api/v1")
app.include_router(favorites.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(nutrition.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health",
        "message": "🏴‍☠️ Welcome to Smart Recipe Generator API!"
    }


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info("=" * 60)
    
    # Log service availability
    from app.services.gemini_service import gemini_service
    from app.services.spoonacular_service import spoonacular_service
    
    if gemini_service.model:
        logger.info("✅ Gemini AI service ready")
    else:
        logger.warning("⚠️  Gemini AI service not configured")
    
    if spoonacular_service.api_key and spoonacular_service.api_key != "your-spoonacular-api-key":
        logger.info("✅ Spoonacular service ready")
    else:
        logger.warning("⚠️  Spoonacular service not configured")
    
    logger.info(f"📚 API Documentation: http://localhost:{settings.PORT}/docs")
    logger.info(f"🏥 Health Check: http://localhost:{settings.PORT}/api/v1/health")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("👋 Shutting down Smart Recipe Generator API")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

