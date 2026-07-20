# research-company

Gather source-backed facts and uncertainties about a target
organisation from public web sources. Produce a structured
**org-brief** YAML — the company-specific overlay that pairs with an
industry primer to drive vertical pack composition.

See [`SKILL.md`](SKILL.md) for the canonical procedure.

## Relationship to compose-org

`compose-org` invokes this skill internally during its Phase Research
when pre-approved evidence is not supplied. This skill remains
installed and directly callable for research-only use.

## Files

| File | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | Four-phase procedure. Strict frontmatter (≤1024 char, semver 3.0.0). |
| [`references/brief-schema.md`](references/brief-schema.md) | Authoritative schema for the output YAML. |
| [`references/industry-primers/`](references/industry-primers/) | Canonical industry shorthand per vertical. Canon — do not normalize. |

## What's in scope

A **thin overlay** of company-specific facts. The brief captures only
what an industry primer can't infer:

- Identity, ownership, size, geography
- ~10 subsidiaries (legal entities)
- ~10 named ELT leaders
- 3–5 strategic themes from last 24 months press
- Stack overrides where the company has publicly disclosed

Vertical breadth (function tree, regulator catalogue, entity kinds,
proposed-domain library, rituals, KPI cinematics) lives in the
matching industry primer. `compose-org` reads both at build time.

## Contract boundaries

This skill produces **source-backed facts and uncertainties only**.
It does not create synthetic actors, records, or world state. Every
claim carries confidence + source references. Gaps go in
`uncertainties[]` — never invented.

## What's NOT in scope

- Single-process deep dives → use `threadlight-design`
- Pitch decks → use a deck generator
- Code generation → out of scope for any research skill
- Synthetic actor worlds or seed data → compose-org Phase Build
- Domains / regulators / KPIs / rituals — those are primer canon

## Output

Always writes to `briefs/<slug>-org-brief.yaml` (relative to operator
cwd). `briefs/` is gitignored — per-engagement output stays out of
the public catalog.

Target size: **300–500 lines**. Anything > 800 suggests harvesting
things the primer already covers.

## Changelog

- **3.0.0** (MAJOR) — Updated to reflect compose-org v2 contract.
  Explicit statement that compose-org invokes this skill. Added
  contract boundary: never generates synthetic actors/records.
  Clarified facts/uncertainties/source-refs contract.
- **2.0.0** (MAJOR) — Slimmed to thin-overlay design. Removed
  org_chart[], vertical_entity_kinds[], proposed_domains[],
  regulators[], cadenced_rituals[], kpi_cinematics[], functions[]
  from the brief schema; those live in the primer. Procedure cut
  to 4 phases. Brief target 300–500 lines.
- **1.0.0** — Initial version (thirteen-phase, fat-brief).
