"""
Tests for recipe endpoints
"""

import pytest


def test_search_recipes(client, sample_ingredients):
    """Test recipe search endpoint"""
    response = client.post(
        "/api/v1/recipes/search",
        json={
            "ingredients": sample_ingredients,
            "limit": 10
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "recipes" in data
    assert "total_found" in data
    assert isinstance(data["recipes"], list)


def test_search_recipes_with_dietary_restrictions(client, sample_ingredients):
    """Test recipe search with dietary restrictions"""
    response = client.post(
        "/api/v1/recipes/search",
        json={
            "ingredients": sample_ingredients,
            "dietary_restrictions": ["vegetarian"],
            "limit": 5
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    # All returned recipes should have vegetarian tag
    for recipe_match in data["recipes"]:
        assert "vegetarian" in recipe_match["recipe"]["dietary_tags"]


def test_search_recipes_invalid_ingredients(client):
    """Test recipe search with empty ingredients"""
    response = client.post(
        "/api/v1/recipes/search",
        json={
            "ingredients": [],
            "limit": 10
        }
    )
    
    assert response.status_code == 400


def test_list_recipes(client):
    """Test listing all recipes"""
    response = client.get("/api/v1/recipes/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "recipes" in data
    assert "total" in data
    assert len(data["recipes"]) > 0


def test_list_recipes_with_pagination(client):
    """Test recipe pagination"""
    response = client.get("/api/v1/recipes/?page=1&page_size=5")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["recipes"]) <= 5
    assert data["page"] == 1
    assert data["page_size"] == 5


def test_list_recipes_with_cuisine_filter(client):
    """Test filtering recipes by cuisine"""
    response = client.get("/api/v1/recipes/?cuisine=Italian")
    
    assert response.status_code == 200
    data = response.json()
    
    # All returned recipes should be Italian
    for recipe in data["recipes"]:
        assert recipe["cuisine_type"] == "Italian"


def test_get_recipe_detail(client):
    """Test getting recipe detail by index"""
    response = client.get("/api/v1/recipes/0")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "recipe" in data
    assert "title" in data["recipe"]
    assert "ingredients" in data["recipe"]
    assert "instructions" in data["recipe"]


def test_get_recipe_detail_not_found(client):
    """Test getting non-existent recipe"""
    response = client.get("/api/v1/recipes/99999")
    
    assert response.status_code == 404


def test_filter_by_nutrition(client):
    """Test filtering recipes by nutritional values"""
    response = client.get("/api/v1/recipes/filter/by-nutrition?max_calories=500&min_protein=20")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "recipes" in data
    
    # Check nutritional constraints
    for recipe in data["recipes"]:
        if recipe["nutrition"]:
            if recipe["nutrition"]["calories"]:
                assert recipe["nutrition"]["calories"] <= 500
            if recipe["nutrition"]["protein"]:
                assert recipe["nutrition"]["protein"] >= 20

