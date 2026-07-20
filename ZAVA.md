# Zava -- Technical Briefing

> **Executable org composition.** One invocation builds a proven vertical
> pack with a synthetic actor world. Then deploy private-live or
> public-replay.

---

## One-invocation journey

```
compose-org "<target>"
```

Internally runs four phases:

| Phase | What happens | Output |
|-------|-------------|--------|
| **Research** | Invokes `research-company` (factual sub-skill). Profiles the target against public sources -- Wikipedia, registries, annual reports. | `org-brief.yaml` with sourced facts and explicit uncertainties |
| **Design** | Selects process profiles from the shared engine library. Maps org-brief to actor archetypes and causal scenario seeds. | Vertical design document |
| **Build** | Generates the executable vertical pack: typed actors, causal world state, process instances, deterministic golden scenarios. | `verticals/<slug>/` -- standalone proven pack |
| **Prove** | Runs the proof gate: replay deterministic scenarios, verify causal invariants, emit `proof/manifest.json`. Fail-closed. | Proof manifest with source_commit, fingerprint, live_result, replay_result |

The fact/synthetic boundary: Phase Research produces only source-backed
facts; Phases Design+Build generate the deterministic synthetic world
anchored by those facts; Phase Prove connects them with a verifiable proof.

---

## Vertical packs

A vertical pack (`verticals/<slug>/`) is the build output:

- **Typed actors** -- deterministic synthetic entities with causal
  relationships (not random data).
- **Process profiles** -- drawn from shared engines (expense-claim,
  vendor-kyc, etc.) and composed per vertical.
- **Causal world** -- a self-consistent actor world where every state
  transition is causally justified.
- **Golden scenarios** -- deterministic replay sequences that prove
  correctness.
- **Proof manifest** -- `proof/manifest.json` with source_commit,
  fingerprint, evidence, live_result=PASS, replay_result=PASS.

A vertical pack is NOT a repository fork, global rebrand, schema swap, UI
mock, or stub library. It is an executable proven artifact.

---

## Deployment modes

```
zava-workspace-deploy --mode private-live
zava-workspace-deploy --mode public-replay
```

| Mode | Actor world | Auth | Functions | State |
|------|-------------|------|-----------|-------|
| **private-live** | Enabled, writable | Required | Durable Functions enabled | Mutable |
| **public-replay** | Disabled | None | Skipped | Read-only, baked tape |

The deploy skill requires a valid proof manifest before any Azure
mutation. Mode choice is explicit and mandatory.

---

## Proof gate

Before deployment, the proof gate verifies:

- `source_commit` matches `git rev-parse HEAD`
- `fingerprint` matches vertical content hash
- `live_result` = PASS
- `replay_result` = PASS
- `browserErrors` = []

Fail-closed: any mismatch aborts deployment.

---

## Proven reference

**Telco** is the current proven reference vertical -- clean compose-org
run with proof gate PASS. Additional verticals (e.g., Fashion) require
their own acceptance run before claiming proven status.

---

## Source repos

- [`arturcrmbot/zava-control-plane`](https://github.com/arturcrmbot/zava-control-plane) -- the substrate
- [`arturcrmbot/zava-design-skills`](https://github.com/arturcrmbot/zava-design-skills) -- design skills + industry primers
- [`aiappsgbb/zava-constellation`](https://github.com/aiappsgbb/zava-constellation) -- this plugin (compose-org, zava-workspace-deploy, research-company)

---

## Commands

```bash
# Install the plugin
copilot plugin install zava-constellation@zava-constellation

# Build a vertical (Research -> Design -> Build -> Prove)
compose-org "Contoso Telco"

# Deploy
zava-workspace-deploy --mode private-live
zava-workspace-deploy --mode public-replay
```

---

## See also

- [README.md](README.md) -- install and quick start
- [`skills/compose-org/SKILL.md`](skills/compose-org/SKILL.md)
- [`skills/zava-workspace-deploy/SKILL.md`](skills/zava-workspace-deploy/SKILL.md)
- [`skills/research-company/SKILL.md`](skills/research-company/SKILL.md)
