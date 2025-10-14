"""
Supabase Database Connection
Handles all database operations and connection management
"""

from supabase import create_client, Client
from typing import Optional
from app.config import settings
from loguru import logger


class SupabaseClient:
    """Singleton Supabase client manager"""
    
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """
        Get or create Supabase client instance
        
        Returns:
            Client: Supabase client
        """
        if cls._instance is None:
            if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
                logger.warning("Supabase credentials not configured. Some features may be limited.")
                # Return a mock client for development
                return None
            
            try:
                cls._instance = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_KEY
                )
                logger.info("✅ Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Supabase client: {e}")
                return None
        
        return cls._instance
    
    @classmethod
    def reset_client(cls):
        """Reset the client instance (useful for testing)"""
        cls._instance = None


# Global database instance
db = SupabaseClient.get_client()


async def check_database_connection() -> bool:
    """
    Check if database connection is healthy
    
    Returns:
        bool: True if connected, False otherwise
    """
    if db is None:
        return False
    
    try:
        # Try a simple query to verify connection
        result = db.table("recipes").select("id").limit(1).execute()
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False

