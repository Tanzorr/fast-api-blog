# TASK-004 — Add pytest and ruff, and write the tests we must have

| Field | Value |
| :--- | :--- |
| **Status** | `planned` |
| **Priority** | P0 (nothing else can start) |
| **Value driver** | `V-3` from [`../business/VALUE.md`](../business/VALUE.md) |
| **Needs first** | — |
| **Created** | 2026-10-21 |

## Goal

One command shows if the API still works, and one command shows if the code is
clean. After this ticket, every other ticket can prove its result.

## What You Will Learn

| Idea | Docs |
| :--- | :--- |
| `TestClient` | [Testing](https://fastapi.tiangolo.com/tutorial/testing/) |
| `app.dependency_overrides` (test database) | [Testing dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/) |
| pytest fixtures | [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) |
| ruff | [ruff docs](https://docs.astral.sh/ruff/) |

## Ontology Links

**Ideas used:** User, Post.
**Strict rules that must stay true:** `I-1`, `I-2`, `I-3`, `I-4`.
**New ideas:** none.

## Acceptance Criteria

- [ ] AC-1 — `pytest` and `ruff` are in `requirements.txt` (ask first — new
      dependencies).
- [ ] AC-2 — `pyproject.toml` has pytest and ruff settings.
- [ ] AC-3 — Tests use a separate test database; the development data is
      never changed.
- [ ] AC-4 — Tests T-1 – T-6 from [`testing.md`](../context/testing.md) are
      written and pass. Their status there says `done`.
- [ ] AC-5 — `ruff check .` and `ruff format --check .` show no problems.

## Not in This Ticket

| Not here | Ticket |
| :--- | :--- |
| CI (GitHub Actions) | A later ticket |
| Migrations | `TASK-005` |
