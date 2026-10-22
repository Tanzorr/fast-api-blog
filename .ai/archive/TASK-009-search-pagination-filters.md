# TASK-009 — Add search, filters and pagination to the lists

| Field | Value |
| :--- | :--- |
| **Status** | `done` |
| **Priority** | P2 (quality) |
| **Value driver** | `V-1` from [`../business/VALUE.md`](../business/VALUE.md) |
| **Needs first** | — |
| **Created** | 2026-10-22 |

## Goal

A client can get Posts page by page, find Posts by words in the title or
content, and filter them by date and by likes. `GET /users` is also returned
page by page. Today both lists return every row at once.

## What You Will Learn

| Idea | Docs |
| :--- | :--- |
| Query parameters with checks (`Query(ge=…, le=…)`) | [Query parameters and string validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/) |
| A Pydantic model for query parameters (`Annotated[Model, Query()]`) | [Query parameter models](https://fastapi.tiangolo.com/tutorial/query-param-models/) |
| One dependency used by two routers (`Depends(get_pagination)`) | [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) |
| `limit` / `offset`, `ilike`, `where` built step by step | [SQLAlchemy select](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html) |

## Ontology Links

**Ideas used:** Post, User, Like.
**Strict rules that must stay true:** `I-3`.
**New ideas:** none. Pagination and search are API ideas, not domain ideas.

## Acceptance Criteria

Pagination (`GET /posts` and `GET /users`):

- [x] AC-1 — `limit` (default 20, from 1 to 100) and `offset` (default 0,
      0 or more). A wrong value → `422`.
- [x] AC-2 — The order is fixed (by `id`), so two pages never show the same
      row.

Search and filters (`GET /posts` only):

- [x] AC-3 — `search=word` returns Posts with the word in the `title` or the
      `content`. Upper and lower case do not matter.
- [x] AC-4 — `created_after` and `created_before` (date and time) filter by
      `created_at`.
- [x] AC-5 — `min_likes=N` returns Posts with `N` likes or more.
- [x] AC-6 — All parameters work together. With no parameters, the result is
      the same as today (only the first 20).
- [x] AC-7 — `GET /posts` still uses one query (T-18).
- [x] AC-8 — Tests cover every point above, also wrong values. README shows
      the parameters.

## Not in This Ticket

| Not here | Ticket |
| :--- | :--- |
| Filter by author | After `TASK-007` |
| The total number of rows in the response (`{"items": …, "total": …}`) | No ticket yet — it changes the response shape |
| Sorting chosen by the client (`sort=-created_at`) | No ticket yet |
| Search in `GET /users` by email | No ticket — Q-4 (emails are private) |
| Full-text search (PostgreSQL `tsvector`) | No ticket yet |

## Notes

- **The response stays a plain list.** What we lose: the client does not know
  how many pages there are. What we win: old clients and tests do not break.
- **`offset` gets slow on very big tables.** Cursor pagination is faster, but
  harder. That is OK for a learning project.
- **The default `limit=20` changes today's behaviour:** `GET /posts` without
  parameters no longer returns everything. Add a `CHANGELOG.md` line.

---

## Result

**Finished on:** 2026-10-22
**What was built:** `get_pagination()` in `dependencies.py` (`limit` 1–100,
default 20; `offset` ≥ 0) used by `GET /posts` and `GET /users`;
`schemas.PostFilters` (query-parameter model) and
`routers/posts.filter_posts()` for `search`, `created_after`,
`created_before`, `min_likes`. `tests/test_lists.py` — 26 tests (T-21 –
T-25). All 61 tests pass; ruff is clean. ADR-015.
**Changes from the plan:**
- `search` uses `icontains(…, autoescape=True)`, not plain `ilike`: same
  `ILIKE` in PostgreSQL, but `%` and `_` in the search are not wildcards.
- `created_after` and `created_before` include the given time (`>=`, `<=`).
- `count_queries()` moved from `tests/test_likes.py` to `tests/conftest.py`,
  because two test files use it now.
- No migration: no table changed.
**Strict rules checked:** I-3 (`GET /users` still returns `UserOut`).
**New tickets created:** none.
