Inventory pilot
===============

This page records the report-only diagnostic that applies the published FEMIC
CWH INV-01 model cards to the bounded GNN LiDAR pilot. It does **not** add an
operational inventory and does not change the GNN model.

.. warning::

   The CWH cards are 14-plot regional pilots fitted with CHM proxies in CWH
   northern Vancouver Island. They are not a GNN-specific calibration. The GNN
   input is a 10 m strategic CHM over a bounded southern pilot, not a native 1 m
   product or a first-return point cloud. Do not use these predictions for
   operability, THLB, AAC, WS4, or FHOPS decisions.

Inputs
------

- Bundle ``lidarbc-1b7b79757e98cfe5`` / ``2026.10.0-gnn-10m``.
- Cards under ``config/inventory/models/als_cwh_*_2026.json``.
- Pins and caveats in ``config/inventory/cwh_pilot.yaml``.
- Pipeline entry point ``pipeline/cwh_inventory_diagnostic.py``.

Run
---

.. code-block:: bash

   python pipeline/cwh_inventory_diagnostic.py \
     --bundle data/lidar/products/lidarbc-gnn-10m \
     --output-dir build/cwh_inventory_diagnostic

The command derives a 25 m CHM feature table, filters each card to its declared
predictor ranges, applies the three cards, and writes a JSON summary. When the
fragment geometry and compiled matrix are available, it also writes a
descriptive fragment-level VRI comparison.

Result
------

The 25 m feature table has 22,139 cells. After range filtering, the cards retain
21,666 height cells and 21,995 basal-area/volume cells. The joined footprint is
181 fragments, 181 blocks, and 1,317.8 ha by cell area.

At fragment level the VRI comparison is weak: height bias +3.56 m with RMSE
5.90 m and correlation -0.027; volume bias +57.82 m3/ha with RMSE 284.99 m3/ha
and correlation -0.062. The VRI is a conventional inventory, not independent
field validation.

Limits
------

- 14 training plots, CHM proxies, and a small LiDAR pilot.
- Predictor-range cells only; no extrapolation.
- No GNN-specific fit and no spatial holdout.
- No model, curve, THLB, AAC, target, or schedule change.
- Report-only; not an operational inventory.

Full evidence: ``notes/reports/p11-cwh-inventory-diagnostic.md``.
