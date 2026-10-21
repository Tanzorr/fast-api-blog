# TASK-007 — Give every Post an author; only the author can change it

| Field | Value |
| :--- | :--- |
| **Status** | `planned` |
| **Priority** | P1 (main feature) |
| **Value driver** | `V-5` from [`../business/VALUE.md`](../business/VALUE.md) |
| **Needs first** | `TASK-005`, `TASK-006` |
| **Created** | 2026-10-21 |

## Goal

A logged-in User creates Posts. Everyone can read them and see who wrote them.
Only the author can change or delete a Post (Q-2).

## What You Will Learn

| Idea | Docs |
| :--- | :--- |
| `ForeignKey` and `relationship()` | [SQLAlchemy relationships](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many) |
| Nested response schemas | [Body — nested models](https://fastapi.tiangolo.com/tutorial/body-nested-models/) |
| `selectinload` (avoid N+1 queries) | [Relationship loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html) |

## Ontology Links

**Ideas used:** User, Post.
**Strict rules that must stay true:** `I-3` (the author in a Post response has
no password), `I-4`.
**New ideas:** the connection User → Post. New rule: every Post has exactly one
author.

## Acceptance Criteria

- [ ] AC-1 — A migration adds `posts.author_id`. Old Posts without an author are
      handled (the ticket must say how before coding).
- [ ] AC-2 — `POST /posts` without a token → `401`; with a token, the author is
      the logged-in User.
- [ ] AC-3 — `GET /posts` shows each Post with its author's `id` and `email`,
      in a fixed number of queries.
- [ ] AC-4 — `PUT` / `DELETE` by another User → `403`.
- [ ] AC-5 — Tests cover every point above. Q-2 is closed in `ontology.md`.

## Not in This Ticket

| Not here | Ticket |
| :--- | :--- |
| Pagination | A later ticket |
| What happens to Posts when their User is deleted | Decide in this ticket, write an ADR |
