import pytest
import uuid

def test_user_data_isolation(client):
    # Register User A
    email_a = f"user_a_{uuid.uuid4().hex[:8]}@codepilot.dev"
    resp_a = client.post(
        "/api/auth/register",
        json={"email": email_a, "password": "Password123!", "full_name": "User A"}
    )
    assert resp_a.status_code == 200
    token_a = resp_a.json()["access_token"]

    # Register User B
    email_b = f"user_b_{uuid.uuid4().hex[:8]}@codepilot.dev"
    resp_b = client.post(
        "/api/auth/register",
        json={"email": email_b, "password": "Password123!", "full_name": "User B"}
    )
    assert resp_b.status_code == 200
    token_b = resp_b.json()["access_token"]

    # User A creates a private vault item
    item_resp = client.post(
        "/api/vault/items",
        headers={"Authorization": f"Bearer {token_a}"},
        json={
            "content_type": "note",
            "title": "User A Top Secret Distributed Arch",
            "content": "Confidential technical architecture for User A only.",
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
    assert list_b.status_code == 200
    titles_b = [item["title"] for item in list_b.json()]
    assert "User A Top Secret Distributed Arch" not in titles_b

    # Unauthenticated user cannot access User A's item
    no_auth_get = client.get(f"/api/vault/items/{item_id}")
    assert no_auth_get.status_code == 401

def test_vault_file_streaming_security(client):
    """
    CRITICAL SECURITY CHECK:
    Private files must NEVER be accessible publicly or by another user.
    Only the authenticated owner can stream the file.
    """
    # Register User A
    email_a = f"uploader_a_{uuid.uuid4().hex[:8]}@codepilot.dev"
    resp_a = client.post(
        "/api/auth/register",
        json={"email": email_a, "password": "Password123!", "full_name": "Uploader A"}
    )
    token_a = resp_a.json()["access_token"]

    # Register User B
    email_b = f"intruder_b_{uuid.uuid4().hex[:8]}@codepilot.dev"
    resp_b = client.post(
        "/api/auth/register",
        json={"email": email_b, "password": "Password123!", "full_name": "Intruder B"}
    )
    token_b = resp_b.json()["access_token"]

    # User A uploads a text file
    file_content = b"Confidential Design Document for System A"
    upload_resp = client.post(
        "/api/vault/upload",
        headers={"Authorization": f"Bearer {token_a}"},
        files={"file": ("design_spec.txt", file_content, "text/plain")},
        data={"topic": "System Design", "folder": "Internal"}
    )
    assert upload_resp.status_code == 200
    item_id = upload_resp.json()["id"]

    # Verify no raw filesystem path is exposed in API output
    assert "file_path" not in upload_resp.json()

    # User A (owner) can download via authenticated endpoint
    owner_dl = client.get(
        f"/api/vault/items/{item_id}/file",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert owner_dl.status_code == 200
    assert owner_dl.content == file_content

    # User B cannot download User A's file
    intruder_dl = client.get(
        f"/api/vault/items/{item_id}/file",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert intruder_dl.status_code == 404

    # Unauthenticated user cannot download the file
    unauth_dl = client.get(f"/api/vault/items/{item_id}/file")
    assert unauth_dl.status_code == 401

def test_vault_action_authentication_required(client):
    """Verify that ad-hoc study actions require authentication."""
    resp = client.post(
        "/api/vault/action",
        json={"action": "summarize", "content": "Sample content to summarize"}
    )
    assert resp.status_code == 401

def test_admin_authorization_restriction(client):
    # Regular user attempt
    user_email = f"regular_{uuid.uuid4().hex[:8]}@codepilot.dev"
    user_resp = client.post(
        "/api/auth/register",
        json={"email": user_email, "password": "Password123!", "full_name": "Regular User"}
    )
    user_token = user_resp.json()["access_token"]

    admin_access = client.get(
        "/api/admin/stats",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert admin_access.status_code == 403  # Forbidden for non-admin

    # Admin access using seeded admin in conftest
    admin_login = client.post(
        "/api/auth/login",
        json={"email": "admin@codepilot.dev", "password": "Admin1234!"}
    )
    assert admin_login.status_code == 200
    admin_token = admin_login.json()["access_token"]

    admin_success = client.get(
        "/api/admin/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert admin_success.status_code == 200
    assert admin_success.json()["total_users"] >= 1
