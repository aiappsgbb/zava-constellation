# Vertical Pack Contract

Defines what a customer vertical pack **owns** and what it **never touches**.

## Pack-owned surfaces

All customer-specific behavior lives under `verticals/<slug>/` in the
acquired substrate. A vertical pack may contain:

| Surface | Path | Notes |
|---|---|---|
| Domain definitions | `verticals/<slug>/domains/` | One YAML per workflow_type |
| Orchestrators | `verticals/<slug>/orchestrators/` | Per-domain orchestrator logic |
| Agent skills | `verticals/<slug>/skills/` | Domain-specific Copilot skills |
| Personas | `verticals/<slug>/personas/` | Customer-named ELT + archetypes |
| World seeds | `verticals/<slug>/worlds/` | Actor world, causal stories |
| Process profiles | `verticals/<slug>/profiles/` | Per-process config |
| Reference cases | `verticals/<slug>/cases/` | Golden-path scenario bundles |
| Authority policies | `verticals/<slug>/policies/` | Function/role authority matrix |
| MCP servers | `verticals/<slug>/mcps/` | Customer stack mock MCPs |
| Actions & commands | `verticals/<slug>/actions/` | Typed commands and handlers |
| Durable objects | `verticals/<slug>/durable/` | Durable workflow state |
| Projections | `verticals/<slug>/projections/` | Read-model event projections |
| Recordings | `verticals/<slug>/recordings/` | Replay-proof screen flows |
| UI extensions | `verticals/<slug>/ui/` | Custom drawer/portal components |
| Operations | `verticals/<slug>/operations/` | Deployment / infra overrides |

## Global surfaces — never replaced

The vertical pack never replaces or overwrites global registries,
schemas, or shared infrastructure:

- **Global domain registry** (`api/shared/domains.py`) — vertical
  domains are *registered* there but defined in `verticals/<slug>/`.
- **Global function registry** (`api/shared/functions.py`) — the
  pack adds entries; it never removes or renames existing ones.
- **Global persona registry** (`api/shared/personas.py`) — additive.
- **Core schema / Kuzu entity definitions** — the pack extends; it
  never renames or removes existing entity kinds.
- **Shared skills / MCPs / tools** — the pack may *use* them but
  never modifies their source.
- **Root package manifests** — the pack never edits root
  `package.json`, `pyproject.toml`, or `Makefile` beyond additive
  entries.

> **Rule**: A vertical pack never replaces global registries or
> overwrites global schema. All customization is additive under
> `verticals/<slug>/`.
