---
name: compose-org
description: >
  Build a working vertical pack for a named company or industry
  inside the Zava substrate. Four phases: Research, Design, Build,
  Prove. Acquires zava-control-plane, keeps canonical remote as
  upstream, places all customer behavior under verticals/<slug>/,
  never mass-rebrands core or replaces global registries. Proves
  via docs/VERTICAL-PROOF.md live causal chain. Output is a working
  local repo; deployment is separate.
  USE FOR: compose-org "Company" or compose-org "Industry".
  DO NOT USE FOR: single domain (use compose-domain inside the
  pack), deployment, pitch decks.
metadata:
  version: "2.0.0"
---

# compose-org

Build a **working vertical pack** for a named company or industry.

```
compose-org "<company or industry>"
```

One public entry point. Four phases. Output is a working local repo.

## Phase Research

If the operator does not supply pre-approved evidence, this phase
invokes `research-company` to gather source-backed facts and
uncertainties about the target organisation.

Research produces:
- Identity, ownership, size, geography
- Subsidiaries, leadership
- Strategic themes and stack signals
- Source references for every claim

Research is **facts and uncertainties only** — synthetic records or
actor worlds are never created or presented as facts in this phase.

If the operator supplies approved evidence (a signed org-brief),
this phase validates it and skips to Design.

## Phase Design

Interactive business-question phase. The agent asks **one question
at a time** and awaits approval before proceeding. Questions cover:

1. Actor world — who are the actors, what are their relationships?
2. Causal story — what events drive the business?
3. Process breadth — which processes does this vertical need?
4. Heroes — which ≤3 processes are hero (demo-grade)?
5. Functions and authority — org chart shape and decision rights.
6. Systems — what external systems does the company use?
7. Realism, seed, and reset — distribution parameters, seed data
   shape, teardown/reset policy.
8. Proof contract — what does "proven" mean for this vertical?
   (References `docs/VERTICAL-PROOF.md`.)

Technical decisions (file layout, framework choices, internal
module structure) stay with the agent — the operator approves
business semantics only.

## Phase Build

Acquires zava-control-plane and retains the canonical remote as
`upstream`. All customer-specific behavior is **additive** under
`verticals/<slug>/` — the build never performs literal mass-rebrands
of core, never replaces global registries or schema, and contains
no stubs.

Build produces the full manifest as applicable:

- Functions, domains, agents, authority, personas
- Policies, skills, MCPs
- Actor world and worlds (seed + reset)
- Operations, process profiles, reference cases
- Actions (typed commands), durable objects, projections
- Recordings, UI extensions

Uses the current Telco pack as a proven structural reference (not a
literal copy). Uses the current pack-scoped `compose-domain` for
bespoke hero workflows. Related processes may share engines, skills,
or MCPs, but each has a distinct trigger, profile, typed command,
world case, and success evidence.

### Build constraints

- Customer behavior lives in `verticals/<slug>/` only.
- Global registries are extended additively, never replaced.
- No stubs — every surface is functional or omitted.
- `upstream` remote is preserved for future substrate pulls.

See [`references/vertical-pack-contract.md`](references/vertical-pack-contract.md)
for the full ownership/boundary specification.

## Phase Prove

Follows the target substrate's proof protocol at `docs/VERTICAL-PROOF.md`.

The proof demonstrates a **live causal chain**:

```
actor world → sensor → objective → Durable → HITL →
typed command → world mutation → evaluation
```

The same IDs and outcomes must be observable across World, workflow
API, drawer, Memory, Knowledge, AG-UI, graph, and Constellation.

After the happy path, replay with Functions and world disabled.
Verify: zero browser errors, zero dropped workflow events, clean
teardown.

The build must generate a **permanent proof command**:

```bash
make prove VERTICAL=<slug>
```

This command writes a permanent evidence bundle at the repository
root `proof/`, including `proof/manifest.json`, screenshots,
recordings, logs, and before/after world snapshots. Pack-curated
recordings may additionally be copied to `verticals/<slug>/`
but the deploy artifact is the root `proof/` bundle.

See [`references/proof-contract.md`](references/proof-contract.md)
for the full proof specification.

**Never claim ready if proof fails.** Report the failing criterion
and stop.

## Safety rails

- Output is a working local repo. Deployment is separate.
- No automatic push to GitHub.
- Substrate `upstream` remote preserved — operator can pull future
  substrate updates.
- Per-phase commit boundaries for clean rollback.
- Idempotent: re-running with the same inputs produces the same
  vertical pack.

## Iterating

- Business-question issues → re-run Phase Design.
- Build issues → fix and re-run Phase Build.
- Primer issues → fix the matching primer, re-run.
- Proof failures → fix, re-prove. Never ship red.

## Downstream

After compose-org finishes and proof passes:

1. **Boot** — `make up` in the working repo.
2. **Walk** — verify in the control-plane UI.
3. **Deploy** — separate step, not part of this skill.
