import pytest
import uuid

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ai" in data

def test_login_demo_user(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "demo@codepilot.dev", "password": "Demo1234!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "demo@codepilot.dev"
    assert data["user"]["role"] == "USER"

def test_login_invalid_password(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "demo@codepilot.dev", "password": "WrongPassword!"}
    )
    assert response.status_code == 401

def test_register_and_get_profile(client):
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@codepilot.dev"
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

def test_admin_self_registration_is_blocked(client):
    """
    CRITICAL SECURITY REGRESSION:
    Public registration MUST NEVER allow elevating privileges to ADMIN.
    Even if client sends role='ADMIN', created account must strictly be 'USER'.
    """
    attacker_email = f"attacker_{uuid.uuid4().hex[:8]}@example.com"
    response = client.post(
        "/api/auth/register",
        json={
            "email": attacker_email,
            "password": "AttackerPass123!",
            "full_name": "Attacker Attempt",
            "role": "ADMIN"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "USER"

    # Confirm in backend /me
    token = data["access_token"]
    me_resp = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_resp.status_code == 200
    assert me_resp.json()["role"] == "USER"
