# Industry Primer — Retail (Fashion / Apparel focus)

> **Canon — see [AGENTS.md § 2.2](../../../../AGENTS.md#22--reference-data-files-are-canon--do-not-normalize).**
> Do not normalize the published shorthand documented here.

A starting-point cheat sheet for the `research-company` skill when
the target is a fashion/apparel retailer (vertically-integrated
specialty, fast-fashion, or multi-brand group). Extends to general
retail where noted.

**Status: design canon, unproven until a clean Fashion compose-org
acceptance run completes end-to-end.**

---

## Sub-segments

| Sub-segment | Examples | Notes |
|---|---|---|
| **Fast-fashion** | (high-turnover, trend-led, 4–8 week design-to-shelf) | Speed-to-market KPI dominant. |
| **Vertically-integrated specialty** | (own-brand, own-manufacture, DTC + wholesale) | Full supply-chain visibility. |
| **Multi-brand group** | (portfolio of owned/licensed brands, shared logistics) | Brand P&L autonomy vs shared ops. |
| **Premium / luxury** | (heritage brands, limited-run, high margin) | Clienteling and allocation dominant. |
| **Pure-play e-commerce** | (marketplace or vertical DTC, no physical stores) | Fulfilment and returns dominant. |

General retail extension: Grocer, General-merch, DIY/Home, QSR
follow similar entity structures but differ in replenishment cadence
and regulatory load.

---

## Canonical vertical entity kinds (actor/entity set)

| Kind | Meaning |
|---|---|
| `Customer` | End consumer — loyalty member or anonymous basket. |
| `Store` | Physical retail location (flagship, mall, outlet, concession). |
| `DistributionCentre` | DC / warehouse / fulfilment centre. |
| `Supplier` | Tier-1 manufacturer, fabric mill, trim supplier. |
| `Product` | Design-level item (style + colourway). |
| `SKU` | Size/colour variant of a Product — the stockable unit. |
| `Inventory` | Stock-on-hand record: SKU × Location × quantity. |
| `Order` | Customer purchase (online or in-store POS transaction). |
| `Promotion` | Price markdown, campaign bundle, loyalty offer. |
| `Return` | Reverse-logistics unit (refund, exchange, repair). |
| `Range` | Seasonal collection or capsule grouping of Products. |
| `Replenishment` | Auto-stock transfer request from DC to Store. |
| `Allocation` | Initial push of new-season stock from DC to Store. |
| `PurchaseOrder` | Outbound order to Supplier for production. |
| `Shipment` | Inbound or inter-location freight movement. |

---

## Connected causal story — "New Season Drop"

A realistic end-to-end scenario connecting actors and processes:

1. **Merchandising** creates a Range (Spring/Summer capsule) and
   selects 120 Products across 4 themes.
2. **Buying** issues PurchaseOrders to 8 Suppliers; lead time 10–14
   weeks.
3. **Suppliers** confirm and ship; Shipments arrive at 2 DCs.
4. **Allocation** engine pushes initial stock to 85 Stores based on
   cluster profile (urban-flagship gets 2× depth vs outlet).
5. **Stores** receive, merchandise floor, update planograms.
6. **Customers** purchase; Orders flow through POS and e-commerce.
7. **Replenishment** fires nightly for SKUs below safety-stock at
   each Store.
8. **Promotions** trigger at week 6 for slow-movers (markdown
   cadence: 20% → 40% → 60%).
9. **Returns** feed reverse-logistics; re-stockable units re-enter
   Inventory.
10. **End-of-season** — remaining stock flows to outlet channel or
    third-party off-price.

This story exercises: Product lifecycle, supply chain, allocation,
replenishment, promotions, returns — all connected through shared
Inventory state.

---

## Candidate hero processes (≤3 per engagement)

| Process | Function | Why hero |
|---|---|---|
| `allocation-to-store` | Merchandising | High-impact, visual, connects buying → store floor. |
| `markdown-optimisation` | Commercial / Pricing | Revenue-critical, cadenced, measurable. |
| `order-to-delivery` | Operations / E-commerce | Customer-facing, SLA-driven, cross-functional. |

## Shared process families

Related processes that share engines/skills/MCPs but each has a
distinct trigger, profile, typed command, world case, and success
evidence:

| Family | Processes | Shared engine |
|---|---|---|
| Inventory management | `replenishment`, `stock-transfer`, `stock-count`, `shrinkage-write-off` | Inventory projection engine |
| Order lifecycle | `order-to-delivery`, `click-and-collect`, `return-to-restock` | Order state machine |
| Range planning | `range-build`, `allocation-to-store`, `de-range` | Allocation engine |
| Pricing | `initial-price-set`, `markdown-optimisation`, `promo-activation` | Price-decision engine |
| Supplier management | `purchase-order-create`, `supplier-onboard`, `quality-inspection` | Supplier gateway MCP |

---

## Realistic distributions

| Dimension | Fashion typical | General retail extension |
|---|---|---|
| Stores | 50–500 (specialty) / 1,000–5,000 (fast-fashion) | 200–15,000 (grocer) |
| SKUs active | 20,000–80,000 | 50,000–500,000 |
| Orders/day | 10,000–200,000 (omni) | 500,000–5,000,000 (grocer) |
| Suppliers | 50–300 | 500–5,000 |
| DCs | 2–8 | 5–40 |
| Markdown cycles/season | 3–5 | 1–2 (grocer: continuous) |
| Return rate | 15–35% (online), 5–8% (store) | 2–5% (grocer) |
| Range refresh | 4–12 drops/year | 1–2 major resets/year |

---

## Typed commands and success evidence examples

| Typed command | Domain | Success evidence |
|---|---|---|
| `AllocateRange { range_id, store_cluster, depth_multiplier }` | allocation-to-store | Allocation records created for every Store in cluster; Inventory projections updated; no over-allocation vs available DC stock. |
| `ApplyMarkdown { sku_ids[], percentage, effective_date }` | markdown-optimisation | Price records updated; POS systems reflect new price by effective_date; margin impact projected. |
| `FulfilOrder { order_id, ship_from }` | order-to-delivery | Shipment created; Inventory decremented at ship_from location; customer notification dispatched; SLA timer started. |
| `RaiseReplenishment { store_id, sku_id, qty }` | replenishment | Transfer order created at DC; Inventory reserved; expected delivery date calculated. |
| `CreatePurchaseOrder { supplier_id, sku_ids[], quantities[], delivery_date }` | purchase-order-create | PO issued to Supplier; confirmation expected within SLA; Inventory pipeline updated. |
| `ProcessReturn { order_id, sku_id, reason, disposition }` | return-to-restock | Return logged; refund/exchange initiated; if re-stockable, Inventory incremented at receiving location. |

---

## Deterministic golden scenarios

Scenarios with fixed seeds and expected outcomes for proof runs:

### Golden scenario 1: "Capsule allocation"

- **Seed**: Range R-2025-SS-01 with 12 Products, 48 SKUs.
  DC-NORTH holds 4,800 units. Store cluster URBAN-FLAGSHIP (5 stores).
- **Command**: `AllocateRange { range_id: "R-2025-SS-01", store_cluster: "URBAN-FLAGSHIP", depth_multiplier: 1.0 }`
- **Expected outcome**: Total allocation of 4,800 units distributed evenly
  across 5 stores = 960 units per store, distributed across 48 SKUs
  proportionally (20 units per SKU per store). Inventory at DC-NORTH
  decremented by 4,800 total. No SKU receives negative allocation.

### Golden scenario 2: "Week-6 markdown"

- **Seed**: 15 slow-mover SKUs, sell-through < 40% at week 6.
  Current price £49.99.
- **Command**: `ApplyMarkdown { sku_ids: [15 ids], percentage: 20, effective_date: "2025-03-15" }`
- **Expected outcome**: New price £39.99 for all 15 SKUs. Price
  change records created with audit trail. Projected margin remains
  above floor (cost + 10%).

### Golden scenario 3: "Express order fulfilment"

- **Seed**: Order ORD-00042, 2 items, Customer in London zone,
  Store FLAGSHIP-LON has both SKUs in stock.
- **Command**: `FulfilOrder { order_id: "ORD-00042", ship_from: "FLAGSHIP-LON" }`
- **Expected outcome**: Shipment SHP-00042 created. Inventory at
  FLAGSHIP-LON decremented by 2. SLA timer = 120 minutes
  (express same-day). Customer notification dispatched.

---

## Canonical functions

| Function id | display_name | importance heuristic |
|---|---|---|
| `merchandising` | Merchandising & Range | **hero** (fashion-led retailers) |
| `buying` | Buying & Sourcing | core |
| `commercial` | Commercial & Pricing | core (hero if margin-focused) |
| `ecommerce-ops` | E-commerce Operations | core |
| `store-ops` | Store Operations | core |
| `supply-chain` | Supply Chain & Logistics | core |
| `marketing` | Marketing & CRM | core |
| `finance` | Finance | core |
| `hr` | People | core |
| `tech` | Technology | core |
| `legal` | Legal & Compliance | support |
| `property` | Property & Estates | support |

---

## Canonical regulators

| id | country | domain |
|---|---|---|
| `cma-uk` | GB | competition |
| `dg-comp` | EU | competition |
| `ftc` | US | competition |
| `ico-uk` | GB | data-protection |
| `edpb` | EU | data-protection |
| `trading-standards` | GB | consumer-protection |
| `cpsc` | US | product-safety |
| `reach-eu` | EU | chemicals-in-textiles |
| `hmrc` | GB | customs-duty |
| `cbp` | US | customs-duty |

---

## Canonical KPIs

`like_for_like_sales`, `gross_margin`, `sell_through_rate`,
`inventory_turnover`, `stockout_rate`, `shrinkage_rate`,
`full_price_sell_through`, `markdown_penetration`, `nps`,
`basket_size`, `units_per_transaction`, `online_share`,
`return_rate`, `availability`, `weeks_of_cover`.

---

## Proof status

This primer is **design canon, unproven**. It defines the reference
entity set, causal stories, process families, typed commands, and
golden scenarios for Fashion/Apparel retail verticals. It has not
yet been validated by a clean end-to-end `compose-org` acceptance
run.

Proof requires:
- A complete compose-org run targeting a Fashion retailer.
- All golden scenarios pass deterministically.
- The live causal chain (actor world → sensor → objective → Durable
  → HITL → typed command → world mutation → evaluation) completes.
- Evidence bundle generated at `verticals/<slug>/proof/`.

Until that run completes, treat distributions, golden outcomes, and
process family boundaries as best-effort design guidance subject to
revision during the first real build.
