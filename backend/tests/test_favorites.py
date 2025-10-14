"""
Tests for favorites and ratings endpoints
"""


def test_add_favorite(client):
    """Test adding a recipe to favorites"""
    response = client.post(
        "/api/v1/favorites/",
        json={
            "recipe_id": "recipe-123",
            "user_id": "user-456"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "message" in data


def test_get_user_favorites(client):
    """Test retrieving user favorites"""
    # First add a favorite
    client.post(
        "/api/v1/favorites/",
        json={
            "recipe_id": "recipe-123",
            "user_id": "user-test"
        }
    )
    
    # Then retrieve
    response = client.get("/api/v1/favorites/user-test")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "favorites" in data
    assert isinstance(data["favorites"], list)


def test_remove_favorite(client):
    """Test removing a recipe from favorites"""
    # First add
    client.post(
        "/api/v1/favorites/",
        json={
            "recipe_id": "recipe-to-remove",
            "user_id": "user-test-2"
        }
    )
    
    # Then remove
    response = client.request(
        "DELETE",
        "/api/v1/favorites/",
        json={
            "recipe_id": "recipe-to-remove",
            "user_id": "user-test-2"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_rate_recipe(client):
    """Test rating a recipe"""
    response = client.post(
        "/api/v1/favorites/ratings",
        json={
            "recipe_id": "recipe-789",
            "user_id": "user-rater",
            "rating": 5,
            "review": "Delicious!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "average_rating" in data
    assert "total_ratings" in data


def test_rate_recipe_invalid_rating(client):
    """Test rating with invalid value"""
    response = client.post(
        "/api/v1/favorites/ratings",
        json={
            "recipe_id": "recipe-999",
            "user_id": "user-bad",
            "rating": 6  # Invalid: should be 1-5
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_get_recipe_ratings(client):
    """Test getting all ratings for a recipe"""
    # Add a rating first
    client.post(
        "/api/v1/favorites/ratings",
        json={
            "recipe_id": "recipe-ratings-test",
            "user_id": "user-1",
            "rating": 4
        }
    )
    
    # Get ratings
    response = client.get("/api/v1/favorites/ratings/recipe-ratings-test")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "average_rating" in data
    assert "total_ratings" in data
    assert "ratings" in data

