# FastAPI Learning Project — Start Here (for AI Agents)

This is a FastAPI project for learning. The goal is to learn FastAPI and Python
in the right way: a real database, tests, Docker, and the habits that real
projects need. **The app is a blog API** — see the ontology below.

This file sends you to the right place in [`.ai/`](.ai/README.md). Read only the
section below that you need. Do not read this whole file. Do not read every
context file.

---

## 0. BE SHORT

- **Give the answer first.** Add more details after it, or not at all.
- **Write each fact in one place only.** If another file already says it, add a
  link. Do not write it again.
- **Delete any sentence that is not needed.**
- **Use tables and lists** when you write about a group of things.
- **No introduction and no summary at the end.**
- **Say what you lose and what you win.** Do not try to sell the idea.

These rules are for documentation, tickets, commit messages, code comments and
replies.

---

## 1. THIS IS A LEARNING PROJECT

The owner is learning FastAPI and Python. So the agent must work like this:

- **Explain each new idea** in one or two sentences the first time you use it
  (for example a dependency with `Depends`, an `APIRouter`, a Pydantic schema,
  a SQLAlchemy session). Add a link to the official docs page.
- **Use the built-in way first**, not a clever or shorter way. Use `Depends`
  before writing your own middleware. Use Pydantic validation before checking
  data by hand. Use `response_model` before building dicts by hand.
- **Do not add a library just to skip learning something.** Ask first.
- **Use simple English (B1 level).** Short sentences. The owner is not a native
  speaker. This is also true for every document you write. If the owner writes
  in Ukrainian, reply in Ukrainian.

---

## 2. ONTOLOGY (THE DOMAIN MODEL)

The domain model is in [`.ai/context/ontology.md`](.ai/context/ontology.md).

- **Take names from the ontology.** Model names, router names and URL paths use
  its words.
- **A new idea in the domain means you update `ontology.md`** in the same
  change.
- **Invariants (I-n) are strict rules, not wishes.** If the code breaks one,
  it is a bug.

---

## 3. WHICH MODE TO USE

| Mode | File | Use it when | Read |
| :--- | :--- | :--- | :--- |
| **implement** | [`.ai/router/implement.md`](.ai/router/implement.md) | You build what a ticket describes | The ticket, [`conventions.md`](.ai/context/conventions.md), [`architecture.md`](.ai/context/architecture.md), [`stack.md`](.ai/context/stack.md), [`testing.md`](.ai/context/testing.md) |
| **review** | [`.ai/router/review.md`](.ai/router/review.md) | You check a change before it is committed | The diff, the ticket, [`conventions.md`](.ai/context/conventions.md), the invariants |

For everything else — answering a question, finding a bug, writing a ticket —
you do not need a mode file. Read [`context/INDEX.md`](.ai/context/INDEX.md),
then read only what the question needs. Answering a question does not change
any file.

---

## 4. TRACKING THE WORK

- **Planned work:** [`.ai/backlog/INDEX.md`](.ai/backlog/INDEX.md)
- **Finished work:** [`.ai/archive/INDEX.md`](.ai/archive/INDEX.md), each with
  a short note about the result
- **Template for a new ticket:** [`.ai/backlog/TEMPLATE.md`](.ai/backlog/TEMPLATE.md)

All work needs a ticket. No ticket → write one, or say that the request is not
in the backlog. Do not quietly do more than the ticket asks.

A ticket is finished only when every point of the Definition of Done in
[`conventions.md`](.ai/context/conventions.md) is true. Then move it to the
archive.

---

## 5. USING TOOLS

All the details: [`.ai/context/tools.md`](.ai/context/tools.md). Permissions
that the computer enforces: [`.claude/settings.json`](.claude/settings.json).

**Check your work** — run the command. Do not guess if it will pass. Tests
need the database and `JWT_SECRET` in `.env` (see
[`testing.md`](.ai/context/testing.md)).

```bash
venv1/bin/pytest
venv1/bin/ruff check .
venv1/bin/ruff format --check .
```

**Strict rules**

1. Never read `.env`. Read `.env.example` instead.
2. Never run `docker compose down -v`, `DROP TABLE`, `rm -rf` or
   `git push --force` if nobody asked you to.
3. Never commit or push if nobody asked you to.
4. Never add a dependency (a new package) without asking first.
5. Never write files outside the project folder.
6. Tell the truth about what happened. If a command fails, show its output.

---

## 6. WHERE WE ARE NOW

`TASK-001` – `TASK-006`, `TASK-008` and `TASK-009` are finished: FastAPI with
PostgreSQL in Docker, CRUD for Posts and Users, Argon2 passwords,
`APIRouter`s, pytest + ruff, login with JWT access tokens (only the User can
change their own account), Alembic migrations, Likes (many-to-many User ↔
Post), and pagination, search and filters on the lists. **Posts
have no author and are not protected.** The next ticket is `TASK-007`.
