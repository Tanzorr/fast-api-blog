# Tools, Versions and Services

## Software

| Part | Version | What it does |
| :--- | :--- | :--- |
| Python | 3.12 | The language. Virtual environment in `venv1/` |
| FastAPI | 0.148 | Web framework: path operations, validation, `/docs` |
| Uvicorn | 0.54 | The server that runs the app (`fastapi dev` starts it) |
| Pydantic | 2.14 | Schemas: checks request data, shapes responses |
| pydantic-settings | 2.16 | Reads settings from env variables and `.env` (ADR-003) |
| SQLAlchemy | 2.1 | ORM: models, sessions, queries (ADR-004) |
| psycopg | 3.3 | Lets Python talk to PostgreSQL |
| pwdlib + argon2-cffi | 0.3 / 25.1 | Password hashing with Argon2 (ADR-006) |
| PostgreSQL | 17 | Database, runs in Docker (ADR-001) |
| Docker Compose | v2 | Runs the database on your computer |
| pytest | 9.1 | Runs the tests in `tests/` ([`testing.md`](testing.md)) |
| ruff | 0.17 | Linter and formatter; rules in `pyproject.toml` |

Not installed yet: Alembic (`TASK-005`).

The packages are listed in [`../../requirements.txt`](../../requirements.txt),
**without exact versions** (ADR-002). The versions above are what `venv1` has
today (`venv1/bin/pip list`).

## Services

| Service | How it runs | Port on your computer | Notes |
| :--- | :--- | :--- | :--- |
| API | On your computer, from `venv1` | 8000 | `fastapi dev main.py` restarts by itself when code changes |
| `db` | Docker Compose, container `fastapi-postgres` | `POSTGRES_PORT` (default 5432) | Data is saved in the volume `pgdata`. Has a health check |

## Environment Variables

They are read only in [`database.py`](../../database.py) by the `Settings`
class, and nowhere else (ADR-003). The API and `docker-compose.yml` read the
same `.env` file. Copy `.env.example` to `.env` to start.

| Variable | Example | Meaning |
| :--- | :--- | :--- |
| `POSTGRES_USER` | `postgres` | Database user (required) |
| `POSTGRES_PASSWORD` | `change-me` | Database password (required, only for development) |
| `POSTGRES_DB` | `fastapi` | Database name (required) |
| `POSTGRES_HOST` | `localhost` | Where the API finds the database (default `localhost`) |
| `POSTGRES_PORT` | `5432` | Database port on your computer (default `5432`) |

## Commands

```bash
cp .env.example .env                       # first time only, then edit it
docker compose up -d                       # start the database
python3 -m venv venv1                      # first time only
venv1/bin/pip install -r requirements.txt  # first time, and after requirements change
venv1/bin/fastapi dev main.py              # start the API with auto-restart
venv1/bin/pytest                           # run the tests (the database must run)
venv1/bin/ruff check .                     # find code problems
venv1/bin/ruff format .                    # format the code
docker compose logs -f db
docker compose exec db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"  # SQL prompt
```

| URL | What |
| :--- | :--- |
| <http://localhost:8000/docs> | Interactive API docs (Swagger UI) — try every endpoint here |
| <http://localhost:8000/redoc> | The same docs, another style |
| <http://localhost:8000/> | Returns `{"message": "Hello World!!!"}` |
