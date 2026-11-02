# P11.1 CWH inventory diagnostic on the GNN LiDAR pilot

Date: 2026-11-02
Status: diagnostic complete; report-only, not an operational inventory.

## Purpose

Apply the published FEMIC INV-01 CWH pilot cards to the existing bounded GNN
LiDAR pilot and record what the result does and does not support. This does not
refit a card, change the LiDAR bundle, rebuild the GNN matrix, or change a
curve, THLB, AAC, target, schedule, or release value.

## Inputs

- Bundle: `lidarbc-1b7b79757e98cfe5` / `2026.10.0-gnn-10m`
  (`data/lidar/products/lidarbc-gnn-10m`).
- Grid: 25 m, `min_cover_pct=34.5`.
- Cards, copied from FEMIC `origin/main`:
  - `config/inventory/models/als_cwh_lorey_height_2026.json`
    (SHA-256 `59e23df2...`)
  - `config/inventory/models/als_cwh_basal_area_2026.json`
    (SHA-256 `3aee425e...`)
  - `config/inventory/models/als_cwh_gross_volume_2026.json`
    (SHA-256 `2dde2935...`)
- Config: `config/inventory/cwh_pilot.yaml`.
- Entry point: `pipeline/cwh_inventory_diagnostic.py`.

The cards are the local CWH pilot fits: 14 FAIB PSP plots in CWH northern
Vancouver Island, LidarBC 2023/2024 CHM proxies, 0-2 year plot/LiDAR offset.
They are regionally relevant to the GNN AOI but are not a GNN-specific
calibration.

## Method

1. Validate the bundle with `femic lidar inspect`.
2. Derive a 25 m CHM feature table with `femic lidar inventory-features`
   (`--grid-size-m 25 --min-cover-pct 34.5`).
3. Filter each cell to the card's declared predictor ranges:
   - height: `Lhp95` in `[4.6541, 56.0259]`;
   - basal area and volume: `Lhmean` in `[2.941, 42.0214]` and `CC2m` in
     `[34.4388, 100.0]`.
4. Apply each card with `femic lidar inventory` and `--fragment-id-field
   fragment_id`.
5. Join the cell predictions to the P9 fragment geometry and compare them with
   the compiled VRI attributes. The VRI comparison is descriptive.

## Reproduction

```bash
python pipeline/cwh_inventory_diagnostic.py \
  --bundle data/lidar/products/lidarbc-gnn-10m \
  --output-dir build/cwh_inventory_diagnostic
```

When the fragment geometry and compiled matrix are not in the working tree,
pass them explicitly:

```bash
python pipeline/cwh_inventory_diagnostic.py \
  --bundle data/lidar/products/lidarbc-gnn-10m \
  --output-dir build/cwh_inventory_diagnostic \
  --fragments output/patchworks_gnn/fragments_merged/fragments.shp \
  --vri-fragments runtime/gnn/matrix/fragments.parquet
```

The command took 76 s on the local workstation. It wrote no tracked data;
`build/` and `data/lidar/` are gitignored.

## Results

Feature table: **22,139** 25 m cells.

| Card | Retained cells | Dropped by range | Mean | Median | Min | Max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CWH Lorey height (m) | 21,666 | 473 | 16.24 | 15.38 | 6.32 | 43.80 |
| CWH basal area (m2/ha) | 21,995 | 144 | 42.29 | 41.30 | 12.74 | 95.78 |
| CWH gross volume (m3/ha) | 21,995 | 144 | 361.64 | 310.66 | 41.45 | 1,683.81 |

Fragment join: **21,085** cells fall inside **181** fragments and **181**
blocks, a cell-area footprint of **1,317.8 ha**. This is not the P9 direct
LiDAR support (930.62 ha / 181 fragments / 184 blocks); it counts 25 m cell
centres that fall inside fragment polygons and is used only for the descriptive
comparison.

### VRI comparison at fragment level

| Attribute | Fragments | Predicted mean | VRI mean | Bias | RMSE | Correlation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Lorey height (m) | 181 | 16.14 | 12.58 | +3.56 | 5.90 | -0.027 |
| Gross volume (m3/ha) | 181 | 355.97 | 298.15 | +57.82 | 284.99 | -0.062 |

The VRI is a conventional interpreted inventory, not independent field truth.
The weak correlation and positive bias are the same pattern the GNN P9 work
recorded for VRI height: the comparison is a screening check, not validation.

## Forest-condition card

`notes/reports/gnn-forest-condition-2026.json` and `.md` publish the diagnostic as a
`ws4.forest_condition.report.v1` card. It carries the CWH BA diagnostic mean
(42.29 m2/ha), the card's 9.27 m2/ha LOOCV RMSE, the 21,995 in-range cells, the
181-fragment / 184-block / 979 ha LiDAR pilot coverage, and two advisory alerts.
The card is `draft` and report-only; it does not change the model or become an
operational early-warning product.

## Limits

- The CWH cards use 14 training plots and CHM proxies. They are regional pilots,
  not a GNN calibration and not an operational model.
- The GNN input is a 10 m strategic CHM derived from LidarBC DEM/DSM. It is not
  a native 1 m product and not a first-return point cloud.
- The LiDAR pilot is a bounded southern subset (181 direct fragments / 184
  blocks / 979 ha), not a GNN-wide layer.
- The VRI comparison is not an independent P48/P49 field validation.
- Predictions are better where canopy cover is inside the card range; cells
  outside the range are dropped rather than extrapolated.
- No prediction enters the GNN matrix, curves, THLB, AAC, targets, schedule, or
  release label.

## Decision

Keep this as a report-only diagnostic. Do not promote the CWH cards as a GNN
inventory. A defensible next step, if the pilot is worth continuing, is to
materialize the discovered point clouds over a bounded GNN block, derive
first-return metrics, and fit a GNN-area card with a spatial holdout before any
WS4/FHOPS use. The TSA 23 INV-01 runbook is the reference workflow for that
step.
