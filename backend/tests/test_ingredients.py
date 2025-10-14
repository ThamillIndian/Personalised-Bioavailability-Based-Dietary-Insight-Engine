"""
Tests for ingredient endpoints
"""

import io
import pytest


def test_recognize_text_ingredients(client):
    """Test text-based ingredient recognition"""
    response = client.post(
        "/api/v1/ingredients/recognize-text",
        data={"ingredients_text": "tomato, onion, garlic, chicken"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "ingredients" in data
    assert len(data["ingredients"]) == 4


def test_recognize_text_ingredients_newline_separated(client):
    """Test text recognition with newline-separated ingredients"""
    ingredients_text = "tomato\nonion\ngarlic\nchicken"
    
    response = client.post(
        "/api/v1/ingredients/recognize-text",
        data={"ingredients_text": ingredients_text}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["ingredients"]) == 4


def test_ingredient_substitutions(client):
    """Test getting ingredient substitutions"""
    response = client.post(
        "/api/v1/ingredients/substitutions",
        json={
            "ingredient": "butter",
            "context": "baking"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert data["original_ingredient"] == "butter"
    assert "substitutions" in data
    assert len(data["substitutions"]) > 0


def test_image_upload_invalid_file(client):
    """Test image upload with invalid file type"""
    # Create a text file pretending to be an image
    file_content = b"This is not an image"
    
    response = client.post(
        "/api/v1/ingredients/recognize-image",
        files={"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    )
    
    assert response.status_code == 400 or response.status_code == 422

