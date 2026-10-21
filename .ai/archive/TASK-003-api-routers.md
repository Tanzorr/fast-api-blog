# TASK-003 — Split the endpoints into `APIRouter`s

| Field | Value |
| :--- | :--- |
| **Status** | `done` |
| **Priority** | P2 |
| **Value driver** | V-1 |
| **Needs first** | TASK-002 |
| **Created** | 2026-10-21 |

## Goal

Each idea has its own file, so the project can grow. The URLs do not change.

## What You Will Learn

`APIRouter` with `prefix` and `tags`, `include_router`
([Bigger applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)).

## Acceptance Criteria

- [x] AC-1 — `routers/posts.py` and `routers/users.py` each have one router.
- [x] AC-2 — `main.py` only creates the app and includes the routers.
- [x] AC-3 — All URLs and status codes are the same as before.
- [x] AC-4 — `/docs` groups the endpoints by "posts" and "users".

---

## Result

**Finished on:** 2026-10-21
**What was built:** `routers/`, `schemas.py`, `security.py`, a short `main.py`.
**Changes from the plan:** added `get_post_or_404()`, like the one for users.
**Strict rules checked:** I-1, I-3 — by a manual script with `TestClient` for
every endpoint.
**New tickets created:** none.
