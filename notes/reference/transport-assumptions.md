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

## Legacy CLEWs/FFCM evidence

`UBC-FRESH/clews-c2070-fresh` documents a legacy log barge:

- 3,000 m3 capacity
- 25 km/h
- 120 CAD/h operating
- 18.345336 CAD/km fuel
- 4.57 CAD/m3 transload

Derived: 0.007715 CAD/m3/km; 100 km barge = 0.7715 CAD/m3; plus transload
= 5.3415 CAD/m3.

The same archive has a BC logging truck:

- 46.1 m3 capacity
- 90 km/h
- 120 CAD/h operating
- 1.257304 CAD/km fuel

Derived: 0.056195 CAD/m3/km; 100 km truck = 5.6195 CAD/m3; plus transload
= 10.1895 CAD/m3.

A 100 km truck + 100 km barge + transload = **10.961 CAD/m3**.

These are **legacy diagnostic values**. The source repository labels them
"rough prototype only" and says the cost year and assumptions are unclear. They
are not current carrier/terminal quotes. See
`notes/reference/clews-transport-costs.md`.

## What must replace it

- Road network and landing/transfer locations.
- Barge terminal/route and carrier quotes.
- Distance by road/water, not straight-line.
- Terminal handling and storage charges.
- Season/availability constraints.

The sustainable gate must reject `data_status=assumption` for a sustainable
label.
