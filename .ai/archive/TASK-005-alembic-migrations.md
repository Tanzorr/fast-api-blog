# TASK-005 — Replace `create_all()` with Alembic migrations

| Field | Value |
| :--- | :--- |
| **Status** | `done` |
| **Priority** | P1 (main feature) |
| **Value driver** | `V-3` from [`../business/VALUE.md`](../business/VALUE.md) |
| **Needs first** | `TASK-004` |
| **Created** | 2026-10-21 |

## Goal

When a model changes, the database changes too, with a file in git that shows
what changed. Today a new column in a model does nothing (ADR-005).

## What You Will Learn

| Idea | Docs |
| :--- | :--- |
| What a migration is; `alembic init`, `revision --autogenerate`, `upgrade` | [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) |
| `env.py` with `Base.metadata` and settings from `config.py` | [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) |

## Ontology Links

**Ideas used:** User, Post.
**Strict rules that must stay true:** `I-1`, `I-4` (the unique and not-null
rules must be in the first migration).
**New ideas:** none.

## Acceptance Criteria

- [x] AC-1 — Alembic is in `requirements.txt` (ask first).
- [x] AC-2 — The first migration creates `posts` and `users` exactly as the
      models say.
- [x] AC-3 — `create_all()` is removed from `main.py`.
- [x] AC-4 — `alembic upgrade head` works on an empty database. The existing
      database is marked with `alembic stamp head`, not created again.
- [x] AC-5 — `alembic check` finds no difference between models and database.
- [x] AC-6 — ADR-005 is updated; `stack.md` lists the new commands.

## Not in This Ticket

| Not here | Ticket |
| :--- | :--- |
| New columns | `TASK-007` |

---

## Result

**Finished on:** 2026-10-22
**What was built:** Alembic 1.20 (`alembic.ini`, `alembic/env.py`). The first
migration `46c3acdcd5ee_create_posts_and_users.py` makes `posts` and `users`.
`create_all()` and `lifespan` are removed from `main.py`. The development
database was marked with `alembic stamp head`; `alembic check` finds no
difference. On an empty database, `upgrade head` → `check` → `downgrade base`
→ `upgrade head` all work. All 22 tests pass; ruff is clean.
**Changes from the plan:**
- `env.py` takes the URL from `config.settings`, so `alembic.ini` has no URL
  (ADR-003). A password with `%` would break the `.ini` file.
- `alembic.ini` runs `ruff format` and `ruff check --fix` on each new
  migration file.
- `pyproject.toml`: `known-third-party = ["alembic"]`. Without it, ruff sorts
  `from alembic import op` as our own code, because the folder has the same
  name.
- The first migration was made with `--autogenerate` against a new, empty
  database `fastapi_alembic_check` on the same server.
- The test database still uses `create_all()` (ADR-009). Tests do not run the
  migrations.
**Strict rules checked:** I-1 (`UniqueConstraint("email")` is in the
migration), I-4 (`title` `String(255)`, `nullable=False`; `content`
`nullable=False`).
**New tickets created:** none.
