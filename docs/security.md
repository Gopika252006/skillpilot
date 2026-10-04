# CodePilot Security & User Isolation Architecture

CodePilot adheres to defense-in-depth principles across authentication, authorization, storage, and AI inference.

## 1. Authentication & Password Security
- **Password Hashing**: Utilizes bcrypt with automatic salted PBKDF2-HMAC-SHA256 fallback (100,000 iterations), protecting against GPU rainbow table attacks.
- **JWT Tokens**: Cryptographically signed HMAC-SHA256 tokens carrying user subject ID, role, and expiration timestamp.
- **Admin Privilege Escalation Prevention**: Public registration (`POST /api/auth/register`) strictly assigns `role = "USER"`. Any attempt by an external client to supply `role = "ADMIN"` is unconditionally ignored. Admin creation occurs exclusively via server-side bootstrap/seed functionality. Verified via automated regression test.

## 2. Strict User Data Isolation
- **Backend Enforcement**: Never trusts client-provided user IDs. User identity is derived strictly from the cryptographically verified JWT payload via the `get_current_user` FastAPI dependency.
- **SQL Queries**: Every query for code analyses, knowledge concepts, weekly plans, and vault items is filtered by `user_id == current_user.id`.
- **Verified via Automated Test**: `backend/tests/test_isolation.py` and `comprehensive_test.py` explicitly test that User B querying User A's private vault item ID or file returns a `404 Not Found` error.

## 3. Role-Based Authorization (RBAC)
- Roles: `USER` and `ADMIN`.
- System telemetry and platform statistics (`/api/admin/*`) require the `get_current_admin` dependency. Requests by users with role `USER` are rejected with `403 Forbidden`.
- Admin endpoints view platform aggregated volume (e.g. total analyses count), but never expose another user's private code submissions or notes.

## 4. Knowledge Vault File Storage & Streaming Security
- **No Public Static Mounts**: Public StaticFiles mounts for private vault files are strictly eliminated. Uploaded user materials are never exposed via unauthenticated paths like `/uploads/<filename>`.
- **Authenticated File Streaming**: Uploaded files can only be downloaded through `GET /api/vault/items/{item_id}/file`, which authenticates the requester, verifies user ownership, checks file presence, and guards against path traversal before streaming.
- **Internal Path Protection**: Internal filesystem paths (e.g. `C:\Users\...`) are never exposed in API schemas or JSON responses. Clients only receive sanitized display filenames and metadata.
- **Path Traversal Mitigation**: Uploaded files are assigned random UUID filenames on disk (`uuid.uuid4() + ext`). File streaming and deletion verify that canonical paths reside within `UPLOAD_DIR`.
- **File Extensions & Size Limits**: Extensions are restricted to safe technical formats (`.pdf`, `.txt`, `.md`, `.png`, `.jpg`, `.jpeg`, `.webp`), capped at 15MB.

## 5. Network & API Hardening
- **CORS Hardening**: Configured with explicit allowed origins (`http://localhost:5173`, `http://127.0.0.1:5173`, `http://localhost:3000`). Never allows wildcard `*` with credentials enabled.
- **Sanitized Error Responses**: Global exception handler logs full stack traces server-side while returning generic error messages to clients to prevent exposing internal infrastructure details.
- **Ad-Hoc AI Protection**: All study actions (`POST /api/vault/action`) require valid authentication to prevent unauthenticated resource exhaustion.
