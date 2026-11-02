# P15.2 GNN private LiDAR fit and publication pre-registration

Date: 2026-11-02
Status: pre-registered before the private data arrive. No model has been fit.

## Data

- Primary: the 8 FAIB plots measured since 2018 (5 in 2023, 3 in 2022):
  `4028484`, `4028476`, `4028460`, `4028464`, `4028474`, `4028475`, `4028471`,
  `4028500`.
- BEC: 7 CWH (vm/vh) and 1 MH (wh).
- Secondary: the 16 older plots. They are used only for sensitivity, not the primary
  fit.
- Predictors: `Lhmean`, `Lhcv`, `Lhp95`, `CC2m` from first-return point clouds.
- Responses: Lorey height, basal area, gross volume from live trees DBH >= 9.1 cm,
  following the INV-01 card definitions.

## Model forms

Pre-register the same forms as the CWH pilot for comparability:

- Lorey height: identity, `Lhp95`.
- Basal area: log, `Lhmean` + `CC2m`.
- Gross volume: log, `Lhmean` + `CC2m`.

`Lhcv` and interaction terms are sensitivity checks, not primary predictors. Any
change to the primary form is a protocol deviation and must be recorded.

## Holdout design

1. **Primary: leave-one-plot-out (LOOCV).** Descriptive only; it is not independent
   validation.
2. **Secondary: leave-one-spatial-cluster-out.** Pre-registered clusters:
   - A: `4028484`, `4028476`
   - B: `4028460`, `4028464`
   - C: `4028474`, `4028475`, `4028471`
   - D: `4028500`
   Each fold trains on the other three clusters. Cluster D has one plot, so its fold
   is a stress test, not a stable estimate.
3. **Tertiary: temporal transfer.** Train on the 5 plots measured in 2023 and test on
   the 3 measured in 2022. Report it as a small temporal check, not a validation set.

Any other split is exploratory.

## Acceptance and interpretation

- Report LOOCV and spatial-cluster RMSE, bias, and R2 for every attribute.
- Report the per-cluster fold results and the temporal transfer separately.
- Report the coefficient stability across folds; unstable signs are a stop signal.
- Compare with the published CWH cards and the P11 transfer diagnostic.
- **Research-grade** means the errors and holdouts are reported with all caveats.
- **Operational** is not available from 8 plots. It requires an independent P48/P49
  or partner plot set, a spatial holdout, and partner review.
- If the coefficients are unstable, publish the evaluation only, not a model card.

## Derived-public products

Public after review, under ADR 0007:

- P14 coverage summary and the `tile_id` tile index;
- derived DEM/DSM/CHM and first-return feature tables without raw filenames;
- the 25 m inventory prediction raster/table, labelled research-only;
- the model card and validation summary, if the fit is stable;
- the fit/holdout report and provenance note.

Private, never published:

- raw LAS/LAZ and private manifests;
- source filenames and private path listings;
- point-level records;
- any partner-restricted table.

Publication requires the partner's written permission, a licence/provenance note, and
a review that no raw payload or personal path is included.

## Decision gates

- If the private upload does not cover the 8 plots: no fit; use the P13 fallback.
- If it covers fewer than 6 plots: descriptive only.
- If the coefficients are unstable or a holdout fails: evaluation only.
- If the partner does not approve derived-public release: internal research only.

## Implementation

The pre-registered fit is implemented by `pipeline/fit_inventory_cards.py`; see
`notes/reports/p16-fit-pipeline.md` and `notes/reports/p16-fit-runbook.md`.

## References

- `notes/adr/0007-private-lidar-derived-public.md`
- `notes/reports/p14-ingest-runbook.md`
- `notes/reports/p13-pointcloud-acquisition-request.md`
