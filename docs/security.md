# CodePilot Security & User Isolation Architecture

CodePilot adheres to defense-in-depth principles across authentication, authorization, storage, and AI inference.

## 1. Authentication & Password Security
- **Password Hashing**: Utilizes bcrypt with automatic salted PBKDF2-HMAC-SHA256 fallback (100,000 iterations), protecting against GPU rainbow table attacks.
- **JWT Tokens**: Cryptographically signed HMAC-SHA256 tokens carrying user subject ID, role, and expiration timestamp.
- **Token Invalidation**: Session expiry with client-side cleanup and expiration checks on every protected endpoint.

## 2. Strict User Data Isolation
- **Backend Enforcement**: Never trusts client-provided user IDs. User identity is derived strictly from the verified JWT payload via the `get_current_user` FastAPI dependency.
- **SQL Queries**: Every query for code analyses, knowledge concepts, weekly plans, and vault items is filtered by `user_id == current_user.id`.
- **Verified via Automated Test**: `backend/tests/test_isolation.py` explicitly tests that User B querying User A's private vault ID returns a 404 Not Found error.

## 3. Role-Based Authorization (RBAC)
- Roles: `USER` and `ADMIN`.
- System telemetry and platform statistics (`/api/admin/stats`) require the `get_current_admin` dependency. Requests by users with role `USER` are rejected with `403 Forbidden`.
- Admin endpoints view platform aggregated volume (e.g. total analyses count), but never expose another user's private code submissions or notes.

## 4. File Storage & Path Traversal Mitigation
- Uploaded files are assigned random UUID filenames on disk (`uuid.uuid4() + sanitized_ext`).
- Client-provided filenames are stored strictly as display metadata in the database.
- Extensions are restricted to safe technical formats (`.pdf`, `.txt`, `.md`, `.png`, `.jpg`, `.jpeg`, `.webp`).
- File deletion verifies that the canonical absolute path starts within the configured `UPLOAD_DIR` to prevent arbitrary filesystem deletion.
