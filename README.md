# zava-constellation

> **Three Copilot skills.** Name a company → branded digital-clone workspace
> on Azure.

**▶ [Live experience page](https://aiappsgbb.github.io/zava-constellation/)**

---

## What is Zava?

**Zava** is the agentic substrate that powers digital-clone demos: a
multi-domain control plane with 37 operational domains, 170+ API routes,
persona-driven orchestration, real-time SSE fleet streams, and
OpenTelemetry → App Insights observability.

The pipeline runs in three steps — each a self-contained Copilot skill:

```
research-company → compose-org → zava-workspace-deploy
```

1. **`research-company`** — profile the target company (Wikipedia, annual
   reports, registry data) → emit `org-brief.yaml`
2. **`compose-org`** — fork the
   [`zava-control-plane`](https://github.com/arturcrmbot/zava-control-plane)
   substrate into a customer-branded digital clone
3. **`zava-workspace-deploy`** — build the React SPA, package with FastAPI,
   deploy to Azure Container Apps with OpenTelemetry

> **Full architecture and runbook:** [ZAVA.md](ZAVA.md)

---

## Quick start

### Install the plugin (all 3 skills)

```bash
copilot plugin marketplace add aiappsgbb/zava-constellation
copilot plugin install zava-constellation@zava-constellation
```

### Or install individual skills

```bash
gh skill install aiappsgbb/zava-constellation research-company
gh skill install aiappsgbb/zava-constellation compose-org
gh skill install aiappsgbb/zava-constellation zava-workspace-deploy
```

### Run the pipeline

```
> "Use research-company to profile Contoso Bank."
> "Use compose-org to fork the substrate for Contoso Bank."
> "Use zava-workspace-deploy to ship this to Azure."
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
| [**research-company**](skills/research-company/) | Profile a target organisation against its public web footprint — Wikipedia, annual reports, registry data — and emit an `org-brief.yaml` with named ELT, subsidiaries, strategic themes, and stack overrides. Ships 5 industry primers (telco, airline, banking, retail, auto-OEM). |
| [**compose-org**](skills/compose-org/) | Fork the substrate into a customer-flavoured digital clone using a signed-off org-brief + the matching primer. Ten phases: clone, rebrand, repack data fabric, swap entity kinds, regenerate personas, extend domain registry, scaffold MCP mocks, re-seed data, smoke-test. |
| [**zava-workspace-deploy**](skills/zava-workspace-deploy/) | Deploy the branded React/Vite SPA to Azure Container Apps — builds the SPA bundle, packages with FastAPI, generates Bicep + `azure.yaml`, configures API proxy + SSE passthrough, wires OpenTelemetry → App Insights. |

---

## License

[MIT](LICENSE)
