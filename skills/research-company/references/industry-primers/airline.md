# Industry Primer - Airline

> **Status: Unproven seed.**
> This inventory is not a reviewed airline primer. It must be expanded and
> reviewed by `compose-org` during the first airline Design phase before it can
> support a build. Public-source research remains mandatory.

## Sub-segments

| Sub-segment | Examples | Notes |
|---|---|---|
| **Legacy / network carrier** | (national flag carriers, alliance members) | Hub-and-spoke, alliance member. |
| **Low-cost carrier (LCC)** | (point-to-point European / US discount operators) | Point-to-point, secondary airports, ancillaries. |
| **Ultra low-cost (ULCC)** | (US ultra-unbundled carriers, LATAM ULCCs) | Unbundled to the maximum. |
| **Charter / leisure** | (tour-operator-led carriers) | Tour-operator-led. |
| **Cargo-only** | (dedicated freight operators) | No passengers. |
| **Regional** | (sub-200-seat short-haul operators) | Sub-200 routes. |

## Canonical vertical entity kinds

`Route`, `Sector`, `Slot`, `Roster`, `Aircraft`, `Crew`, `Pairing`,
`Booking`, `Bay`, `Gate`, `MROOrder`, `Spare`, `FuelHedge`, `Licence`,
`FrequentFlyer`.

## Canonical regulators

| id | country | domain |
|---|---|---|
| `caa-uk` | GB | aviation |
| `easa` | EU | aviation |
| `faa` | US | aviation |
| `caas` | SG | aviation |
| `dgca-in` | IN | aviation |
| `casa` | AU | aviation |
| `anac-br` | BR | aviation |

## Canonical KPIs

`otp_d0`, `load_factor`, `ask_growth`, `rask`, `cancellation_rate`,
`mro_cycle_time`, `crew_utilisation`, `slot_compliance`, `nps`.

## Gaps before use

The first airline Design phase must add and review actor relationships, causal
dynamics, process families, authority, typed commands, deterministic golden
scenarios, operating distributions, system candidates, and proof status. The
seed must not be treated as evidence that those sections already exist.
