# Proof Contract

**Contract version: `1.0.0`**

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
4. **Durable** — Azure Durable Functions processes the command through
   defined phases.
5. **HITL** — when the workflow declares one, the governed gate fires,
   persists recovery context, and resumes from the declared decision.
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

## Live and replay parity

After live proof passes, replay the same qualifying workflow set with Functions
and actor-world mutation disabled. Live and replay require user-visible parity
for workflow status, timeline, reasoning, observed tools, decisions, lineage,
and deterministic output, subject only to the substrate's documented volatile
field exclusions.

## Clean-room criteria

- Zero browser console errors during proof run
- Zero dropped workflow events
- Clean teardown — Azure Durable Functions and temporary state removed

## Evidence manifest

Every proof run must produce a permanent evidence bundle at the
repository root `proof/`:

| Artifact | Purpose |
|---|---|
| `proof/manifest.json` | Canonical machine-readable pass/fail manifest |
| `proof/live-summary.json` | Per-criterion detail for the live run |
| `proof/replay-summary.json` | Per-criterion detail for the replay run |
| `proof/screenshots/` | Key UI states captured during run |
| `proof/recordings/` | AG-UI interaction recordings |
| `proof/world-snapshot-before.json` | Actor world state before proof |
| `proof/world-snapshot-after.json` | Actor world state after proof |

Pack-curated recordings may additionally be copied into
`verticals/<slug>/` for pack-local reference, but the authoritative
deploy artifact is always the root `proof/` bundle.

## Source commit and manifest schema

The permanent evidence bundle is anchored by `proof/manifest.json`.
This file must be written (or overwritten) by the proof command and
must contain all fields required by the deploy skill:

```json
{
  "source_commit": "<sha>",
  "vertical": "<slug>",
  "fingerprint": "<pack-runtime-fingerprint>",
  "live_result": "PASS",
  "replay_result": "PASS",
  "browserErrors": [],
  "live_summary": "proof/live-summary.json",
  "replay_summary": "proof/replay-summary.json"
}
```

`source_commit` is the exact `git rev-parse HEAD` SHA at proof time.
`fingerprint` is the pack runtime fingerprint recorded at build time.
`live_summary` and `replay_summary` point to per-criterion detail
files also written under `proof/` by the same proof command.
Additional fields (e.g. `timestamp`, `criteria`) may be present but
the eight fields above are required and must pass the deploy preflight.

## Permanent proof command

The build phase must generate a runnable proof command that any
operator can execute to re-prove the vertical at any future commit:

```bash
make prove VERTICAL=<slug>
```

This command is permanent — it must work at any point in the
repository's future without manual setup beyond `make funcvenv`.

The command is responsible for:
- Running live and replay proof passes
- Writing `proof/manifest.json` with the current `source_commit`
  (`git rev-parse HEAD`), `fingerprint`, `live_result`, `replay_result`,
  `browserErrors`, `live_summary`, and `replay_summary`
- Writing `proof/live-summary.json` and `proof/replay-summary.json`
- Capturing screenshots, recordings, and world snapshots under `proof/`

## Readiness vocabulary

- **Build ready** means every applicable machine criterion in the acquired
  `docs/VERTICAL-PROOF.md` passes.
- **Demo ready** additionally requires a human seller review of reset, pacing,
  visual quality, and story coherence.

Machine proof cannot set seller review to PASS.

This contract version does not change the current proof manifest shape.
Manifest schema, repeatability-ledger, and deploy-preflight changes require a
later versioned contract.

## Failure policy

Never claim a vertical is ready if the proof fails. Report the
failing criterion, the evidence bundle path, and stop. The operator
fixes and re-runs.
