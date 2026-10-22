# Testing

Tests prove two things: the strict rules (invariants) in
[`ontology.md`](ontology.md) are true, and the behaviour a ticket promises
works. A test that can never fail proves nothing.

## Kinds of Tests

| Kind | What it uses | Use it for |
| :--- | :--- | :--- |
| Unit | Nothing outside the code | Simple functions, for example password hashing |
| API | `TestClient` + a test database | Endpoints: status codes, response bodies, errors |

For features, use **API tests** first. They test path → schema → model →
database together. Most bugs in how the parts connect are found there.

Tests must use a **separate test database**, never the development database
(ADR-009). [`tests/conftest.py`](../../tests/conftest.py) does this:

| Fixture | What it gives |
| :--- | :--- |
| `test_engine` | Once per run: creates `<POSTGRES_DB>_test` if missing, then its tables |
| `db` | A session on the test database. After the test, every table is emptied |
| `client` | A `TestClient`; `app.dependency_overrides[get_db]` returns `db` |
| `new_user`, `other_user` | A saved User, with its plain `password` added to the dict |
| `auth_headers` | `{"Authorization": "Bearer <token>"}` for `new_user` |

## Tests We Must Have

Each row needs at least one test. Tickets add new rows.

| # | Behaviour | Proves | Status |
| :--- | :--- | :--- | :--- |
| T-1 | Creating a User with an email that is already used → `409` | I-1 | done |
| T-2 | The saved password is not the plain text, and `verify()` accepts the original | I-2 | done |
| T-3 | No `/users` response contains `password` | I-3 | done |
| T-4 | A Post with a missing title or content → `422` | I-4 | done |
| T-5 | `GET`, `PUT`, `DELETE` on an unknown id → `404` for posts and users (there is no `GET /posts/{id}`) | `TASK-001`, `TASK-002` | done |
| T-6 | Create → get → update → delete works for posts and users | `TASK-001`, `TASK-002` | done |
| T-7 | The right email and password → `200` and a token that decodes to the User's id | `TASK-006` | done |
| T-8 | A wrong password → `401` | `TASK-006` | done |
| T-9 | An unknown email → `401` with the **same** message as T-8 | `TASK-006` | done |
| T-10 | `GET /users/me` with a token → the User; without a token → `401` | `TASK-006` | done |
| T-11 | An expired token → `401` | `TASK-006` | done |
| T-12 | A token signed with another secret → `401` | `TASK-006` | done |
| T-13 | A token of a deleted User → `401` | `TASK-006` | done |
| T-14 | `PUT` / `DELETE` a User without a token → `401`; another User → `403`; your own → `200` / `204` | I-5 | done |
| T-15 | Like a Post → `201` with `likes_count`; no token → `401`; unknown Post → `404` | `TASK-008` | done |
| T-16 | Like the same Post twice → `409`, still one like | I-6 | done |
| T-17 | Unlike → `204`; not liked → `404`; no token → `401` | `TASK-008` | done |
| T-18 | `GET /posts` shows the right `likes_count`; the number of queries does not grow with more Posts | `TASK-008` | done |
| T-19 | `GET /users/me/likes` lists only liked Posts; no token → `401` | `TASK-008` | done |
| T-20 | Deleting a Post or a User deletes its likes | `TASK-008` | done |
| T-21 | `GET /posts` and `GET /users`: 20 rows by default; `limit` / `offset` pages do not overlap; a wrong value → `422` | `TASK-009` | done |
| T-22 | `search` finds the text in `title` or `content`, in any case; `%` is a plain character | `TASK-009` | done |
| T-23 | `created_after` / `created_before` filter by `created_at`; a wrong date → `422` | `TASK-009` | done |
| T-24 | `min_likes` returns Posts with that many likes or more; a wrong value → `422` | `TASK-009` | done |
| T-25 | All parameters work together, and `GET /posts` is still one query | `TASK-009` | done |

## How to Write Tests

- One behaviour in each test. Use the behaviour as the name:
  `test_duplicate_email_returns_409`.
- Create the data inside the test (or in a fixture). Never use rows that
  another test created.
- Check the result you can see — a status code, a field in the response, a row.
- Also test what happens when things go wrong: bad data, an id that does not
  exist, an action that is not allowed.
- Code that depends on time: give the time to the code, or override it. Never
  use `time.sleep()`.

## Commands

The database must run (`docker compose up -d`), and `.env` must have
`JWT_SECRET`.

```bash
venv1/bin/pytest
venv1/bin/pytest -k users           # only tests with this name
venv1/bin/pytest -x --lf            # stop at the first failure, run only the last failed tests
```

## Before You Say Something Works

Run the tests and read the output. "It should pass" is not a result.
