# Using Tools

Which tool to use for which job, and what the agent may touch. The computer
enforces part of this in
[`../../.claude/settings.json`](../../.claude/settings.json); this file explains
why.

## Permissions

| Level | What | Why |
| :--- | :--- | :--- |
| **Allowed, no question** | Reading the repository; shell commands that only read (`rg`, `find`, `ls`, `git status/log/diff`); `pytest`, `ruff`, `pip list` | You can undo them, they change nothing |
| **Ask first** | `pip install`, `alembic upgrade/revision`, starting the server, `docker compose up/down`, `git add/commit/push`, editing `requirements.txt` / `docker-compose.yml` / `.env.example` | Each one makes a lasting change — to packages, the database, containers or git history |
| **Not allowed** | Reading `.env` and keys; `rm -rf`; `git push --force`; `docker compose down -v` | The agent never needs a secret, and never needs to destroy data |

## Searching

```bash
rg 'class UserModel' --type py       # find a name in all the code
rg -n 'password' routers/            # search only in one folder
rg -l 'Depends\(get_db\)'            # show which files, not which lines
```

- Use `rg` rather than `grep`; it skips the files in `.gitignore`.
- Search for the *word from the ontology* first. If nothing is found, it is not
  built yet.
- Where FastAPI's own source code is:
  `venv1/bin/python -c "import fastapi; print(fastapi.__path__)"`.

## Editing

- **Read a file before you edit it.**
- Change only the part you need. Do not rewrite the whole file.
- One topic in each edit. Do not reformat a file that you are also changing.
- After `TASK-005`: never change a migration that was already applied — create
  a new one.

## Checking

```bash
venv1/bin/pytest                 # after TASK-004
venv1/bin/ruff check .           # after TASK-004
venv1/bin/ruff format --check .  # after TASK-004
docker compose ps
docker compose logs --tail=50 db
```

Run the check. Do not guess if it will pass.

## Strict Rules

1. **Never read `.env`.** Read `.env.example` instead.
2. **Never run a command that destroys data if nobody asked you to.**
3. **Never commit or push if nobody clearly asked you to.**
4. **Never install a dependency without asking first.**
5. **Never write files outside the project folder.**
6. **Tell the truth about what happened.**
