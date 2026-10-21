# Testing

Tests prove two things: the strict rules (invariants) in
[`ontology.md`](ontology.md) are true, and the behaviour a ticket promises
works. A test that can never fail proves nothing.

**Today there are no automated tests.** `TASK-004` adds pytest. Until then,
check a change by hand: start the API and call the endpoints in `/docs`, or
with FastAPI's `TestClient` in a short script.

## Kinds of Tests (after `TASK-004`)

| Kind | What it uses | Use it for |
| :--- | :--- | :--- |
| Unit | Nothing outside the code | Simple functions, for example password hashing |
| API | `TestClient` + a test database | Endpoints: status codes, response bodies, errors |

For features, use **API tests** first. They test path → schema → model →
database together. Most bugs in how the parts connect are found there.

Tests must use a **separate test database**, never the development database.
Replace `get_db` with `app.dependency_overrides[get_db]`.

## Tests We Must Have

Each row needs at least one test. Tickets add new rows.

| # | Behaviour | Proves | Status |
| :--- | :--- | :--- | :--- |
| T-1 | Creating a User with an email that is already used → `409` | I-1 | not written |
| T-2 | The saved password is not the plain text, and `verify()` accepts the original | I-2 | not written |
| T-3 | No `/users` response contains `password` | I-3 | not written |
| T-4 | A Post with a missing title or content → `422` | I-4 | not written |
| T-5 | `GET`, `PUT`, `DELETE` on an unknown id → `404` for posts and users | `TASK-001`, `TASK-002` | not written |
| T-6 | Create → get → update → delete works for posts and users | `TASK-001`, `TASK-002` | not written |

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

## Commands (after `TASK-004`)

```bash
venv1/bin/pytest
venv1/bin/pytest -k users           # only tests with this name
venv1/bin/pytest -x --lf            # stop at the first failure, run only the last failed tests
```

## Before You Say Something Works

Run the tests and read the output. "It should pass" is not a result.
