# P16 private LiDAR fit runbook

Date: 2026-11-02
Status: ready; no real private data used.

## Preconditions

- P14 ingest audit passed and the raw LAZ is private.
- At least 6 of the 8 primary plots are covered by the private point cloud.
- The P15 fit/pre-registration is reviewed.

## Build plot-level features

Use the FEMIC checkout at `origin/main` or newer:

```bash
PYTHONPATH="$FEMIC_SRC/src" python -m femic lidar inventory-pointcloud-features \
  --pointcloud <private-laz-or-tiles> \
  --dem <co-registered-dem> \
  --output <private>/features_25m.csv \
  --grid-size-m 25 \
  --min-returns 10
```

For the real fit, prefer a plot-support feature table matched to the FAIB plot radius
rather than the nearest 25 m cell.

## Fit

```bash
python pipeline/fit_inventory_cards.py \
  --plots <private>/plots.csv \
  --features <private>/features_25m.csv \
  --clusters <private>/clusters.csv \
  --output-dir <private>/fit \
  --temporal-train-year 2023 \
  --temporal-test-year 2022 \
  --min-plots 6 \
  --write-cards
```

Outputs under `<private>/fit`:

- `fit_summary.json` — LOOCV, spatial-cluster, temporal metrics, stability;
- `predictions.csv` — observed/predicted rows with the design label;
- `cards/` — only if `--write-cards` and coefficient signs are stable;
- `cards/manifest.json` — card hashes.

## Review

- Check the LOOCV and spatial-cluster RMSE/bias and the per-fold coefficient signs.
- If a sign flips, do not force cards; publish the evaluation only.
- Compare with the CWH cards and the P11 transfer diagnostic.
- The result is research-only. Eight plots cannot support an operational card.

## Publication gate

Before publishing any derived product:

1. get the partner's written permission;
2. record the source/licence note;
3. confirm no raw filename, private path, or point payload is included;
4. label the product research-only and cite ADR 0007.

Raw LAZ and private manifests are never committed.
