import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_data_isolation():
    # Login as User A (demo user)
    resp_a = client.post(
        "/api/auth/login",
        json={"email": "demo@codepilot.dev", "password": "Demo1234!"}
    )
    token_a = resp_a.json()["access_token"]

    # Register User B
    resp_b = client.post(
        "/api/auth/register",
        json={
            "email": "user_b_isolation@codepilot.dev",
            "password": "Password123!",
            "full_name": "User B",
            "role": "USER"
        }
    )
    token_b = resp_b.json()["access_token"]

    # User A creates a private vault item
    item_resp = client.post(
        "/api/vault/items",
        headers={"Authorization": f"Bearer {token_a}"},
        json={
            "content_type": "note",
            "title": "User A Top Secret Note",
            "content": "Confidential technical architecture for User A.",
            "topic": "Security"
        }
    )
    assert item_resp.status_code == 200
    item_id = item_resp.json()["id"]

    # User B tries to access User A's private item by ID
    attempt_get = client.get(
        f"/api/vault/items/{item_id}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert attempt_get.status_code == 404  # Completely isolated, invisible to User B

    # User B queries their vault list - should NOT see User A's note
    list_b = client.get(
        "/api/vault/items",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    titles_b = [item["title"] for item in list_b.json()]
    assert "User A Top Secret Note" not in titles_b

def test_admin_authorization_restriction():
    # Login as regular user
    user_resp = client.post(
        "/api/auth/login",
        json={"email": "demo@codepilot.dev", "password": "Demo1234!"}
    )
    user_token = user_resp.json()["access_token"]

    # Attempt to access admin dashboard
    admin_access = client.get(
        "/api/admin/stats",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert admin_access.status_code == 403  # Forbidden

    # Login as Admin
    admin_resp = client.post(
        "/api/auth/login",
        json={"email": "admin@codepilot.dev", "password": "Admin1234!"}
    )
    admin_token = admin_resp.json()["access_token"]

    # Authorized admin access
    admin_success = client.get(
        "/api/admin/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert admin_success.status_code == 200
    assert admin_success.json()["total_users"] >= 2
