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
| **User** | yes | A person with an account: an email and a password. Later a User logs in and writes Posts (`TASK-006`, `TASK-007`). |
| **Post** | yes | An article: a title, the text (content), and the date it was created. |
| **Visitor** | no | Anyone who calls the API without logging in. |

## 2. Connections

```
User   --writes-->   Post   (one User, many Posts)  — planned, TASK-007
```

Today Posts and Users are not connected.

## 3. Strict Rules (Invariants)

Things that must always be true. If the code breaks one, it is a bug.

| # | Rule |
| :--- | :--- |
| I-1 | No two Users have the same email. |
| I-2 | A password is never saved as plain text. Only its Argon2 hash is saved. |
| I-3 | The API never returns a password or a password hash. |
| I-4 | Every Post has a title (255 characters or less) and content. |

## 4. Open Questions

We write questions here; we do not answer them quietly. Each one becomes a
ticket when it becomes important.

- **Q-1** — Who may change or delete a User? **Today: anyone**, because there
  is no login. This is a security hole. `TASK-006` answers it: only the User
  themself.
- **Q-2** — Who may change or delete a Post? Today: anyone. `TASK-007` answers
  it: only its author.
- **Q-3** — Is the email case-sensitive? Today `A@x.com` and `a@x.com` are two
  different Users. No ticket yet.
