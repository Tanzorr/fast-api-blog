# TASK-006 — Let a User log in and get a token; protect User changes

| Field | Value |
| :--- | :--- |
| **Status** | `planned` |
| **Priority** | P1 (main feature) |
| **Value driver** | `V-5` from [`../business/VALUE.md`](../business/VALUE.md) |
| **Needs first** | `TASK-004` |
| **Created** | 2026-10-21 |

## Goal

A User logs in with email and password and gets a token. Only that User can
change or delete their own account. Today anyone can change any User's
password (Q-1).

## What You Will Learn

| Idea | Docs |
| :--- | :--- |
| OAuth2 password flow, `OAuth2PasswordBearer` | [Security — first steps](https://fastapi.tiangolo.com/tutorial/security/first-steps/) |
| JWT tokens, `password_hash.verify()` | [OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) |
| A `get_current_user` dependency | [Get current user](https://fastapi.tiangolo.com/tutorial/security/get-current-user/) |

## Ontology Links

**Ideas used:** User, Visitor.
**Strict rules that must stay true:** `I-2`, `I-3`.
**New ideas:** a token (access token). Add it to `ontology.md`. New rule: only
the User themself can change or delete their account.

## Acceptance Criteria

- [ ] AC-1 — `POST /auth/login` with the right email and password returns a
      token; a wrong password or unknown email returns `401` with the same
      message.
- [ ] AC-2 — `GET /users/me` returns the logged-in User.
- [ ] AC-3 — `PUT` and `DELETE /users/{user_id}` without a token → `401`;
      with another User's token → `403`.
- [ ] AC-4 — The token secret comes from `.env` (`JWT_SECRET`), and
      `.env.example` lists it.
- [ ] AC-5 — Tests cover every point above. Q-1 is closed in `ontology.md`.

## Not in This Ticket

| Not here | Ticket |
| :--- | :--- |
| Refresh tokens, logout | A later ticket |
| Protecting Posts | `TASK-007` |
