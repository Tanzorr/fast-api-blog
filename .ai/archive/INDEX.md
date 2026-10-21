# Archive

Finished tickets. A ticket moves here from [`../backlog/`](../backlog/INDEX.md)
when every point of its Definition of Done is true
([`../context/conventions.md`](../context/conventions.md)).

## Finished Tickets

| ID | Title | Finished | Goal | Result |
| :--- | :--- | :--- | :--- | :--- |
| [TASK-004](TASK-004-pytest-ruff.md) | Add pytest and ruff, and write the tests we must have | 2026-10-21 | V-3 | 10 tests (T-1 – T-6) on a separate test database; ruff clean |
| [TASK-003](TASK-003-api-routers.md) | Split the endpoints into `APIRouter`s | 2026-10-21 | V-1 | `routers/posts.py`, `routers/users.py`, `schemas.py`, `security.py`; same URLs |
| [TASK-002](TASK-002-user-crud.md) | Add User CRUD with password hashing | 2026-10-20 | V-5 | `/users` CRUD; Argon2 hash; duplicate email → `409` |
| [TASK-001](TASK-001-post-crud.md) | Basic FastAPI + PostgreSQL project with Post CRUD | 2026-10-20 | V-1 | `/posts` CRUD; PostgreSQL 17 in Docker; settings from `.env` |

TASK-001 – TASK-003 were written after the work was done, when `.ai/` was
added. They were checked by hand, not with automated tests.

## How to Move a Ticket Here

1. Fill in the ticket's **Result** section: what was built, changes from the
   plan, strict rules checked, new tickets (with their IDs).
2. Set `Status: done`.
3. `git mv .ai/backlog/TASK-NNN-*.md .ai/archive/`
4. Remove its row from the backlog table; add a row here.

## Why We Keep This

Six months later, the useful question is usually not "what does this code do?"
— the code itself answers that. The useful question is "what did we want to
achieve, and what ideas did we say no to?" The result notes answer this.

**Never change** a ticket in the archive. If its decision was wrong, write a new
ticket that links to it.
