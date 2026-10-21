# Mode: IMPLEMENT

Build what a ticket describes.

## Read

1. The ticket from [`../backlog/`](../backlog/INDEX.md) — also the "Not in This Ticket" part
2. [`../context/conventions.md`](../context/conventions.md) — every time
3. [`../context/architecture.md`](../context/architecture.md) — layers, where each idea lives in code, decisions (ADRs)
4. [`../context/stack.md`](../context/stack.md) — versions, services, commands
5. [`../context/testing.md`](../context/testing.md) — before you write tests
6. The strict rules (invariants) the ticket names, from [`../context/ontology.md`](../context/ontology.md)

## Steps

1. **Read the acceptance criteria again.** If something is not clear, ask now,
   not during review.
2. **Find the places to change.** Read the files before you edit them.
3. **Write the test first** for the behaviour the ticket promises.
4. **Build the smallest thing** that meets the criteria.
5. **Explain the new FastAPI / Python ideas** you used, in a few words, with a
   docs link (CLAUDE.md §1).
6. **Run the checks**: `pytest`, `ruff check`, `ruff format --check`
   (see [`testing.md`](../context/testing.md)).
7. **Update what the change made wrong** — the ontology, an ADR, a context file.
8. **Finish**: move the ticket to [`../archive/`](../archive/INDEX.md) with a
   note about the result.

## Rules

- **Stay inside the ticket.** If you find something else broken, it needs a new
  ticket.
- **New idea in the domain ⇒ update `ontology.md`** in the same change.
- **New decision ⇒ write an ADR** in `architecture.md`.
- **Blocked, or the ticket is wrong?** Stop and say it.
- **Never say a test passes if you did not run it.**

## Finished When

Every point of the Definition of Done in
[`../context/conventions.md`](../context/conventions.md) is true.
