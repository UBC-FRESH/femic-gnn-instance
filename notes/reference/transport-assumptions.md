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

## FHOPS marine path

`UBC-FRESH/fhops#187` is closed. The GNN instance now has an opt-in FHOPS
marine Phase I adapter:

```bash
python pipeline/fhops_marine_transport.py --out runtime/p4/fhops_marine_cost.csv
```

It exercises the FHOPS Sunshine Coast -> Howe Sound fixture at 100%, 75%, and
50% barge utilisation. That fixture is **not** the GNN geography: the GNN AOI is
northern Vancouver Island, while the fixture is southern BC. The cases are API
tests, not GNN transport estimates. The 2026-10-25 base results, including contract fixed
dispatch costs, are:

- low cost: 5.642 CAD/m3 at a full 3,000 m3 barge;
- base: 6.100 CAD/m3 at 2,250 m3; and
- high cost: 7.097 CAD/m3 at 1,500 m3.

The fixture is synthetic and geographically unrelated. It has no GNN terminals,
road network, water distances, or current carrier/terminal quotes. See
`notes/reference/gnn-marine-geography.md`. The legacy path remains the
default published comparison. The screens accept
`--transport fhops-marine` for a separate diagnostic sensitivity.

P6 also provides a separate public-route proxy for Quatsino Sound ->
Ladysmith Harbour, with explicit assumed rates and capacity. It is diagnostic
only and not the published base. See `notes/reference/gnn-marine-proxy.md`.

## What must replace it

- Road network and landing/transfer locations.
- Barge terminal/route and carrier quotes.
- Distance by road/water, not straight-line.
- Terminal handling and storage charges.
- Season/availability constraints.

The sustainable gate must reject `data_status=assumption` and
`upstream_fhops_fixture_api_test` for a sustainable label.
