# Architecture

How the ontology becomes code. The ontology says what exists; this file says
where it lives in the code.

## Layers

```
HTTP                      routers/<name>.py
   │                      Short and simple. Read the input, call a helper or
   │                      service, return the result. Raise HTTPException.
   ▼
Schemas                   schemas.py
   │                      Pydantic models: what the API accepts and returns.
   ▼
Services (when needed)    services/<name>.py — create it when you first need it
   │                      Business actions that use several models or need
   │                      one transaction.
   ▼
Models                    models.py
                          SQLAlchemy tables, columns, constraints.
```

Rule: **a layer may use only the layers below it.** A model never imports a
router or a schema.

These files are shared by all layers:

| File | What is in it |
| :--- | :--- |
| `config.py` | `Settings` and `settings` — the only place that reads env variables (ADR-003) |
| `database.py` | `engine`, `SessionLocal`, `Base`, `get_db()` |
| `security.py` | `password_hash` (Argon2), `DUMMY_HASH`, `create_access_token()`, `decode_access_token()` |
| `dependencies.py` | `oauth2_scheme`, `get_current_user()` — used by routers with `Depends` |

## Project Files

```
main.py          Creates the app, creates the tables, includes the routers
config.py        Settings from env variables
database.py      Database connection
models.py        SQLAlchemy models
schemas.py       Pydantic schemas
security.py      Password hashing, access tokens
dependencies.py  get_current_user()
routers/         One APIRouter for each idea: auth.py, posts.py, users.py
tests/           pytest tests; conftest.py has the fixtures (testing.md)
pyproject.toml   pytest and ruff settings
```

## Where Each Idea Lives in Code

You must be able to find every ontology idea in the code.

| Ontology idea | Model | Schemas | Router |
| :--- | :--- | :--- | :--- |
| User | `models.py` → `UserModel` (table `users`) | `User` (input), `UserOut` (output, no password — I-3) | `routers/users.py`, prefix `/users` |
| Post | `models.py` → `PostModel` (table `posts`) | `Post` (input), `PostOut` (output) | `routers/posts.py`, prefix `/posts` |
| Visitor | Not saved. A request without a token | — | — |
| Access token | Not saved. A JWT made by `security.create_access_token()` | `Token` (output) | `routers/auth.py`, `POST /auth/login`; checked by `dependencies.get_current_user()` |

## Architecture Decision Records (ADRs)

An ADR is a short note about a decision: what we chose, why, and what it costs
us. Each one has a date. When a decision changes, we edit its ADR here.

### ADR-001 — PostgreSQL in Docker, not SQLite
**2026-10-20 · Accepted**
Real projects use PostgreSQL, and it works differently from SQLite in ways that
cause problems later (data types, constraints, many writes at the same time).
Docker gives the same database on every computer. Cost: you need Docker.

### ADR-002 — `requirements.txt` without exact versions
**2026-10-20 · Accepted — should change**
One file, one `pip install`. Cost: a new install next month can get different
versions and break. Fix it by pinning versions (`fastapi==0.148.0`); this needs
a ticket.

### ADR-003 — Settings from `pydantic-settings`, read only in `config.py`
**2026-10-20 · Accepted · changed 2026-10-21 (TASK-006)**
`Settings` checks types and fails with a clear error if a required variable is
missing or wrong (for example a `JWT_SECRET` shorter than 32 characters). Other
code imports `settings`; it never reads `os.environ`. Cost: one dependency.
Change: `Settings` moved from `database.py` to `config.py`, because the JWT
settings are not about the database. Cost: one more file.

### ADR-004 — Sync SQLAlchemy 2.x with `Mapped[]` types
**2026-10-20 · Accepted**
Sync code is easier to learn and to debug. FastAPI runs sync endpoints in a
thread pool, so they do not block the server. The `Mapped[...]` style gives
type hints for every column. Cost: async would handle more requests at the
same time; we do not need that now.

### ADR-005 — Tables are created with `create_all()` at startup, no migrations
**2026-10-20 · Accepted — temporary**
`Base.metadata.create_all()` in `lifespan` creates missing tables. It is the
fastest start. Cost: it **never changes a table that already exists**. A new
column in a model does nothing in the database. `TASK-005` replaces this with
Alembic.

### ADR-006 — Passwords hashed with Argon2 via `pwdlib`
**2026-10-20 · Accepted**
The FastAPI docs recommend `pwdlib`; `PasswordHash.recommended()` uses Argon2id
with a random salt for each hash. `passlib` is not maintained any more. Cost:
two dependencies (`pwdlib`, `argon2-cffi`).

### ADR-007 — Duplicate email → `409 Conflict`, found by the database
**2026-10-20 · Accepted**
The `users.email` column is `unique`. We catch `IntegrityError` on commit and
return `409`. If we checked with a `SELECT` first, two requests at the same time
could both pass. Cost: any other `IntegrityError` on users also becomes `409`.

### ADR-008 — One `APIRouter` per idea in `routers/`
**2026-10-21 · Accepted**
Each router has a `prefix` and `tags`. `main.py` only includes them. A new idea
means a new file and one `include_router` line. Cost: more files to open.

### ADR-009 — Tests use a second PostgreSQL database, emptied after each test
**2026-10-21 · Accepted**
Tests run on `<POSTGRES_DB>_test` on the same server, not on SQLite (ADR-001:
the same database as in real use). `conftest.py` creates it if it is missing.
After each test, `TRUNCATE … RESTART IDENTITY CASCADE` empties every table, so
ids start at 1 again. Cost: the Docker database must run for tests; `TRUNCATE`
is slower than rolling back a transaction, but easier to understand.

### ADR-010 — Access tokens are JWTs made with `PyJWT`, algorithm HS256
**2026-10-21 · Accepted**
The FastAPI docs use `PyJWT`; `python-jose` is not maintained. HS256 needs only
one secret, `JWT_SECRET` from `.env`. Cost: one dependency. Every server that
checks tokens must know the secret, and anyone with the secret can make a token
for any User. Changing the secret logs out everybody.

### ADR-011 — The token's `sub` is the User id, not the email
**2026-10-21 · Accepted**
The email can change (`PUT /users/{id}`); the id never changes. `sub` is saved
as a string, because the JWT standard wants a string. Cost: none.

### ADR-012 — Login uses `OAuth2PasswordRequestForm`
**2026-10-21 · Accepted**
`POST /auth/login` takes form data, the OAuth2 standard, so the **Authorize**
button in `/docs` works. Wrong email and wrong password give the same `401`,
and an unknown email is still checked against `DUMMY_HASH`, so the answer time
does not show which emails exist. Cost: the form field is called `username`,
but it holds the email.

### ADR-013 — An access token lives 30 minutes
**2026-10-21 · Accepted**
`ACCESS_TOKEN_EXPIRE_MINUTES`, default 30. A stolen token stops working soon.
Cost: the User logs in again after 30 minutes (no refresh tokens yet). A token
still works after a password change or after logout, until it expires.
