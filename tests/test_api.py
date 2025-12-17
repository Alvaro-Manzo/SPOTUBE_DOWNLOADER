"""
Tests para la API Flask
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def client():
    """Cliente de prueba para Flask"""
    try:
        from api import app

        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client
    except ImportError:
        pytest.skip("Flask app not available")


def test_health_endpoint(client):
    """Test del endpoint de salud"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_download_endpoint_missing_url(client):
    """Test descarga sin URL"""
    response = client.post("/api/download", json={})
    assert response.status_code == 400


def test_download_endpoint_with_url(client):
    """Test descarga con URL válida"""
    response = client.post(
        "/api/download",
        json={
            "url": "https://open.spotify.com/playlist/test",
            "name": "test_playlist",
            "quality": "high",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "task_id" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
