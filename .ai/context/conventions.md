# Code Rules

Rules for every line of code in this repository. When a rule has a reason, we
give the reason. If you understand why a rule exists, you can use it in cases
the rule does not mention.

## Language and Style

- **Python 3.12.** Every function has type hints.
- **PEP 8**, checked by `ruff format` and `ruff check`. Both
  must show no problems before you finish.
- Use f-strings to build text; use `pathlib.Path` for file paths.
- Use modern types: `list[int]`, `str | None` — not `List`, `Optional`.

## Names

| Thing | Rule | Example |
| :--- | :--- | :--- |
| SQLAlchemy model | `CamelCase`, singular, ends in `Model` | `PostModel` |
| Table | lowercase, plural | `posts` |
| Input schema | the ontology word | `Post`, `User` |
| Output schema | ends in `Out` | `PostOut`, `UserOut` |
| Router file | plural noun | `routers/posts.py` |
| URL path | plural noun, id in the path | `/posts/{post_id}` |
| Column | `snake_case`; date+time ends in `_at` | `created_at` |
| Function / variable | `snake_case`, starts with a verb | `get_post_or_404()` |
| Constant | `UPPER_SNAKE` | `MAX_TITLE_LENGTH` |
| Test | `test_<behaviour>` | `test_duplicate_email_returns_409` |

**Names come from the ontology.** If the ontology says `Post`, the model is not
called `Article` or `Item`.

## HTTP

| Action | Method | Success status |
| :--- | :--- | :--- |
| List | `GET /things` | `200` |
| Get one | `GET /things/{id}` | `200` |
| Create | `POST /things` | `201` |
| Replace | `PUT /things/{id}` | `200` |
| Delete | `DELETE /things/{id}` | `204`, no body |

## DO

- **Keep endpoints short.** Business rules go in a helper or a service.
- **Always set `response_model`.** It is the only way to be sure secret fields
  (like `password`) never leave the API (I-3).
- **Use separate input and output schemas.** Input has what the client sends;
  output has what the client may see.
- **Get the database session with `Depends(get_db)`.** Never create
  `SessionLocal()` in an endpoint.
- **Use a `get_<thing>_or_404()` helper** when you find a row by an id from
  the URL.
- **Let the database enforce rules** (unique, not null) and turn its errors
  into HTTP errors (ADR-007).
- **Hash passwords with `security.password_hash`** — nothing else.

## DON'T

- **Don't build SQL with f-strings.** Use the ORM, or `text()` with parameters.
- **Don't return a model without `response_model`.**
- **Don't read `os.environ` outside `config.py`** (ADR-003).
- **Don't put secrets in code or in `docker-compose.yml`.** Use `.env`.
- **Don't leave `print()`, `breakpoint()` or code in comments** in a change.
- **Don't add a package to solve a five-line problem.** Ask before you add any
  dependency.
- **Don't commit `.env`** or real passwords and keys.

## Errors

- Row does not exist → `404` with `HTTPException`.
- Bad request data → FastAPI returns `422` by itself. Do not check by hand what
  Pydantic can check.
- A unique rule is broken → `409`, after `db.rollback()`.
- Don't catch an exception if you cannot handle it. A bare `except:` hides bugs.

## Commits

- The first line is a command, 72 characters or less: `Add login endpoint`.
- Name the ticket in the message body: `Ticket: TASK-006`.
- One logical change in each commit.

## Definition of Done

A ticket is finished only when all of this is true:

1. The code follows the rules above; `ruff check` and `ruff format --check`
   show no problems.
2. Tests cover the new behaviour, and also what happens when it fails.
3. All `pytest` tests pass.
4. Every strict rule (invariant) the change touches is still true. Write which
   ones in the ticket.
5. If you made a decision, it is written as an ADR in
   [`architecture.md`](architecture.md).
6. If you added or renamed an idea, [`ontology.md`](ontology.md) is updated.
7. A change that users can see has a line in
   [`CHANGELOG.md`](../../CHANGELOG.md) that starts with the ticket ID.
8. The ticket is moved to [`../archive/`](../archive/INDEX.md) with a note
   about the result.
