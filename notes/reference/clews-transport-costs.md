# CLEWs-C2070 legacy transport costs

Date: 2026-10-25
Status: legacy diagnostic evidence; not a calibrated 2026 tariff.

## Source

`UBC-FRESH/clews-c2070-fresh` at `71b3d45`:

- `metadata/ffcm-archive/parsed/transporters.csv`
- `metadata/ffcm-archive/parsed/transporter_materials.csv`
- `metadata/ffcm-archive/parsed/transload_costs.csv`
- `metadata/ffcm-archive/data-source-disposition.csv`
- `metadata/ffcm-archive/residue-cost-validation-policy-gates.csv`

The source repo labels transporter costs **“Use for schema and rough prototype
only”** and says the **“Cost year and assumptions unclear.”** This note uses
them as a diagnostic bound, not a production quote.

## Log barge

| Field | Value |
| --- | ---: |
| Mode | WATER |
| Speed | 25 km/h |
| Operating cost | 120 CAD/h |
| Fuel cost | 18.345336 CAD/km |
| Capacity | 3,000 m3 |
| Transload | 4.57 CAD/m3 |

Derived:

- operating per km: `120 / 25 = 4.80 CAD/km`
- total per km: `4.80 + 18.345336 = 23.145336 CAD/km`
- per m3-km: `23.145336 / 3000 = 0.007715 CAD/m3/km`
- at 100 km: `0.7715 CAD/m3`
- plus transload: `5.3415 CAD/m3`

## Logging truck

| Field | Value |
| --- | ---: |
| Mode | ROAD |
| Speed | 90 km/h |
| Operating cost | 120 CAD/h |
| Fuel cost | 1.25730374 CAD/km |
| Capacity | 46.1 m3 |

Derived:

- operating per km: `120 / 90 = 1.333333 CAD/km`
- total per km: `1.333333 + 1.257304 = 2.590637 CAD/km`
- per m3-km: `2.590637 / 46.1 = 0.056195 CAD/m3/km`
- at 100 km: `5.6195 CAD/m3`
- plus transload: `10.1895 CAD/m3`

## Combined 100 km truck + barge + transload

`5.6195 + 0.7715 + 4.57 = 10.961 CAD/m3`

This is substantially lower than the earlier 31 CAD/m3 placeholder. It is also
uncalibrated and assumes a 100 km road haul plus a 100 km barge leg, a 3,000 m3
barge, and no road construction, handling delays, storage, or profit.

## Use rule

- Treat these as a **legacy diagnostic sensitivity**, not a current tariff.
- Do not use them to claim a scenario is profitable without a current
  carrier/terminal quote.
- The sustainable gate must reject `legacy_diagnostic` unless the maintainer
  explicitly accepts the bound.
- Replace with actual road/water distances and terminal/carrier rates.
