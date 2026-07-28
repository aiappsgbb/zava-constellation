# Vertical Pack Contract

**Validated build contract:** `1.0.0`

This companion reference summarizes the acquired substrate's
`docs/superpowers/contracts/VERTICAL-BUILD-CONTRACT.md`. The acquired contract
is authoritative.

## Pack composition root

Customer-specific business behavior lives under `verticals/<slug>/` and is
composed by `verticals/<slug>/manifest.py`. Packs are automatically discovered
from manifest directories.

A pack may own modules and assets for domains, functions, agents, authority,
personas, policies, skills, MCP tools, actor worlds, process profiles, cases,
typed actions, Durable registrations, projections, recordings, and UI
extensions. The exact shape follows the current substrate pack contract; this
reference does not impose one directory layout on every industry.

## Shared surfaces

A vertical never replaces or overwrites global registries or shared
infrastructure.

`api/shared/domains.py`, `api/shared/functions.py`, and equivalent compatibility
modules are read-only active-pack adapters. A vertical never patches them,
another pack, `function_app.py`, or a global business inventory.

An industry-neutral substrate extension is allowed only when the behavior is
not customer-specific and is covered by shared tests. Business behavior remains
pack-owned.

## Generated and bespoke runtime interfaces

Generated and bespoke code use the same canonical substrate interfaces:

- `run_agent_session` for declared agent work and observed tool evidence;
- canonical workflow identity at every Durable checkpoint;
- governance plus persisted HITL recovery context;
- typed command dispatch with idempotency;
- canonical projection identity for API and UI surfaces.

Bespoke code is not permission to create pack-local evidence, governance, or
identity substitutes.

## Rule

Reuse when behavior matches, extend an industry-neutral primitive when multiple
verticals need it, and otherwise write bespoke pack code. Never relabel another
vertical's business behavior.
