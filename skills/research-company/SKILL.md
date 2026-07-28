---
name: research-company
description: >
  Gather source-backed facts and uncertainties about a target
  organisation from public web sources. Produces a thin org-brief
  YAML — the company-specific overlay that pairs with an industry
  primer. compose-org invokes this skill internally during Phase
  Research when pre-approved evidence is not supplied. Also directly
  callable for research-only use. Facts carry confidence + source
  refs; gaps go in uncertainties[]. This skill never generates
  synthetic actors, records, or world state — those are Build
  concerns.
  USE FOR: profile a company before compose-org, research-only
  exploration, generate an org-brief.
  DO NOT USE FOR: single-process design (use threadlight-design),
  pitch decks, code generation, building actor worlds.
metadata:
  version: "3.1.0"
---

# research-company

Profile an organisation from public web sources and produce a **thin**
org-brief YAML — the company-specific facts that an industry primer
can't infer.

## Relationship to compose-org

`compose-org` invokes this skill internally during its Phase Research
when the operator does not supply pre-approved evidence. This skill
remains installed and directly callable for research-only use — it is
not a required account-team step, but is always available as the
research engine.

## Contract boundaries

This skill produces **source-backed facts and uncertainties only**.
It does not generate synthetic actors, records, or world state.
Synthetic actor worlds, causal stories, and seed data are the
responsibility of compose-org's Phase Design and Phase Build — never
this skill.

Every factual claim requires:
- A confidence level (`high`, `medium`, `low`)
- One or more source references (URL, accessed date, kind)

Gaps and unknowns go in `uncertainties[]` — never invented or
filled with plausible-sounding fiction.

## Mental model

```
  industry primer        +        org brief         =     fork inputs
  (vertical canon)                (this skill)            (compose-org reads both)
  ───────────────────────         ──────────────────
  • function tree                 • identity (name, brand voice)
  • regulator catalogue           • ownership + size + geo
  • entity-kind set               • ~10 subsidiaries
  • proposed-domain library       • ~10 named ELT leaders
  • stack vendor candidates       • 3–5 strategic themes
  • rituals + KPI cinematics      • stack overrides (when public)
                                  • narrative-arc seeds (recent press)
```

If a vertical primer exists in
[`references/industry-primers/`](references/industry-primers/), the
research run is **thin** — 30–45 minutes of web work, ~300–500 lines
of YAML. If no usable primer exists, record the missing industry-model sections and
return the gap to `compose-org`. The controller decides whether to expand an
existing seed or author and review a new primer during Design. Do not expose a
separate prerequisite workflow to the operator and do not invent missing
industry facts inside the org brief.

## When to use

- Profile a target organisation before a customer pilot or workshop
- Called automatically by compose-org during Phase Research
- Standalone research exploration (no build intended)
- Produce a reviewable spec a customer SME can sanity-check

## Output convention

```
briefs/<slug>-org-brief.yaml
```

where `<slug>` is the kebab-case form of the target's short name
(≤ 16 chars). `briefs/` is gitignored — per-engagement output stays
out of the public skill catalog.

## Tooling priority

For every factual claim, point at one or more rows in `sources[]`,
gathered via:

1. **`web_fetch` against the target's own properties** — `/about`,
   `/leadership`, latest annual report or capital-markets-day PDF,
   `/press` or `/newsroom`, `/governance`. Self-reported data is
   `confidence: medium` unless cross-corroborated.
2. **`web_search` for cross-corroboration** — two independent
   secondary sources concurring lifts to `confidence: high`.
3. **`web_fetch` against authoritative third parties** — Wikipedia,
   national company registry (Companies House / SEC EDGAR / etc.),
   regulator filings, news of record.
4. **`web_search` for stack-override signal** — vendor case studies
   where the target's logo appears, recent partnership press.

Never rely on a single answer-engine summary.

## Output schema

The output conforms to [`references/brief-schema.md`](references/brief-schema.md).
The schema is **deliberately thin** — only the company-specific
sections are required. Industry-standard sections (functions,
entity kinds, proposed domains, regulators, rituals, KPIs) are
**optional** in the brief; `compose-org` reads them from the primer
when absent.

Key rules:

- Every `Fact` requires `{value, confidence, source_refs?, notes?}`.
- Every `Source` row needs `{id, url, accessed, kind, used_for}`.
- Truly-missing fields go in `uncertainties[]`.
- `meta.status` walks `in_progress` → `needs_review` → `ready`.

## The four phases

### Phase 0 — Bootstrap

Create `briefs/<slug>-org-brief.yaml` with skeleton keys + empty
arrays. Pick the matching reviewed primer. If none is usable, return the
explicit gap to `compose-org` and wait for its Design-stage industry-model
decision.

### Phase A — Identity, ownership, size, geography (10 min)

Sources: Wikipedia + `/about` + last annual report. Fill:

- `identity.{name, short_name, slug, domain, description,
  brand_voice, industry, sub_industry, tagline}`
- `ownership.{structure, parent, ticker, founded, key_shareholders}`
- `size.{employees, revenue_usd, revenue_currency, revenue_period,
  customers_count, assets_count}`
- `geo.{hq, regions, countries_present, key_hubs, footprint_notes}`

### Phase B — Subsidiaries + leadership (15 min)

- `subsidiaries[]`: walk the national registry. Cap at 15.
- `leadership[]`: publicly-named ELT from `/leadership`, 8–15 rows.

### Phase C — Strategic themes + stack overrides (10 min)

- `strategic_themes[]`: 3–5 themes from last 24 months press.
- `stack_overrides[]`: ONLY publicly disclosed systems.

### Phase D — Cross-check & finalise (5–10 min)

Pick three `confidence: high` claims at random. Re-run `web_search`
and confirm. Downgrade any that don't recheck. Validate against
schema. Set `meta.status` → `needs_review`.

## Output budget

A thin org-brief lands at **300–500 lines of YAML**. Anything > 800
suggests harvesting things the primer already covers — stop and trim.

## Iterating the skill

When a generated brief looks wrong, **fix this SKILL.md or the
matching primer**, not the brief. Two runs against the same target
should diff to nothing meaningful except `accessed` dates.

## Downstream

Once `meta.status: ready`, `compose-org` reads the brief + primer
and builds the vertical pack. The brief provides company facts; the
primer provides vertical breadth.
