# TASK-002 — Add User CRUD with password hashing

| Field | Value |
| :--- | :--- |
| **Status** | `done` |
| **Priority** | P1 |
| **Value driver** | V-5 |
| **Needs first** | TASK-001 |
| **Created** | 2026-10-20 |

## Goal

Create, read, change and delete Users. A password is never saved or returned
as plain text.

## What You Will Learn

Password hashing and salt ([Security — OAuth2 with JWT, hashing part](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#password-hashing)),
`EmailStr`, separate input and output schemas, unique constraints.

## Acceptance Criteria

- [x] AC-1 — `GET/POST /users`, `GET/PUT/DELETE /users/{user_id}`; unknown id
      → `404`.
- [x] AC-2 — The database keeps only the Argon2 hash (I-2).
- [x] AC-3 — Responses have `id`, `email`, `created_at` — no password (I-3).
- [x] AC-4 — A second User with the same email → `409` (I-1).
- [x] AC-5 — A bad email → `422`.

---

## Result

**Finished on:** 2026-10-20
**What was built:** `UserModel` (unique `email`), `User` / `UserOut` schemas,
`pwdlib[argon2]` in `requirements.txt`, five `/users` endpoints.
**Changes from the plan:** none.
**Strict rules checked:** I-1, I-2, I-3 — by a manual script with `TestClient`
(create, duplicate, get, update, delete). No automated tests (`TASK-004`).
**New tickets created:** TASK-006 (login; today anyone can change any User).
