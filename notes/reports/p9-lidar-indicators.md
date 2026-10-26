# P9 LiDAR-Derived Indicators

Phase: P9 / `UBC-FRESH/femic-gnn-instance#45`
Task: P9.1 / `UBC-FRESH/femic-gnn-instance#46`
Branch: `feature/p9-lidar-indicators`
Status: pr-open

## Outcome

The GNN compiled dataset now carries reviewed LiDAR fields on a **bounded
southern pilot**:

- **181** fragments have direct LiDAR overlap.
- **184** blocks have LiDAR support.
- **365** fragments are covered after block-level support is propagated to
  fragments that share a covered block.
- Direct fragment support: **930.62 ha**.
- Unique block support: **978.63 ha**.

This is **not** a GNN-wide LiDAR layer. The public LidarBC coverage only
intersects a small southern part of the AOI. Most GNN fragments remain outside
LiDAR coverage and must retain the coarse DEM/centroid terrain or a future
partner LiDAR source.

## Coverage Evidence

LidarBC discovery over the full GNN AOI:

| Product | Tiles | Notes |
| --- | ---: | --- |
| Point cloud | 755 | Not materialized |
| DEM | 280 | Materialized |
| DSM | 269 | Materialized |
| All discovered | 1,304 | Includes point clouds |

Materialized DEM/DSM:

- **549** tiles, **5.5 GiB**, all checksum-verified.
- No point-cloud payload was downloaded.
- Source tile CRSs are **EPSG:6652** and **EPSG:3157**, despite the selection
  manifest's `native_crs: EPSG:3005` metadata. Reprojection to EPSG:3005 is
  explicit in the GNN builder.

Spatial coverage:

- GNN AOI: **682,155 ha**.
- DEM/DSM tile union inside the AOI: **17,360 ha** (**2.5%**).
- Valid 10 m land inside the AOI: **4,660 ha**.
- Direct fragment support: **181 / 19,366** fragments (**0.9%**), **930.62 ha**
  (**0.37%** of the 250,461 ha support).
- Block support: **184 / 19,366** blocks, **978.63 ha**.

The difference between the tile union and valid land is ocean, inlets, and
nodata. The difference between valid land and fragment support is non-forest
land and fragments outside the LiDAR footprint.

## Build

- GNN strategic grid: **10 m**, 13,438 x 9,009 = **121,062,942 pixels**.
- 1 m DEM/DSM were explicitly reprojected and mean-aggregated to 10 m.
- The 10 m grid is a documented GNN modelling choice, **not** a native LidarBC
  product and not a field-validation dataset.
- Derived products: Horn percent slope and CHM (DSM minus DEM).
- Bundle: `lidarbc-1b7b79757e98cfe5`, version `2026.10.0-gnn-10m`.
- Products: `slope`, `chm`, `canopy`.
- Validation: valid; 3 products; **5,188,965 bytes**.
- Warning: the selection requested `dem` and `dsm`, but the bundle intentionally
  packages only the derived consumer products. DEM/DSM are intermediates and
  would violate the FEMIC plan's source-product `derived` rule at 10 m.

## WS4 Integration

Added fields to `runtime/gnn/matrix`:

- `lidar_slope_valid_pixels`
- `lidar_slope_mean`
- `lidar_slope_p95`
- `lidar_chm_valid_pixels`
- `lidar_chm_mean`
- `lidar_chm_p95`
- `lidar_chm_cover_ge_2`
- `lidar_chm_cover_ge_5`
- `lidar_chm_cover_ge_10`
- `lidar_chm_cover_ge_20`
- `lidar_available`
- `lidar_supported_ha`

The fields are present in both fragment and block tables. Block values are
replicated across track rows; fragments in a covered block inherit the block
support when they do not have direct polygon support.

Dataset backup: `runtime/gnn/matrix_pre_lidar`.

Validation:

- `ws4 validate --dataset runtime/gnn/matrix` passes.
- `Simulator.from_dataset("runtime/gnn/matrix")` loads 26,801 fragments and sees
  the LiDAR fields.
- `curves.parquet`, `treatments.parquet`, `tracks.parquet`, `strata.parquet`,
  `features.parquet`, `products.parquet`, `accounts.parquet`,
  `protoaccounts.parquet`, `groups.parquet`, and `messages.parquet` are
  unchanged versus the backup.
- Only `fragments.parquet`, `blocks.parquet`, and `manifest.json` changed.

### WS4 blocker and fix

The GNN block table has 26,801 rows but 19,366 unique block IDs because a block
can appear on multiple track rows. WS4's LiDAR integration initially forced a
one-to-one block merge and failed. The fix is `UBC-FRESH/ws4#438` / PR #439:
fragment mapping remains one-to-one, block mapping is many-to-one, and a
regression test covers duplicate block rows.

## Limits

- The fields are a **bounded southern pilot**, not GNN-wide terrain.
- 10 m is a strategic aggregation; it is not native 1 m.
- CHM p95 at 10 m can understate fine-scale canopy peaks.
- No VRI comparison, field accuracy, DBH, true stems/ha, biomass, biodiversity,
  or operability conclusion is added.
- No curve, THLB, AAC, price, recovery, or benchmark value is changed.
- The release remains volume-only; no sustainable or model-improvement claim is
  made.

## Next

1. Keep these fields as pilot evidence only; do not use them to infer
   whole-AOI operability or biodiversity.
2. Request partner or provincial LiDAR coverage for the northern GNN AOI, or
   document that the coarse DEM remains the only model-wide terrain.
3. If broader coverage arrives, rebuild the bundle and rerun
   `pipeline/integrate_gnn_lidar.py`; do not edit the delivered bundle in place.
4. Review whether any GNN model/UI should expose `lidar_available` as a coverage
   flag before using the fields in a scenario.
