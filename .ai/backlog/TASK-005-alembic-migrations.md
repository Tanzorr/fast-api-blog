# TASK-005 — Replace `create_all()` with Alembic migrations

| Field | Value |
| :--- | :--- |
| **Status** | `planned` |
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

- [ ] AC-1 — Alembic is in `requirements.txt` (ask first).
- [ ] AC-2 — The first migration creates `posts` and `users` exactly as the
      models say.
- [ ] AC-3 — `create_all()` is removed from `main.py`.
- [ ] AC-4 — `alembic upgrade head` works on an empty database. The existing
      database is marked with `alembic stamp head`, not created again.
- [ ] AC-5 — `alembic check` finds no difference between models and database.
- [ ] AC-6 — ADR-005 is updated; `stack.md` lists the new commands.

## Not in This Ticket

| Not here | Ticket |
| :--- | :--- |
| New columns | `TASK-007` |
