# P12.1 GNN point-cloud inventory feasibility

Date: 2026-11-02
Status: audit complete; **no-go** for a GNN-specific first-return inventory pilot
from the current public data.

## Purpose

Decide whether the GNN AOI has enough public FAIB plots and LidarBC point-cloud
coverage to justify a local first-return inventory. This audit does not download
tiles, fit a card, rebuild the matrix, or change the model.

## Inputs

- GNN AOI: `data/source/aoi/gnn_full.gpkg` (682,155.0 ha).
- Public FAIB plot header and visit table.
- Existing LidarBC selection manifest: `metadata/lidar/lidarbc_selection.json`.

## Results

| Item | Result |
| --- | ---: |
| FAIB plots inside the GNN AOI | 24 |
| CWH / MH plots | 22 / 2 |
| PSP_G / PSP_R plots | 7 / 17 |
| Plots measured since 2018 | 8 |
| LidarBC point-cloud tiles | 755 |
| Point-cloud acquisition years | 2019 (319), 2023 (382), 2024 (54) |
| Point-cloud bounding-box footprint inside the AOI | 7,486.8 ha |
| Footprint share of the AOI | 1.10% |
| Plots inside any point-cloud tile | 0 |
| Recent plots inside any point-cloud tile | 0 |
| Nearest recent plot to a point-cloud tile | 32.7 km |
| Median recent-plot distance | 38.1 km |
| Farthest recent plot | 56.2 km |

All 24 plots are in TSA 46 (GBR North); the point-cloud footprint is a small
southern subset of the AOI. The two layers do not overlap at any plot.

## Decision

**No-go for a GNN-specific first-return pilot from current public data.**

A local fit needs co-located plots and point clouds. The current public data have
24 FAIB plots and 8 recent plots, but none is inside or near the 1.1% point-cloud
footprint. The nearest recent plot is 32.7 km away.

To make the pilot defensible, one of these must happen:

1. Acquire LidarBC or partner point clouds over the 8 recent plots (or all 24
   plots) and pair them with the plot visits.
2. Add recent FAIB or partner plots inside the existing point-cloud footprint.
3. Keep the CWH transfer as a report-only diagnostic, as P11 does, and do not
   present it as a GNN calibration.

## Limits

- The footprint is the union of tile bounding boxes clipped to the AOI. It is an
  upper bound, not valid-pixel or first-return coverage.
- The FAIB header may not include every non-PSP plot; the GNN non-PSP sample is a
  separate evidence layer.
- Plot counts are site-level; the P11 diagnostic used 25 m cells, not plots.
- The audit does not assess point-cloud quality, point density, or ground returns.

## Reproduction

```bash
python pipeline/pointcloud_inventory_feasibility.py \
  --aoi data/source/aoi/gnn_full.gpkg \
  --plots <faib_plot_header.csv> \
  --visits <faib_sample_byvisit.csv> \
  --selection metadata/lidar/lidarbc_selection.json \
  --output notes/reports/p12-pointcloud-inventory-feasibility.json
```

The machine-readable summary is `notes/reports/p12-pointcloud-inventory-feasibility.json`.
