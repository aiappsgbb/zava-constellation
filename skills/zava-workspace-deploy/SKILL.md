---
name: zava-workspace-deploy
description: >
  Deploy proven Zava workspace to Azure Container Apps in private-live
  (auth, Durable Functions, actor world) or public-replay (read-only
  baked tape, no Functions) mode. Proof manifest required before Azure
  mutation. azd/ACA/Bicep; tenant isolation via aiappsgbb/awesome-gbb.
  USE FOR: deploy Zava, Zava ACA, azd up, Zava live, Zava replay,
  agentic-org deploy, zava-control-plane deploy.
  DO NOT USE FOR: Threadlight deploy, Citadel hub, Foundry agents.
metadata:
  version: "4.0.0"
---

# Zava Workspace Deploy

Deploy a proven Zava workspace vertical to Azure Container Apps.
Choose a mode, validate the proof manifest, revalidate tenant isolation,
then `azd up`.

## Mode gate — choose before any Azure mutation

You MUST select or pick a mode before any Azure mutation or `azd` command:

| Mode | Slug | Purpose |
|------|------|---------|
| **private-live** | Authenticated live org simulation | Full Durable Functions orchestration, actor world enabled, writable state, HITL gates |
| **public-replay** | Read-only deterministic replay | Baked tape playback, read-only middleware, Functions skipped, actor world disabled |

---

## Proof manifest — fail closed

Deployment requires a passing proof from compose-org (or equivalent).
The proof manifest lives at `proof/manifest.json` in the workspace repo.

### Required manifest fields

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

### Preflight checks (shell/jq) — exit 1 on any failure

```bash
# 1. Source commit must match current HEAD
MANIFEST_COMMIT=$(jq -r '.source_commit' proof/manifest.json)
[ "$(git rev-parse HEAD)" = "$MANIFEST_COMMIT" ] || { echo "❌ source_commit mismatch"; exit 1; }

# 2. Vertical matches requested vertical
MANIFEST_VERT=$(jq -r '.vertical' proof/manifest.json)
[ "$MANIFEST_VERT" = "$REQUESTED_VERTICAL" ] || { echo "❌ vertical mismatch"; exit 1; }

# 3. Fingerprint matches selected pack runtime fingerprint (from manifest)
MANIFEST_FP=$(jq -r '.fingerprint' proof/manifest.json)
[ -n "$MANIFEST_FP" ] || { echo "❌ fingerprint missing"; exit 1; }

# 4. Live result PASS
[ "$(jq -r '.live_result' proof/manifest.json)" = "PASS" ] || { echo "❌ live proof not PASS"; exit 1; }

# 5. Replay result PASS
[ "$(jq -r '.replay_result' proof/manifest.json)" = "PASS" ] || { echo "❌ replay proof not PASS"; exit 1; }

# 6. browserErrors must be empty []
ERRORS=$(jq '.browserErrors | length' proof/manifest.json)
[ "$ERRORS" -eq 0 ] || { echo "❌ browserErrors not empty ($ERRORS errors)"; exit 1; }

echo "✅ Proof manifest validated — safe to deploy"
```

All checks use fresh evidence from files; the preflight fails closed
(any mismatch → abort with `exit 1`).

---

## Inputs

| Input | Description |
|-------|-------------|
| Proven workspace repo | Cloned repo with passing `proof/manifest.json` |
| Mode | `private-live` or `public-replay` |
| Azure tenant/subscription | Isolated via `azure-tenant-isolation` (aiappsgbb/awesome-gbb) |
| Existing shared ACR | Container registry (not provisioned by this skill) |
| Existing App Insights | Telemetry sink (not provisioned by this skill) |
| LLM endpoint | Citadel APIM gateway or direct Foundry endpoint (live mode) |

---

## Tenant isolation — revalidate before azd up

Tenant isolation dependency lives in **aiappsgbb/awesome-gbb**
(`azure-tenant-isolation` skill). You MUST revalidate tenant immediately
before any `azd up`:

```bash
# Set AZURE_CONFIG_DIR / AZD_CONFIG_DIR per aiappsgbb/awesome-gbb tenant-isolation
ACTUAL_TENANT=$(az account show --query tenantId -o tsv)
[ "$ACTUAL_TENANT" = "$EXPECTED_TENANT_ID" ] || { echo "❌ Tenant mismatch"; exit 1; }
echo "✅ Tenant verified — proceeding with azd up"
```

---

## Capabilities — introspect from manifest

Do NOT hard-code domain/route/agent counts. Discover capabilities from
the workspace manifest or repo introspection:

```bash
# Example: read domain count from manifest or file system
DOMAINS=$(jq '.verticals | length' manifest.json 2>/dev/null || find verticals -maxdepth 1 -mindepth 1 -type d | wc -l)
echo "Deploying workspace with $DOMAINS domain verticals"
```

The manifest declares what the workspace contains — capabilities are
introspected at deploy time, not baked into the skill definition.

---

## Deploy: `azd up`

The workspace uses the standard azd/ACA pattern:

```
workspace-repo/
├── azure.yaml              # azd project: host=containerapp
├── deploy/
│   ├── Dockerfile          # Multi-stage: node → python → runtime
│   └── entrypoint.sh       # Mode-aware: live starts Functions; replay skips
├── infra/
│   ├── main.bicep          # Subscription-scoped orchestrator
│   └── modules/            # UAMI, storage, ACA env, ACA app, RBAC
└── proof/
    └── manifest.json       # Required — validated in preflight
```

Bicep provisions: UAMI, Storage (Azure Files for KuzuDB persistence),
ACA environment + container app, AcrPull RBAC on shared ACR.

---

## private-live mode

Configuration:

```bash
ZAVA_MODE=live
ZAVA_VERTICAL=<slug>
```

Behavior:
- **Durable Functions enabled** — `entrypoint.sh` starts the Functions host
  on :7071 alongside uvicorn on :80
- **Actor world enabled** — entity graph writable, state mutations allowed
- **Writable state** — KuzuDB, working memory, audit ledger accept writes
- **Authentication required before public ingress** — ACA ingress auth or
  application-level auth gate blocks unauthenticated access

### private-live postdeploy smoke

| Check | Command |
|-------|---------|
| Health | `curl -sf https://$FQDN/api/health` |
| Workflow smoke | `curl -sf https://$FQDN/api/workflows \| jq length` |
| HITL gate present | `curl -sf https://$FQDN/api/hitl/pending \| jq length` |
| World mutation smoke | `curl -X POST https://$FQDN/api/entities/test-write` returns 2xx |

---

## public-replay mode

Configuration:

```bash
ZAVA_MODE=replay
ZAVA_TAPE_PATH=/app/tape/tape.tar.gz
```

Behavior:
- **Baked tape** — all workflow events replayed from pre-recorded tape path
- **Read-only middleware** — write endpoints return 405 or 403
- **Functions skipped** — `entrypoint.sh` detects `ZAVA_MODE=replay` and
  does not start the Functions host (no AzureWebJobsStorage dependency)
- **Actor world disabled** — entity graph and state are read-only

### public-replay postdeploy smoke

| Check | Command |
|-------|---------|
| Replay meta smoke | `curl -sf https://$FQDN/api/replay/meta \| jq .tape_path` |
| Read-only write rejection | `curl -X POST https://$FQDN/api/workflows -w '%{http_code}'` returns 405 or 403 |
| Surface smoke | `curl -sf https://$FQDN/ && curl -sf https://$FQDN/portal/` |

---

## Entrypoint behavior (from zava-control-plane)

The `deploy/entrypoint.sh` implements mode-awareness:

- **live**: starts Azure Functions host background process on :7071, then
  `exec uvicorn` on :80 as PID 1. Functions host enables Durable
  orchestration for workflow state machines.
- **replay**: skips Functions host entirely (`ZAVA_MODE=replay` branch in
  entrypoint), execs uvicorn directly. No AzureWebJobsStorage dependency.

This matches the actual repo's `deploy/entrypoint.sh` pattern — no
fabricated commands.

---

## Infrastructure (Bicep modules)

| Module | Resource | Purpose |
|--------|----------|---------|
| `uami.bicep` | User-Assigned Managed Identity | Keyless auth to Foundry, Storage, ACR |
| `storage.bicep` | Storage Account + Azure Files | KuzuDB persistence across ACA restarts |
| `aca-env.bicep` | ACA Managed Environment + volume | Container runtime with Azure Files volume |
| `aca-app.bicep` | ACA Container App | Runs uvicorn; placeholder image swapped by azd deploy |
| `rbac-acr-pull.bicep` | AcrPull role assignment | UAMI → existing shared ACR |

Shared resources (ACR, App Insights, Log Analytics) are NOT provisioned
by this skill — they are passed as parameters from the existing
subscription-level shared infra.

---

## Deployment sequence

1. **Select mode** — `private-live` or `public-replay` (mode gate)
2. **Validate proof manifest** — all preflight checks pass or abort
3. **Set tenant isolation** — per aiappsgbb/awesome-gbb skill
4. **Revalidate tenant** — immediately before `azd up`
5. **Run `azd up`** — provisions Bicep infra + builds/deploys container
6. **Postdeploy smoke** — mode-specific health/function/surface checks

---

## See also

| Skill | Relationship |
|-------|-------------|
| `azure-tenant-isolation` (aiappsgbb/awesome-gbb) | Tenant/subscription isolation — MANDATORY dependency |
| `compose-org` | Produces the workspace + proof manifest this skill deploys |
| `threadlight-deploy` | Deploys individual Threadlight processes |
| `citadel-hub-deploy` | Deploys the APIM gateway for LLM routing |
