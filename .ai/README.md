# `.ai/` — Project Knowledge

This folder has everything you need to know to work on this repository
correctly. It is saved in git and reviewed like code, not kept in prompts. So
each new work session uses it again. Nobody needs to guess the domain again,
invent new names, or make the same decisions again.

The main idea: **each kind of knowledge has its own level.**

```
ontology  ──►  PLANNING       what exists, how things are connected
context   ──►  IMPLEMENTING   where code goes, how to write it
tools     ──►  ACTING         what you may read, run, change
```

## Folder Structure

```
.ai/
├── business/VALUE.md         Why the project exists — goals, and what it is not
├── context/
│   ├── INDEX.md              Which file to read, and when
│   ├── ontology.md           The domain — ideas, connections, strict rules
│   ├── stack.md              Versions, services, env variables, commands
│   ├── architecture.md       Layers, where each idea lives in code, decisions (ADRs)
│   ├── conventions.md        Names, what to do and not do, Definition of Done
│   ├── testing.md            Kinds of tests, tests we must have (T-n)
│   └── tools.md              Permissions, how to search/edit/check
├── router/                   implement · review
├── backlog/                  INDEX · TEMPLATE · open tickets
└── archive/                  Finished tickets, with a note about the result
```

[`../CLAUDE.md`](../CLAUDE.md) is the start page. It sends you to the right file
here.

## The Chain From Goal to Result

```
Goal (V-n) ──► Ontology idea ──► Strict rule (I-n)
                               │
                               ▼
                       Ticket (TASK-NNN)
                               │
                               ▼
               Code ──► Test (T-n) ──► Archive entry
```

Every link in this chain must be there. A missing link is a problem, and we
should name it:

- A ticket with no goal (value driver) is extra work nobody needs.
- A strict rule (invariant) with no test is a promise nobody checks.
- A name in the code that is not in the ontology is a name nobody agreed on.
- A finished ticket with no result note is a decision we forgot.

## Keeping It Up to Date

- Context files describe the system **as it is now**. Change the file directly;
  git keeps the old versions.
- When you choose between real options, write it down as an ADR in
  [`context/architecture.md`](context/architecture.md).
- If a file and the code say different things, that is a bug. An old, wrong
  context file is worse than no file, because people trust it.
