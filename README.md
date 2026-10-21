# fast-api-blog

A small blog API for learning FastAPI: Posts and Users with PostgreSQL.

## Start

You need Python 3.12 and Docker.

```bash
cp .env.example .env                       # then set your own password
docker compose up -d                       # start PostgreSQL
python3 -m venv venv1
venv1/bin/pip install -r requirements.txt
venv1/bin/fastapi dev main.py
```

Open <http://localhost:8000/docs> to try the API.

## Endpoints

| Method | Path | What it does |
| :--- | :--- | :--- |
| GET | `/posts` | List Posts |
| POST | `/posts` | Create a Post |
| PUT | `/posts/{post_id}` | Change a Post |
| DELETE | `/posts/{post_id}` | Delete a Post |
| GET | `/users` | List Users |
| GET | `/users/{user_id}` | Get one User |
| POST | `/users` | Create a User |
| PUT | `/users/{user_id}` | Change a User |
| DELETE | `/users/{user_id}` | Delete a User |

## More

- Project knowledge, plans and decisions: [`.ai/`](.ai/README.md)
- Rules for AI agents: [`CLAUDE.md`](CLAUDE.md)
- Changes: [`CHANGELOG.md`](CHANGELOG.md)
