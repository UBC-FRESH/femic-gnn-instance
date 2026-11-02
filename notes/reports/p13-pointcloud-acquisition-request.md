# P13 GNN point-cloud acquisition request

Date: 2026-11-02
Status: request package prepared; no acquisition commitment.

## Why

The P12 audit is a no-go for a GNN-specific first-return inventory from current
public data:

- 24 FAIB plots in the GNN AOI, 8 measured since 2018;
- 755 LidarBC point-cloud tiles covering 1.10% of the AOI;
- no plot inside a point-cloud tile;
- nearest recent plot 32.7 km from the nearest tile.

The CWH cards remain a report-only transfer. A local fit needs point clouds over
the recent plots, or recent plots inside the existing footprint.

## Private upload status

A private LAZ upload for the GNN area is pending from the partner to the UBC ARC
Chinook account. The destination collection is `GNN TSR LiDAR Upload`
(`40487994-e1d0-4b74-bbf5-56a6b4947c80`); `/incoming/` and `/manifests/` were both
empty on 2026-11-02.

The raw point files are private. Derived datasets may be public after review; see
`notes/adr/0007-private-lidar-derived-public.md` and
`notes/reports/p14-ingest-runbook.md`.

This P13 request is a fallback. If the private upload covers a plot, mark that plot
as satisfied and do not request a duplicate public acquisition for it.

## Request

Acquire LidarBC-compatible point clouds over the 8 recent FAIB plots as the high
priority, with the 16 older plots as secondary.

| Priority | Plots | 2 km request footprint |
| --- | ---: | ---: |
| High (measured since 2018) | 8 | 8,661.3 ha union |
| Secondary (older) | 16 | 8,952.6 ha additional |
| All | 24 | 17,613.9 ha union |

Each row in `p13-gnn-pointcloud-acquisition-request.csv` carries the site ID, TSA,
BEC, last visit, EPSG:3005 coordinates, nearest existing tile distance, and a
2 km request bbox. The per-plot bbox is 1,600 ha; the union removes overlap.

High-priority plots:

| Site | BEC | Last visit | Nearest existing tile |
| --- | --- | ---: | ---: |
| 4028484 | CWH vm | 2023 | 32.7 km |
| 4028476 | CWH vm | 2023 | 33.6 km |
| 4028460 | CWH vh | 2023 | 37.2 km |
| 4028464 | CWH vh | 2023 | 37.4 km |
| 4028474 | CWH vm | 2022 | 38.9 km |
| 4028475 | CWH vm | 2022 | 38.9 km |
| 4028471 | MH wh | 2023 | 40.3 km |
| 4028500 | CWH vm | 2022 | 56.2 km |

## Specification

- Point cloud: classified LAS/LAZ, first returns retained, with acquisition date,
  point density, CRS, and vertical datum.
- DEM/DSM: 1 m where available, co-registered with the point cloud.
- Extent: the 2 km request bboxes in the CSV; a single merged tile set is fine.
- CRS: native LidarBC CRS accepted; EPSG:3005 preferred for the delivered mosaic.
- Transfer: Globus to the existing GNN/Chinook collection, with a SHA-256 manifest.
- Metadata: contract/project ID, acquisition dates, sensor, density, classification
  scheme, and any known vertical-datum limitation.

## What it unblocks

A bounded first-return feature table over the 8 recent plots, a local fit with a
spatial or temporal holdout, and a comparison with the P11 CWH transfer. Eight plots
is still a small pilot; the result would be research-grade, not operational.

## Limits

- The 2 km bbox is an acquisition footprint, not a guarantee of usable density.
- The recent plots are 2022-2023; the point cloud must be time-matched to those
  visits, not to the 2019 footprint.
- A partner may have a different boundary, priority, or acquisition window.
- No point cloud has been requested, downloaded, or processed by this package.

## Files

- `notes/reports/p13-gnn-pointcloud-acquisition-request.csv`
- `notes/reports/p13-pointcloud-acquisition-request.md`
- Source audit: `notes/reports/p12-pointcloud-inventory-feasibility.md`
