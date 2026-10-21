# Changelog

Important changes. The newest changes are at the top. Each line names its
ticket, so you can find the ticket's acceptance criteria in
[`.ai/archive/`](.ai/archive/INDEX.md).

The format follows [Keep a Changelog](https://keepachangelog.com/). Adding a
line here is part of the Definition of Done in
[`.ai/context/conventions.md`](.ai/context/conventions.md).

## Unreleased

**Added**
- TASK-006: `POST /auth/login` returns an access token (JWT, 30 minutes).
  `GET /users/me` returns the logged-in User. The **Authorize** button in
  `/docs` works. New required setting: `JWT_SECRET` in `.env` (32 characters or
  more).
- TASK-004: Automated tests with pytest (`venv1/bin/pytest`) on a separate
  test database, and code checks with ruff. Settings are in `pyproject.toml`.
- The `.ai/` folder with project knowledge: business value, ontology, context
  files, modes for the agent, backlog and archive.
- `CLAUDE.md` start page, with rules for the agent in a learning project.
- `.claude/settings.json` permission rules: the agent can read most things,
  must ask before it changes things, and cannot read secrets or run commands
  that delete data.
- `README.md`, `.editorconfig`, `.gitattributes`.
- TASK-002: `/users` endpoints to create, list, get, change and delete Users.
  Passwords are saved as Argon2 hashes and never returned. A used email returns
  `409`.
- TASK-001: `/posts` endpoints to create, list, change and delete Posts.
  PostgreSQL 17 runs in Docker Compose. Settings come from `.env`.

**Changed**
- TASK-006: `PUT` and `DELETE /users/{user_id}` need a token: no token → `401`,
  another User's account → `403`. Before, anyone could change any User.
- TASK-003: Endpoints are split into `routers/posts.py` and `routers/users.py`.
  The URLs are the same. `/docs` groups them by topic.

---

## Rules for This File

- One line for each change that a user can see. Start it with the ticket:
  `TASK-004: …`.
- Write for a person who did not do the work.
- Sections: **Added**, **Changed**, **Fixed**, **Removed**.
