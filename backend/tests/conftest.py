"""
Pytest configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Test client for API requests"""
    return TestClient(app)


@pytest.fixture
def sample_ingredients():
    """Sample ingredient list for testing"""
    return ["chicken", "tomato", "onion", "garlic", "rice"]


@pytest.fixture
def sample_image_bytes():
    """Sample image bytes for testing (1x1 white PNG)"""
    import io
    from PIL import Image
    
    img = Image.new('RGB', (100, 100), color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()

