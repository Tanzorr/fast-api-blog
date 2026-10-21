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

Two files are shared by all layers:

| File | What is in it |
| :--- | :--- |
| `database.py` | `Settings`, `engine`, `SessionLocal`, `Base`, `get_db()` |
| `security.py` | `password_hash` (Argon2). Later: tokens (`TASK-006`) |

## Project Files

```
main.py          Creates the app, creates the tables, includes the routers
database.py      Settings + database connection
models.py        SQLAlchemy models
schemas.py       Pydantic schemas
security.py      Password hashing
routers/         One APIRouter for each idea: posts.py, users.py
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

### ADR-003 — Settings from `pydantic-settings`, read only in `database.py`
**2026-10-20 · Accepted**
`Settings` checks types and fails with a clear error if a required variable is
missing. Other code imports `settings`; it never reads `os.environ`. Cost: one
dependency.

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
