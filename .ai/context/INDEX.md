# Context Index

The important knowledge you need to write code. The mode files
([`../router/`](../router)) tell you *which* of these files to read. Do not
read all of them every time.

| File | Read it when | It tells you |
| :--- | :--- | :--- |
| [`ontology.md`](ontology.md) | You plan, design models, or change what an entity means | Ideas, connections, strict rules, open questions |
| [`stack.md`](stack.md) | Before you run or connect anything | Versions, services, ports, env variables, commands |
| [`architecture.md`](architecture.md) | Before you add a module or decide where code goes | Layers, where each idea lives in code, decisions (ADRs) |
| [`conventions.md`](conventions.md) | Every time you write code | Names, structure, what to do and not do, Definition of Done |
| [`testing.md`](testing.md) | Before you write a test or say that something works | Kinds of tests, tests we must have |
| [`tools.md`](tools.md) | When you search, edit or look at the repository | Which tool for which job, permissions, forbidden commands |

## Reading Order When You Are New

1. [`../business/VALUE.md`](../business/VALUE.md) — why the project exists
2. [`ontology.md`](ontology.md) — what is in the domain
3. [`stack.md`](stack.md) — what is really installed
4. [`architecture.md`](architecture.md) — where things go
5. [`conventions.md`](conventions.md) — how to write them

## Keeping It Up to Date

These files describe the system as it is now, not its history. When a decision
changes, edit the file directly and write the decision as an ADR in
[`architecture.md`](architecture.md). If you see that a file and the code say
different things, fixing it is part of your task.
