# Forest condition report: gnn-cwh-inventory-pilot-2026

- **Scenario:** p11-cwh-inventory-diagnostic
- **Period:** 2026
- **Generated:** 2026-11-02T00:00:00Z
- **Review status:** draft
- **Status:** report-only; alerts are advisory, not operational decisions.

## Indicators

| Indicator | Value | Unit | Source | Status | Applicability |
| --- | ---: | --- | --- | --- | --- |
| cwh_basal_area_diagnostic | 42.29 | m2/ha | femic.inventory.als (cwh-basal-area-psp-lidarbc-2026) | review_required | CWH northern Vancouver Island; 14-plot pilot; GNN diagnostic only |
| lidar_pilot_fragments | 181 | fragments | femic.lidar (2026.10.0-gnn-10m) | ok | bounded southern GNN LiDAR pilot |

## Alerts

| Code | Severity | Indicator | Advisory message |
| --- | --- | --- | --- |
| inventory-not-operational | watch | cwh_basal_area_diagnostic | CWH cards are a 14-plot regional pilot; the VRI comparison is weak; do not use for operability or AAC. |
| lidar-coverage | watch | lidar_pilot_fragments | LiDAR pilot covers 181 fragments / 184 blocks / 979 ha; not a GNN-wide layer. |

## Provenance

- **instance:** femic-gnn-instance@ee0e7a3
- **report:** notes/reports/p11-cwh-inventory-diagnostic.md
- **bundle:** lidarbc-1b7b79757e98cfe5
- **bundle_version:** 2026.10.0-gnn-10m
- **model_card:** config/inventory/models/als_cwh_basal_area_2026.json

## Limits

- This card is report-only and does not change objectives, constraints, growth, or the solver.
- Alerts are advisory and must not be treated as operational decisions.
- Indicator applicability and review status must be checked before use.
