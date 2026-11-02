# P15.1 Private LiDAR dry run

Date: 2026-11-02
Status: synthetic dry run complete; no private data read.

## Purpose

Prove that the first-return point-cloud feature step works on a LAS/LAZ + DEM pair
before the private upload arrives, and record the FEMIC version requirement.

## Synthetic fixture

- LAS: 12 points in EPSG:3005, proper first-return numbers, 10 m above a flat DEM.
- DEM: 400 x 400 m, 1 m cells, EPSG:3005, origin `(899800, 700400)`.
- Grid: 25 m, `--min-returns 1`.

## Command

The installed FEMIC checkout on this workstation predates the command. Use a FEMIC
checkout at `origin/main` or newer:

```bash
cd /path/to/femic
PYTHONPATH="$PWD/src" python -m femic lidar inventory-pointcloud-features \
  --pointcloud /path/to/synthetic/tile.las \
  --dem /path/to/synthetic/dem.tif \
  --output /path/to/synthetic/features.csv \
  --grid-size-m 25 \
  --min-returns 1
```

`origin/main` at `03ca3a2` includes the command. The local
`feature/inv01-inventory-als` checkout does not.

## Result

- 7 grid cells with first returns.
- Columns: `fragment_id`, `x_center`, `y_center`, `source_tile`, `Lhmean`,
  `Lhcv`, `Lhp95`, `CC2m`, `all_first_returns`, `above2m_returns`,
  `grid_size_m`.
- The 10 m synthetic canopy produced `Lhmean` 10.0, `Lhcv` 0.0, `Lhp95` 10.05,
  and `CC2m` 100 in the populated cells.

## What it proves

- LAS first-return numbers and the DEM normalization path are wired.
- The feature contract is produced before any model card is applied.
- The feature table has the predictors used by the INV-01 cards.

## Limits

- Flat synthetic DEM, 12 points, one tile; this is not a terrain or density test.
- It does not apply a model card or validate an inventory.
- It does not read Ken's private LAZ.

## Next

When the private upload arrives, run the P14 ingest kit first. Then run the same
feature command over the covered area and record the real tile count, CRS, and
returns.
