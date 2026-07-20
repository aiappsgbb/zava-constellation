# compose-org

Build a working vertical pack for a named company or industry
inside the Zava substrate.

See [`SKILL.md`](SKILL.md) for the canonical procedure.

## Entry point

```
compose-org "<company or industry>"
```

One command. The agent handles Research → Design → Build → Prove.

## Pipeline position

```
┌─────────────────────────┐
│  compose-org             │
│  "<company or industry>" │
├─────────────────────────┤
│  Phase Research          │ ← invokes research-company if needed
│  Phase Design            │ ← one business question at a time
│  Phase Build             │ ← verticals/<slug>/ additive pack
│  Phase Prove             │ ← docs/VERTICAL-PROOF.md causal chain
└─────────────────────────┘
         ↓
   Working local repo
   (deployment separate)
```

## Files

| File | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | Four-phase procedure. Strict frontmatter (≤1024 char, semver 2.0.0). |
| [`references/vertical-pack-contract.md`](references/vertical-pack-contract.md) | Ownership boundaries: what the pack owns vs global surfaces. |
| [`references/proof-contract.md`](references/proof-contract.md) | Acceptance criteria mirroring `docs/VERTICAL-PROOF.md`. |

## What it does

1. **Research** — gathers source-backed facts via `research-company`
   (or accepts pre-approved evidence).
2. **Design** — asks one business question at a time; approves actor
   world, causal story, process breadth, heroes, authority, systems,
   realism, proof contract.
3. **Build** — acquires zava-control-plane (retains `upstream`
   remote), places all customer behavior under `verticals/<slug>/`.
   Full manifest: functions, domains, agents, authority, personas,
   policies, skills, MCPs, world, operations, profiles, cases,
   actions, durable, projections, recordings, UI.
4. **Prove** — live causal chain per `docs/VERTICAL-PROOF.md`;
   generates a permanent proof command and evidence bundle.

## What it does NOT do

- **Deploy.** Output is a working local repo; deployment is separate.
- **Replace global registries.** All customization is additive.
- **Mass-rebrand core.** The substrate stays canonical.
- **Generate stubs.** Every surface is functional or omitted.
- **Push to GitHub.** Local-only by default.

## Build constraints

- Customer behavior under `verticals/<slug>/` only.
- Canonical `upstream` remote preserved.
- Uses current Telco pack as structural reference, not literal copy.
- Uses pack-scoped `compose-domain` for bespoke hero workflows.
- Related processes share engines/skills/MCPs but each has distinct
  trigger, profile, typed command, world case, success evidence.

## Changelog

- **2.0.0** (MAJOR) — Complete rewrite. Replaced ten-phase
  fork-and-rebrand procedure with four-phase Research/Design/Build/
  Prove contract. Customer behavior now additive under
  `verticals/<slug>/` instead of literal mass-rebrand. Proof
  required before completion claim. No stubs.
- **1.0.2** — Patch: clarified idempotent re-run semantics.
- **1.0.0** — Initial version (ten-phase fork-and-rebrand).
