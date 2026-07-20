# zava-constellation

> **Two Copilot entry points.** `compose-org "<target>"` builds a proven
> executable vertical pack, then `zava-workspace-deploy` ships it
> private-live or public-replay on Azure.

**[Live experience page](https://aiappsgbb.github.io/zava-constellation/)**

---

## What is Zava?

**Zava** is the agentic substrate that powers executable org compositions:
a multi-domain control plane with persona-driven orchestration, real-time
SSE fleet streams, and OpenTelemetry observability.

One invocation builds a complete vertical:

```
compose-org "<target>"
```

Internally `compose-org` runs four phases -- Research, Design, Build, Prove
-- producing a proven vertical pack with a deterministic synthetic actor
world anchored by source-backed factual research.

Then deploy:

```
zava-workspace-deploy --mode private-live   # writable actor world, auth
zava-workspace-deploy --mode public-replay  # baked tape, read-only
```

> **Full architecture and runbook:** [ZAVA.md](ZAVA.md)

---

## Quick start

### Install the plugin

```bash
copilot plugin marketplace add aiappsgbb/zava-constellation
copilot plugin install zava-constellation@zava-constellation
```

### Run

```bash
# Build the vertical (Research -> Design -> Build -> Prove)
> "Use compose-org to build a vertical for Contoso Bank."

# Deploy (choose mode)
> "Use zava-workspace-deploy to ship private-live to Azure."
```

---

## Zava + Threadlight

Threadlight designs and deploys individual business-process agents. Zava
wraps them in a multi-domain control plane with fleet orchestration and a
polished dashboard. Use Threadlight for the "one process" pitch; Zava for
the "enterprise operating system" pitch.

The Threadlight skills live in
[awesome-gbb](https://github.com/aiappsgbb/awesome-gbb).

---

## Skills

| Skill | What it does |
|-------|-------------|
| [**compose-org**](skills/compose-org/) | One invocation: Research, Design, Build, Prove. Takes a target name, invokes `research-company` internally for factual profiling, designs a vertical pack, builds the synthetic actor world, proves causal correctness. Output: a proven executable vertical. |
| [**zava-workspace-deploy**](skills/zava-workspace-deploy/) | Deploy the proven vertical to Azure Container Apps. Two modes: `private-live` (writable actor world, Durable Functions, auth) or `public-replay` (baked tape, read-only). Proof manifest gate required before deploy. |
| [**research-company**](skills/research-company/) | *Internal factual sub-skill* invoked by compose-org during Phase Research. Profiles the target against public sources (Wikipedia, registries, annual reports). Emits `org-brief.yaml`. Not a required separate pipeline step. |

---

## Proven reference

Telco is the current proven reference vertical (clean compose-org run +
proof gate PASS). Additional verticals require their own acceptance run.

---

## License

[MIT](LICENSE)
