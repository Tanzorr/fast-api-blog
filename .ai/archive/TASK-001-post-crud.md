# TASK-001 — Basic FastAPI + PostgreSQL project with Post CRUD

| Field | Value |
| :--- | :--- |
| **Status** | `done` |
| **Priority** | P0 |
| **Value driver** | V-1 |
| **Needs first** | — |
| **Created** | 2026-10-20 |

## Goal

Start the database with one command, start the API, and create, read, change
and delete Posts from `/docs`.

## What You Will Learn

Path operations, Pydantic schemas, `Depends`, `lifespan`
([FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)), SQLAlchemy 2.x
models and sessions.

## Acceptance Criteria

- [x] AC-1 — `docker compose up -d` starts PostgreSQL with a health check.
- [x] AC-2 — Settings come from `.env`; git ignores `.env`.
- [x] AC-3 — `GET/POST /posts`, `PUT/DELETE /posts/{post_id}` work; an unknown
      id returns `404`.

---

## Result

**Finished on:** 2026-10-20
**What was built:** `database.py` (`Settings`, engine, `get_db`), `models.py`
(`PostModel`), endpoints in `main.py`, `docker-compose.yml` with `db`.
**Changes from the plan:** tables are made with `create_all()`, not migrations
(ADR-005). `GET /posts/{post_id}` was not built.
**Strict rules checked:** I-4, by the column types (`String(255)`, `Text`, not
null) and Pydantic.
**New tickets created:** TASK-002.
