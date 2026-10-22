# Backlog

Work we plan to do. A ticket stays here until it is finished. Then it moves to
[`../archive/`](../archive/INDEX.md) with a note about the result.

New tickets use [`TEMPLATE.md`](TEMPLATE.md).

## Open Tickets

| ID | Title | Status | Priority | Goal | Needs first |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TASK-007](TASK-007-post-author.md) | Give every Post one or more authors; only its authors can change it | `planned` | P1 | V-5 | TASK-005, TASK-006 |
## Rules

- **ID** — `TASK-NNN`. Never use a number again. Never change a number. The
  number does not show the order of work; the `Needs first` column does.
- **File name** — `TASK-NNN-<kebab-slug>.md`.
- **Status** — `planned` → `in-progress` → `done`. Or `blocked`, with the
  reason.
- **Priority** — P0: nothing else can start before it · P1: main feature ·
  P2: quality · P3: nice to have.
- **Goal** — every ticket links to a goal (value driver) in
  [`../business/VALUE.md`](../business/VALUE.md).
- This table and the ticket files must say the same thing. If they are
  different, the ticket file is correct.
