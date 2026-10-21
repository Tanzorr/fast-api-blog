# Business Value

Why this project exists. Every ticket in [`../backlog/`](../backlog/INDEX.md)
links to one goal (value driver) on this page.

## 1. The Problem

The owner wants to learn FastAPI and Python. Tutorials teach each piece alone.
They skip what a real API needs: a real database, migrations, tests,
authentication, settings from environment variables, and a setup that works the
same on every computer.

## 2. The Idea

**One small but real API, built the same way as real FastAPI projects.**
Every feature is a lesson. Every lesson comes with a test.

**The app is a blog API.** It is small, everybody knows how it works, and it has
the parts worth learning first: CRUD, validation, password hashing, login with
tokens, and a one-to-many connection (User → Post). The domain is in
[`../context/ontology.md`](../context/ontology.md).

## 3. Goals (Value Drivers)

| ID | Goal | How we reach it |
| :--- | :--- | :--- |
| **V-1** | Learn the FastAPI basics: path operations, Pydantic schemas, `Depends`, `APIRouter`, status codes, errors | The posts and users routers, from `TASK-001` on |
| **V-2** | Learn to write good, normal Python: type hints, modules, exceptions | Code that passes `ruff` and review |
| **V-3** | Learn the habits of real projects: tests, migrations, Docker, settings from env variables, small commits | `TASK-004`, `TASK-005`, [`../context/testing.md`](../context/testing.md) |
| **V-4** | A working API the owner can show to others and grow | The blog API on GitHub |
| **V-5** | Users can sign up, log in, and manage only their own Posts | `TASK-002`, `TASK-006`, `TASK-007` |

## 4. How We Know It Works

- **S-1** — After a fresh `git clone`, the README steps start the API with only
  Python and Docker on the computer.
- **S-2** — `pytest` and `ruff` pass on every commit (after `TASK-004`).
- **S-3** — The owner can explain, in their own words, every FastAPI feature the
  project uses.

## 5. What This Project Is Not

- **Not** a real production deployment. No gunicorn, nginx, HTTPS or CI until
  a ticket asks for them.
- **Not** a frontend project. The API docs page (`/docs`) is the only UI.
- **Not** async database code for now. Sync SQLAlchemy is easier to learn
  first (ADR-004).
