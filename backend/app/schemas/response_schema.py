"""
Generic API response schemas
"""

from pydantic import BaseModel
from typing import Optional, Any, Dict


class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Generic error response"""
    success: bool = False
    error: Dict[str, Any]


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str
    database_connected: bool
    services: Dict[str, bool]

