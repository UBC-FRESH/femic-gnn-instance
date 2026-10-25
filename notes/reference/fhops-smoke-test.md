# FHOPS integration smoke test

Date: 2026-10-25
Status: synthetic smoke test only; no GNN block result.

## Environment

- FHOPS source: sibling `fhops` checkout.
- The package is not installed in the active environment.
- `PYTHONPATH=src` works for the cost core.
- The CLI currently fails without `optuna`; the MIP path also needs `pyomo` and
  `highspy`. Install the FHOPS dependencies before a full scenario run.

## Synthetic cost core test

Using `fhops.costing.machines.estimate_unit_cost_from_stand` with a deliberately
synthetic stand:

| Input | Value |
| --- | ---: |
| Rental rate | 200 CAD/SMH |
| Utilisation | 0.80 |
| Average stem size | 0.5 m3 |
| Volume per ha | 300 m3/ha |
| Stem density | 600 stems/ha |
| Ground slope | 30% |

Result:

- productivity: 45.40 m3/PMH
- single-machine cost: 5.51 CAD/m3

This is **one machine**, not a full harvest system, and the stand values are
synthetic. It proves the cost core runs; it is not a GNN cost estimate.

## Next

1. Install FHOPS dependencies (`optuna`, `pyomo`, `highspy`) or use a dedicated
   FHOPS environment.
2. Map GNN block attributes to the FHOPS stand fields: volume/ha, stem size,
   stems/ha, slope.
3. Run a full ground/cable/heli system for one block, including move-in and
   landing assumptions.
4. Keep the synthetic smoke test separate from any GNN result.
