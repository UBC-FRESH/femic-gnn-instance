# FHOPS marine transport adapter

Date: 2026-10-25
Status: diagnostic implementation; upstream fixture, not GNN geography or a current quote.

> **Geography warning:** the fixture is Sunshine Coast -> Howe Sound. The GNN AOI
> is northern Vancouver Island. This adapter tests the FHOPS marine cost path; it
> does not estimate a GNN barge route. See `notes/reference/gnn-marine-geography.md`.

## Upstream capability

`UBC-FRESH/fhops#187` is closed. The marine/barge path landed in PR #195 as
`f788d7a6`. FHOPS now models a barge as a first-class vessel:

- `TransportMode`, `BargeType`, `Barge`, `Port`, `WaterArc`, `PortLeg`, and
  `MarineRoute`;
- road pickup drayage, origin terminal handling, water leg, destination
  terminal handling, and road delivery;
- Phase I `marine_flows`, `barge_trips`, and `port_inventory`;
- Phase II/III barge-cycle scheduling; and
- a redistributable synthetic Sunshine Coast -> Howe Sound fixture.

## Adapter

`pipeline/fhops_marine_transport.py` loads the FHOPS fixture in
`config/cost_revenue/transport/fhops_marine/`, scales it to an explicit
one-day volume, sizes enough drayage trucks and barges for that day, solves
Phase I, and reports:

- drayage cost;
- barge variable cost;
- terminal handling cost;
- Phase I total;
- contract fixed truck and barge dispatch cost; and
- total cost and cost per m3.

The fixed dispatch cost is added explicitly because FHOPS Phase I charges
variable, handling, and trip cost only; the FHOPS Phase II model charges the
fixed truck and barge costs.

## API fixture cases

The fixture barge capacity is 3,000 m3. The cases vary utilisation, not the
tariff. They are API test cases, not GNN rates:

| Case | Volume | Utilisation | Total CAD/m3 |
| --- | ---: | ---: | ---: |
| Low cost | 3,000 m3 | 100% | 5.642 |
| Base | 2,250 m3 | 75% | 6.100 |
| High cost | 1,500 m3 | 50% | 7.097 |

Run:

```bash
python pipeline/fhops_marine_transport.py \
  --out runtime/p4/fhops_marine_cost.csv
```

The adapter also supports a custom volume:

```bash
python pipeline/fhops_marine_transport.py --volume-m3 3000 --horizon-days 1
```

## Public-route proxy

P6.1 added a separate GNN-specific proxy for the public
Quatsino Sound -> Ladysmith Harbour route. P7.1 switched it from the analytical
workaround to solved FHOPS Phase I after FHOPS P13 landed.

- Path: `config/cost_revenue/transport/fhops_marine_quatsino_ladysmith/`
- Config: `config/cost_revenue/transport/fhops_marine_quatsino_ladysmith.yaml`
- Mode: `solve`
- Results: 8.125 / 9.203 / 11.360 CAD/m3 at 100/75/50% utilisation.
- Status: `public_route_assumption_rates`; not a quote and not the published base.
- Note: `notes/reference/gnn-marine-proxy.md`.

## API screen integration

Both screens keep the legacy CLEWs/FFCM path and add an opt-in FHOPS path:

```bash
python pipeline/screen_net_revenue.py \
  --sample config/cost_revenue/samples/operability_pilot_40.csv \
  --prices runtime/p3/price_deck_reviewed.csv \
  --recovery config/cost_revenue/recovery/recovery_matrix.csv \
  --out runtime/p4/net_revenue_screening_40_fhops.csv \
  --transport fhops-marine
```

```bash
python pipeline/full_thlb_screening.py \
  --checkpoint data/gnn_combined_checkpoint.feather \
  --aoi data/source/aoi/gnn_full.gpkg \
  --prices runtime/p3/price_deck_reviewed.csv \
  --recovery config/cost_revenue/recovery/recovery_matrix.csv \
  --out runtime/p4/full_thlb_screening_fhops_marine.csv \
  --transport fhops-marine
```

Full-THLB API smoke test on 2026-10-25 (not a GNN transport sensitivity):

| Transport path | Low case | Base | High case |
| --- | ---: | ---: | ---: |
| Legacy CLEWs/FFCM | 88.0% | 95.5% | 96.8% |
| FHOPS marine | 90.2% | 95.8% | 97.0% |

The FHOPS path does not change the published screen. It is a separate API
smoke test and remains diagnostic. It is not a GNN distance or cost estimate.
The percentages above must not be cited as GNN transport results.

## Limits

- The FHOPS route, ports, distances, barge cost, truck cost, and terminal
  handling values are synthetic fixture values, not GNN or current quotes.
- The fixture geography is Sunshine Coast -> Howe Sound, not northern Vancouver
  Island. The GNN AOI centroid is about 51.185 N, -127.408 W.
- The GNN instance has no actual barge terminal, road, or water-route inventory.
- The adapter uses one representative day and uncaps terminal storage and daily
  handling for an aggregate lane.
- The adapter sizes a feasible drayage fleet; those trucks are a capacity
  assumption, and the FHOPS Phase I cost is variable plus contract fixed.
- Phase II/III barge sequencing is not used as the cost basis.
- Tides, weather, naval architecture, customs, and a full coastal network are
  out of scope.
- The sustainable gate must still reject this as a current-quote or calibrated
  transport estimate.

## Upstream reference

- Issue: https://github.com/UBC-FRESH/fhops/issues/187
- Merge commit: `f788d7a63113c52159b3a9dbef449d6faf8325e9`
- Fixture: `examples/hauling_marine/scenario.yaml`
