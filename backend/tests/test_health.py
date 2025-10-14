"""
Tests for health check endpoint
"""

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "version" in data
    assert "timestamp" in data
    assert "database_connected" in data
    assert "services" in data


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "name" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "running"

