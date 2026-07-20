# Proof Contract

Defines the acceptance criteria for a vertical pack proof run,
mirroring the target substrate's `docs/VERTICAL-PROOF.md`.

## Relationship to substrate proof spec

This contract references and implements the proof protocol defined in
`docs/VERTICAL-PROOF.md` of the acquired substrate (zava-control-plane).
The proof contract here is the skill-side specification; the substrate
doc is the implementation-side checklist.

## Required proof chain

A vertical is not proven until a live causal chain passes end-to-end:

1. **Actor world** — seeded world with named actors, relationships,
   and realistic distributions.
2. **Sensor** — an event trigger fires from world state.
3. **Objective** — the workflow engine accepts a typed command with
   a declared objective.
4. **Durable** — a Durable Object processes the command through
   defined phases.
5. **HITL** — at least one human-in-the-loop gate fires and is
   approved.
6. **Typed command** — a domain-specific command mutates state.
7. **World mutation** — the actor world reflects the outcome.
8. **Evaluation** — success criteria evaluate to pass.

## Cross-surface consistency

The same IDs and outcomes must be observable across:

- World (actor world state)
- Workflow API (REST/event responses)
- Drawer (UI panel state)
- Memory (conversation memory)
- Knowledge (knowledge graph)
- AG-UI (agent-user interface)
- Graph (entity/relation graph)
- Constellation (skill orchestration)

## Replay with functions disabled

After the happy-path proof passes, replay the same scenario with
Functions and world state disabled. The system must degrade
gracefully — no crashes, no orphaned state.

## Clean-room criteria

- Zero browser console errors during proof run
- Zero dropped workflow events
- Clean teardown — all Durable Objects and temporary state removed

## Evidence manifest

Every proof run must produce a permanent evidence bundle at
`verticals/<slug>/proof/`:

| Artifact | Purpose |
|---|---|
| `proof-run.log` | Full stdout/stderr of the proof command |
| `proof-manifest.json` | Machine-readable pass/fail per criterion |
| `screenshots/` | Key UI states captured during run |
| `recordings/` | AG-UI interaction recordings |
| `world-snapshot-before.json` | Actor world state before proof |
| `world-snapshot-after.json` | Actor world state after proof |

## Source commit SHA

The proof evidence must record the exact source commit SHA of the
substrate at proof time. This is stored in `proof-manifest.json`
under the `source_commit` key. The vertical slug is stored under
`vertical`.

```json
{
  "source_commit": "<sha>",
  "vertical": "<slug>",
  "timestamp": "<ISO-8601>",
  "pass": true,
  "criteria": [ ... ]
}
```

## Permanent proof command

The build phase must generate a runnable proof command that any
operator can execute to re-prove the vertical at any future commit:

```bash
make prove VERTICAL=<slug>
```

This command is permanent — it must work at any point in the
repository's future without manual setup beyond `make funcvenv`.

## Failure policy

Never claim a vertical is ready if the proof fails. Report the
failing criterion, the evidence bundle path, and stop. The operator
fixes and re-runs.
