import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ai" in data

def test_login_demo_user():
    response = client.post(
        "/api/auth/login",
        json={"email": "demo@codepilot.dev", "password": "Demo1234!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "demo@codepilot.dev"
    assert data["user"]["role"] == "USER"

def test_login_invalid_password():
    response = client.post(
        "/api/auth/login",
        json={"email": "demo@codepilot.dev", "password": "WrongPassword!"}
    )
    assert response.status_code == 401

def test_register_and_get_profile():
    unique_email = "testuser_unique@codepilot.dev"
    response = client.post(
        "/api/auth/register",
        json={
            "email": unique_email,
            "password": "Password123!",
            "full_name": "Test Engineer",
            "role": "USER"
        }
    )
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]

    # Verify protected /api/profile endpoint
    profile_resp = client.get(
        "/api/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert profile_resp.status_code == 200
    profile_data = profile_resp.json()
    assert profile_data["target_role"] == "Backend Software Engineer"
