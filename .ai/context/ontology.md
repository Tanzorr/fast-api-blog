# Ontology

The main description of the domain. This file is always correct about the
domain. It says what exists and how the ideas are connected. It says nothing
about FastAPI, tables or classes — that is in [`architecture.md`](architecture.md).

**Domain: a blog API.** Users have accounts and write Posts. Anyone can read
Posts.

---

## 1. Main Ideas

| Idea | Saved in the database | What it is in the domain |
| :--- | :--- | :--- |
| **User** | yes | A person with an account: an email and a password. A User logs in to get an access token. Later a User writes Posts (`TASK-007`). |
| **Post** | yes | An article: a title, the text (content), and the date it was created. |
| **Like** | yes | A User marks a Post as liked. Everyone sees how many likes a Post has. |
| **Visitor** | no | Anyone who calls the API without logging in. |
| **Access token** | no | A signed proof, given at login, that a request comes from one User. It stops working 30 minutes after login. |

## 2. Connections

```
User   --writes-->   Post   (one User, many Posts)  — planned, TASK-007
User   --likes-->    Post   (many Users, many Posts)
User   --gets-->     Access token   (at login; a User can have many at once)
```

When a Post or a User is deleted, its Likes are deleted too.

## 3. Strict Rules (Invariants)

Things that must always be true. If the code breaks one, it is a bug.

| # | Rule |
| :--- | :--- |
| I-1 | No two Users have the same email. |
| I-2 | A password is never saved as plain text. Only its Argon2 hash is saved. |
| I-3 | The API never returns a password or a password hash. |
| I-4 | Every Post has a title (255 characters or less) and content. |
| I-5 | Only the User themself can change or delete their account. |
| I-6 | A User likes one Post at most once. |

## 4. Open Questions

We write questions here; we do not answer them quietly. Each one becomes a
ticket when it becomes important.

- **Q-1** — Who may change or delete a User? **Closed by `TASK-006`:** only
  the User themself (I-5).
- **Q-2** — Who may change or delete a Post? Today: anyone. `TASK-007` answers
  it: only its author.
- **Q-3** — Is the email case-sensitive? Today `A@x.com` and `a@x.com` are two
  different Users. No ticket yet.
- **Q-4** — May a Visitor see the list of all Users and their emails
  (`GET /users`)? Today: yes. This shows private data. No ticket yet.
