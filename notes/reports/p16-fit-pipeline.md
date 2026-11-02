# P16.1 Private LiDAR fit pipeline

Date: 2026-11-02
Status: pipeline implemented and synthetically tested; no real private data used.

## Purpose

Implement the P15 pre-registered fit before the private upload arrives, so the real run
is a command rather than a coding exercise.

## Inputs

- Plot table: `site_identifier`, `x`, `y`, `last_year`, `lorey_height_m`,
  `ba_m2_ha`, `vol_m3_ha`.
- Either a grid feature table (`fragment_id`, `x_center`, `y_center`, `Lhmean`,
  `Lhcv`, `Lhp95`, `CC2m`) or a plot-level feature table.
- Optional cluster table: `site_identifier`, `cluster`.

## Forms

- Lorey height: identity, `Lhp95`.
- Basal area: log, `Lhmean` + `CC2m`.
- Gross volume: log, `Lhmean` + `CC2m`.

Log models apply a Duan smearing correction on the training residuals.

## Checks

- Leave-one-plot-out (LOOCV), the primary descriptive check.
- Leave-one-spatial-cluster-out, using the supplied clusters or connected components
  under `--cluster-distance-m`.
- Optional temporal transfer, for example `--temporal-train-year 2023
  --temporal-test-year 2022`.
- Coefficient stability across LOOCV folds: mean, SD, min, max, and sign changes.

## Cards

`--write-cards` writes `femic.inventory.als.model.v1` cards plus a manifest. If any
coefficient changes sign across LOOCV folds, cards are refused unless
`--force-cards` is passed. A card is research-only and remains private until the P15
and ADR 0007 review gates are satisfied.

## Synthetic test

The test builds 12 plots in four spatial clusters and a matching 25 m feature table.
It checks:

- the three fits;
- LOOCV, spatial-cluster, and temporal metrics;
- stable coefficient signs;
- card schema and manifest.

Run:

```bash
python -m pytest tests/test_fit_inventory_cards.py -q --no-cov
```

## Limits

- The nearest-cell match is not a plot-support extraction. For the real run, prefer a
  plot-level feature table matched to the FAIB plot radius.
- Eight primary plots will make some folds unstable; the pipeline is designed to
  report that, not hide it.
- The synthetic test is not a real calibration.

## Reproduction

```bash
python pipeline/fit_inventory_cards.py \
  --plots /path/to/private/plots.csv \
  --features /path/to/private/features.csv \
  --clusters /path/to/private/clusters.csv \
  --output-dir /path/to/private/fit \
  --temporal-train-year 2023 \
  --temporal-test-year 2022 \
  --min-plots 6 \
  --write-cards
```
