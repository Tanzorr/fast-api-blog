# fast-api-blog

A small blog API for learning FastAPI: Posts and Users with PostgreSQL.

## Start

You need Python 3.12 and Docker.

```bash
cp .env.example .env                       # then set your own password and JWT_SECRET
docker compose up -d                       # start PostgreSQL
python3 -m venv venv1
venv1/bin/pip install -r requirements.txt
venv1/bin/alembic upgrade head             # create the tables
venv1/bin/fastapi dev main.py
```

Open <http://localhost:8000/docs> to try the API.

## Endpoints

| Method | Path | What it does |
| :--- | :--- | :--- |
| GET | `/posts` | List Posts (page by page, with search and filters) |
| POST | `/posts` | Create a Post |
| PUT | `/posts/{post_id}` | Change a Post |
| DELETE | `/posts/{post_id}` | Delete a Post |
| POST | `/posts/{post_id}/likes` | Like a Post 🔒 |
| DELETE | `/posts/{post_id}/likes` | Take your like back 🔒 |
| POST | `/auth/login` | Log in (form: `username` = email, `password`); returns an access token |
| GET | `/users` | List Users (page by page) |
| GET | `/users/me` | Get the logged-in User 🔒 |
| GET | `/users/me/likes` | List the Posts you liked 🔒 |
| GET | `/users/{user_id}` | Get one User |
| POST | `/users` | Create a User (sign up) |
| PUT | `/users/{user_id}` | Change your own User 🔒 |
| DELETE | `/users/{user_id}` | Delete your own User 🔒 |

🔒 needs the header `Authorization: Bearer <token>`. In `/docs`, click
**Authorize** and log in.

### List parameters

The lists are sorted by `id`. A wrong value → `422`.

| Parameter | Lists | Default | What it does |
| :--- | :--- | :--- | :--- |
| `limit` | `/posts`, `/users` | `20` | How many rows, from 1 to 100 |
| `offset` | `/posts`, `/users` | `0` | How many rows to skip |
| `search` | `/posts` | — | The text is in `title` or `content`; case does not matter |
| `created_after` | `/posts` | — | `created_at` is this date and time or later |
| `created_before` | `/posts` | — | `created_at` is this date and time or earlier |
| `min_likes` | `/posts` | — | `likes_count` is this number or more |

Example: `GET /posts?search=fastapi&min_likes=1&limit=10&offset=10` — the
second page of 10 liked Posts about FastAPI.

## Tests

```bash
venv1/bin/pytest          # the database must run
venv1/bin/ruff check .
venv1/bin/ruff format --check .
```

## More

- Project knowledge, plans and decisions: [`.ai/`](.ai/README.md)
- Rules for AI agents: [`CLAUDE.md`](CLAUDE.md)
- Changes: [`CHANGELOG.md`](CHANGELOG.md)
