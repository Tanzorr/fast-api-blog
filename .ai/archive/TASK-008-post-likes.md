# TASK-008 — Let Users like Posts

| Field | Value |
| :--- | :--- |
| **Status** | `done` |
| **Priority** | P2 (quality) |
| **Value driver** | `V-4` from [`../business/VALUE.md`](../business/VALUE.md) |
| **Needs first** | `TASK-005`, `TASK-006` |
| **Created** | 2026-10-22 |

## Goal

A logged-in User can like a Post and take the like back. Everyone can see how
many likes a Post has. A User can see the list of Posts they liked.

## What You Will Learn

| Idea | Docs |
| :--- | :--- |
| Many-to-many with an association table (`secondary=`) | [SQLAlchemy many-to-many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many) |
| Composite primary key (two columns together are unique) | [SQLAlchemy `Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) |
| `ondelete="CASCADE"` on a foreign key | [SQLAlchemy cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html#using-foreign-key-on-delete-cascade-with-orm-relationships) |
| Count rows with `func.count` and `group_by` | [SQLAlchemy select](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#aggregate-functions-with-group-by-having) |

## Ontology Links

**Ideas used:** User, Post, Access token.
**Strict rules that must stay true:** `I-3` (no password in any response),
`I-4`.
**New ideas:** **Like** — a User marks a Post as liked. Connection
`User --likes--> Post` (many Users, many Posts). New rule: a User likes one
Post at most once. Update `ontology.md` in this ticket.

## Acceptance Criteria

- [x] AC-1 — A migration adds the table `post_likes` with `user_id` and
      `post_id`. The two columns together are the primary key.
- [x] AC-2 — `POST /posts/{post_id}/likes` with a token → `201`. Without a
      token → `401`. The Post does not exist → `404`. Already liked → `409`.
- [x] AC-3 — `DELETE /posts/{post_id}/likes` with a token → `204`. Not liked
      → `404`. Without a token → `401`.
- [x] AC-4 — Every Post in a response has `likes_count`. `GET /posts` uses a
      fixed number of queries (no N+1).
- [x] AC-5 — `GET /users/me/likes` with a token returns the Posts the User
      liked.
- [x] AC-6 — When a Post or a User is deleted, their likes are deleted too.
- [x] AC-7 — Tests cover every point above. `ontology.md` has Like, the
      connection and the new rule.

## Not in This Ticket

| Not here | Ticket |
| :--- | :--- |
| A list of the Users who liked a Post (shows emails, see Q-4) | No ticket yet |
| A rule like "a User may not like their own Post" (needs an author) | After `TASK-007`, if needed |
| Extra data on a like (for example the date) — needs an association object, not a plain table | No ticket yet |

## Notes

- `TASK-007` (one author per Post) is one-to-many. This ticket is the
  many-to-many example. They do not depend on each other.

---

## Result

**Finished on:** 2026-10-22
**What was built:** table `post_likes` (`models.py`) with
`PostModel.liked_by`, `UserModel.liked_posts` and `PostModel.likes_count`;
migration `8d0983066387_add_post_likes.py`; `POST` / `DELETE
/posts/{post_id}/likes`; `GET /users/me/likes`; `PostOut.likes_count`.
`tests/test_likes.py` — 13 tests (T-15 – T-20). All 35 tests pass; ruff is
clean; `alembic check` finds no difference.
**Changes from the plan:**
- AC-4 changed before coding: there is no `GET /posts/{post_id}` (T-5), so
  every Post response has `likes_count`.
- The count is a `column_property` with a subquery, not `func.count` +
  `group_by` in the endpoint. The endpoints stay short and `response_model`
  works without building dicts. `GET /posts` is one query (ADR-014).
- `POST /posts/{post_id}/likes` returns the Post (with the new
  `likes_count`).
- `ON DELETE CASCADE` was also checked with plain SQL, without the ORM.
**Strict rules checked:** I-6 new (T-16; primary key `(user_id, post_id)`),
I-3 (`/users/me/likes` returns `PostOut`, no User data), I-4 (Post schema not
changed).
**New tickets created:** none.
