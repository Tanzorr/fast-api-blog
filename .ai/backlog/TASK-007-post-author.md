# TASK-007 — Give every Post one or more authors; only its authors can change it

| Field | Value |
| :--- | :--- |
| **Status** | `planned` |
| **Priority** | P1 (main feature) |
| **Value driver** | `V-5` from [`../business/VALUE.md`](../business/VALUE.md) |
| **Needs first** | `TASK-005`, `TASK-006` |
| **Created** | 2026-10-21 · changed 2026-10-22: many authors, not one |

## Goal

A logged-in User creates a Post and becomes its first author. An author can
add other Users as co-authors and remove them. Everyone can read Posts and see
all their authors. Only an author can change or delete a Post (Q-2).

## What You Will Learn

| Idea | Docs |
| :--- | :--- |
| Many-to-many with `secondary=` (second time, after `TASK-008`) | [SQLAlchemy many-to-many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many) |
| Nested response schemas (a list of authors inside a Post) | [Body — nested models](https://fastapi.tiangolo.com/tutorial/body-nested-models/) |
| `selectinload` (avoid N+1 queries) | [Relationship loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html) |
| A dependency that checks the author (`get_own_post_or_403`) | [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) |

## Ontology Links

**Ideas used:** User, Post, Access token.
**Strict rules that must stay true:** `I-3` (an author in a Post response has
no password), `I-4`, `I-6`.
**New ideas:** **Author** — a User who writes a Post. Connection
`User --writes--> Post` (many Users, many Posts). New rule: every Post has at
least one author. Close Q-2. Update `ontology.md` in this ticket.

## Acceptance Criteria

- [ ] AC-1 — A migration adds the table `post_authors` (`user_id`, `post_id`,
      both together are the primary key). Old Posts without an author are
      handled as the decision D-1 says.
- [ ] AC-2 — `POST /posts` without a token → `401`. With a token → `201`, and
      the logged-in User is the only author.
- [ ] AC-3 — Every Post in a response has `authors`: a list of `id` and
      `email`. `GET /posts` uses a fixed number of queries (no N+1).
- [ ] AC-4 — `PUT` / `DELETE /posts/{post_id}`: no token → `401`; a User who
      is not an author → `403`; any author → `200` / `204`.
- [ ] AC-5 — `POST /posts/{post_id}/authors` with `{"user_id": N}`, by an
      author → `201`. Not an author → `403`. Unknown Post or User → `404`.
      The User is already an author → `409`.
- [ ] AC-6 — `DELETE /posts/{post_id}/authors/{user_id}`, by an author →
      `204`. Not an author → `403`. That User is not an author of the Post →
      `404`. Removing the last author → `409`.
- [ ] AC-7 — Deleting a User works as the decision D-2 says. No Post is left
      without an author.
- [ ] AC-8 — Tests cover every point above. `ontology.md` has Author, the
      connection, the new rule; Q-2 is closed. D-1 and D-2 are ADRs.

## Decisions to Make Before Coding

| # | Question | Options |
| :--- | :--- | :--- |
| D-1 | Posts that exist now have no author. What does the migration do? | (a) delete them — the dev database has only test data; (b) give them to one User chosen by hand; (c) keep them; nobody can change them (breaks the new rule) |
| D-2 | A User is deleted. They are the **only** author of a Post. What happens? | (a) the Post is deleted too; (b) deleting the User → `409` until they add a co-author or delete the Post |

## Not in This Ticket

| Not here | Ticket |
| :--- | :--- |
| An author leaves a Post by themself (remove yourself) | Works through AC-6, no extra endpoint |
| Invitations (the other User must agree first) | No ticket yet |
| Different roles (owner vs. co-author) | No ticket yet — all authors have the same rights |
| Pagination | A later ticket |
| `GET /users` shows emails, and now `authors` too | Q-4, no ticket yet |

## Notes

- The ticket first said "exactly one author" (one-to-many). On 2026-10-22 the
  owner asked for many authors per Post.
- The rule "at least one author" cannot be a simple database constraint. The
  code checks it (AC-6, AC-7), and tests prove it.
