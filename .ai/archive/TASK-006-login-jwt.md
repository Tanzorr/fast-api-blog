# TASK-006 — Let a User log in and get a token; protect User changes

| Field | Value |
| :--- | :--- |
| **Status** | `done` |
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

- [x] AC-1 — `POST /auth/login` with the right email and password returns a
      token; a wrong password or unknown email returns `401` with the same
      message.
- [x] AC-2 — `GET /users/me` returns the logged-in User.
- [x] AC-3 — `PUT` and `DELETE /users/{user_id}` without a token → `401`;
      with another User's token → `403`.
- [x] AC-4 — The token secret comes from `.env` (`JWT_SECRET`), and
      `.env.example` lists it.
- [x] AC-5 — An expired token, a token with a wrong signature, and a token of a
      deleted User all return `401`.
- [x] AC-6 — The **Authorize** button in `/docs` works: log in there, then call
      `GET /users/me`.
- [x] AC-7 — Tests cover every point above. Q-1 is closed in `ontology.md`.

## Not in This Ticket

| Not here | Ticket |
| :--- | :--- |
| Refresh tokens, logout | A later ticket |
| Old tokens stop working after a password change | A later ticket (see "Costs") |
| Protecting Posts | `TASK-007` |
| Hiding `GET /users` from Visitors | Q-4, no ticket yet |

## Plan

### How it works

```
1. POST /auth/login  (form: username=<email>, password=<password>)
       │  find the User by email → password_hash.verify()
       ▼
2. Response: {"access_token": "<jwt>", "token_type": "bearer"}
       │  JWT payload: {"sub": "<user id>", "exp": <now + 30 min>}
       │  signed with JWT_SECRET (HS256)
       ▼
3. Next requests: header  Authorization: Bearer <jwt>
       │  get_current_user() checks the signature and "exp",
       │  then loads the User by id
       ▼
4. The endpoint gets the User, or the client gets 401
```

A JWT is a signed text. Anyone can read what is inside it, but nobody can
change it without the secret. So: **never put a password or other secrets in
the payload**.

### Decisions (write them as ADRs when you build)

| # | Decision | Why | Cost |
| :--- | :--- | :--- | :--- |
| ADR-009 | `PyJWT`, algorithm HS256 | The FastAPI docs use it; `python-jose` is not maintained. HS256 needs only one secret | One new dependency (**ask first**). HS256: every server that checks tokens must know the secret |
| ADR-010 | `sub` = the User **id**, not the email | The email can change (`PUT /users/{id}`); the id never changes | none |
| ADR-011 | Login uses `OAuth2PasswordRequestForm` (form data, field `username` = email) | It is the OAuth2 standard, so the **Authorize** button in `/docs` works | The field is called `username`, but it holds the email |
| ADR-012 | Token lives 30 minutes (`ACCESS_TOKEN_EXPIRE_MINUTES`) | A stolen token stops working soon | The User logs in again after 30 minutes (no refresh tokens yet) |
| ADR-003 (change) | Move `Settings` from `database.py` to a new `config.py` | JWT settings are not about the database | One more file; update ADR-003 and `stack.md` |

### Steps

Each step is small. Run the tests after each one.

1. **Ask to install `pyjwt`.** Add it to `requirements.txt`.
2. **Settings.** Create `config.py` with `Settings` (move it from
   `database.py`) and add:
   `jwt_secret: str` (required), `jwt_algorithm: str = "HS256"`,
   `access_token_expire_minutes: int = 30`.
   `database.py` imports `settings` from `config.py`.
   Add `JWT_SECRET` and `ACCESS_TOKEN_EXPIRE_MINUTES` to `.env.example`.
   Make a secret with `python -c "import secrets; print(secrets.token_hex(32))"`.
3. **Token functions in `security.py`.**
   - `create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str`
   - `decode_access_token(token: str) -> int` — returns the user id; raises an
     error for a bad or expired token (`jwt.InvalidTokenError`).
   - `DUMMY_HASH = password_hash.hash("dummy")` — see step 5.
4. **Schema.** `Token` in `schemas.py`: `access_token: str`,
   `token_type: str = "bearer"`.
5. **Login endpoint.** New `routers/auth.py`, prefix `/auth`, tag `auth`:
   `POST /auth/login` → `Token`.
   - Find the User by email.
   - If there is no User, still call `password_hash.verify(password, DUMMY_HASH)`.
     Then a wrong email and a wrong password take the same time, and an attacker
     cannot find out which emails exist (a *timing attack*).
   - Wrong email or wrong password → the same `401`
     `"Incorrect email or password"`, with the header
     `WWW-Authenticate: Bearer`.
   - Include the router in `main.py`.
6. **`get_current_user` dependency.** New `dependencies.py`:
   - `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")`
   - `get_current_user(token = Depends(oauth2_scheme), db = Depends(get_db)) -> UserModel`
   - Bad token, expired token, or the User does not exist any more → `401`.
7. **Protect users.** In `routers/users.py`:
   - `GET /users/me` → the current User. **Put it before `/{user_id}`**,
     or FastAPI tries to read `"me"` as an id and returns `422`.
   - `PUT` and `DELETE /users/{user_id}`: add `current_user = Depends(get_current_user)`.
     If `current_user.id != user_id` → `403`. A missing User is still `404`.
   - `POST /users` (sign up) stays open for everyone.
8. **Tests** (`tests/test_auth.py`). Add rows T-7 – T-14 to `testing.md`:

   | # | Behaviour |
   | :--- | :--- |
   | T-7 | The right email and password → `200` and a token that decodes to the User's id |
   | T-8 | A wrong password → `401` |
   | T-9 | An unknown email → `401` with the **same** message as T-8 |
   | T-10 | `GET /users/me` with a token → the User; without a token → `401` |
   | T-11 | An expired token (`expires_delta=timedelta(seconds=-1)`) → `401` |
   | T-12 | A token signed with another secret → `401` |
   | T-13 | A token of a deleted User → `401` |
   | T-14 | `PUT` / `DELETE` another User → `403`; your own → `200` / `204` |

9. **Documents.** Write ADR-009 – ADR-012 and change ADR-003 in
   `architecture.md`. In `ontology.md`: add the idea **Access token**, add the
   rule **I-5 — only the User themself can change or delete their account**,
   close Q-1, add Q-4. Update `stack.md` (new env variables, `PyJWT`), the
   README endpoint table, and `CHANGELOG.md`.

### Files

| File | Change |
| :--- | :--- |
| `requirements.txt` | + `pyjwt` |
| `config.py` | **new** — `Settings` with JWT settings |
| `database.py` | imports `settings` from `config.py` |
| `security.py` | + `create_access_token`, `decode_access_token`, `DUMMY_HASH` |
| `schemas.py` | + `Token` |
| `dependencies.py` | **new** — `oauth2_scheme`, `get_current_user` |
| `routers/auth.py` | **new** — `POST /auth/login` |
| `routers/users.py` | + `GET /users/me`; `PUT` / `DELETE` check the owner |
| `main.py` | includes `auth.router` |
| `.env.example` | + `JWT_SECRET`, `ACCESS_TOKEN_EXPIRE_MINUTES` |
| `tests/test_auth.py` | **new** — T-7 – T-14 |

### Costs and Risks

- **A token works until it expires**, even after logout or a password change.
  To stop this you need a token list in the database or a "token version" on
  the User. Not in this ticket.
- **If `JWT_SECRET` leaks, anyone can make tokens** for any User. It lives only
  in `.env`; never in code or in git.
- **Changing `JWT_SECRET` logs out everybody.** That is OK for development.

---

## Result

**Finished on:** 2026-10-21
**What was built:** `config.py`, `dependencies.py`, `routers/auth.py`
(`POST /auth/login`), `GET /users/me`, owner check `get_own_user_or_403()` on
`PUT` / `DELETE /users/{user_id}`, token functions in `security.py`, `Token`
schema. `tests/test_auth.py` — 12 tests (T-7 – T-14, AC-6). All 22 tests pass;
ruff is clean.
**Changes from the plan:**
- ADR numbers moved by one: `TASK-004` used ADR-009 for the test database. So
  PyJWT is ADR-010, `sub` = id is ADR-011, the login form is ADR-012, and the
  30-minute token is ADR-013.
- `jwt_secret` has `Field(min_length=32)`. PyJWT warns about shorter HS256
  keys, so the app does not start with a weak secret (also not with
  `change-me` from `.env.example`).
- `decode_access_token()` requires `sub` and `exp` in the token.
- AC-6 is tested through `/openapi.json` (the Authorize button uses the
  OAuth2 password flow with `tokenUrl` `/auth/login`). The click in a browser
  was not tested.
- Old tests T-3, T-5, T-6 now send a token for `PUT` / `DELETE`.
- Q-4 was already in `ontology.md`.
**Strict rules checked:** I-2 (T-2; login only calls `verify()`), I-3 (T-3 now
also checks `/users/me`; `Token` has no password), I-5 new (T-14).
**New tickets created:** none.
