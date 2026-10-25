# Truck and barge transport assumptions

Date: 2026-10-25
Status: provisional assumption contract; no observed carrier quotes.

## Why this exists

The GNN model has no roads, landings, transfer points, or barge terminals. Public
coastal barge tariffs were not found. A transport cost cannot be invented and
presented as observed.

`config/cost_revenue/transport/assumptions.yaml` provides low/base/high ranges
for:

- truck haul (CAD/m3/km and distance),
- barge (CAD/m3),
- terminal handling (CAD/m3).

Every value is `data_status=assumption`.

## Base envelope

At base values (0.12 CAD/m3/km x 100 km, 15 CAD/m3 barge, 4 CAD/m3 terminal),
the transport allowance is approximately:

``12 + 15 + 4 = 31 CAD/m3``

That is an allowance, not a quote. It is large relative to many log grades and
must be replaced with actual road/terminal/carrier data before a net revenue
claim.

## What must replace it

- Road network and landing/transfer locations.
- Barge terminal/route and carrier quotes.
- Distance by road/water, not straight-line.
- Terminal handling and storage charges.
- Season/availability constraints.

The sustainable gate must reject `data_status=assumption` for a sustainable
label.
