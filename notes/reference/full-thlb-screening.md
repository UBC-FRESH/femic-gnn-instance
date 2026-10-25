# Full-THLB net revenue screening

Date: 2026-10-25
Status: full-THLB screening; not a calibrated or sustainable result.

## Coverage

The screen covers **52,984.43 ha of derived THLB**, at the VRI checkpoint-polygon
level (19,467 rows before THLB filtering).

## Method

- Terrain: AWS Terrarium tiles at zoom 11 (coarse), sampled at the VRI label
  centre; operability classes ground <35%, cable <50%, heli candidate >=50%.
- Harvest cost: class-average full-system screening costs from the FHOPS
  registry:
  - ground_fb_skid: 15.37 CAD/m3
  - cable_running_sr54: 17.77 CAD/m3
  - helicopter: 78.13 CAD/m3
- Transport: legacy CLEWs/FFCM 100 km truck + 100 km barge + transload,
  10.961 CAD/m3 base; 7.77-14.54 range.
- Prices: local reviewed BC Coast Log Market deck for 2026-01-31; sale type by
  age (old growth >=141 years, second growth otherwise; cypress old-growth
  proxy). Raw prices are not committed.
- Recovery: provisional `recovery_matrix.csv`; reject/waste factor 2% low, 5%
  base, 10% high.
- Net unit revenue = gross log revenue / volume - harvest cost - transport.

## Result

| Case | Positive THLB | Share |
| --- | ---: | ---: |
| Low price/recovery, high transport | 46,612.65 ha | **88.0%** |
| Base | 50,602.51 ha | **95.5%** |
| High price/recovery, low transport | 51,285.26 ha | **96.8%** |

By operability (base):

| Class | THLB | Share of THLB | Positive share | Median net |
| --- | ---: | ---: | ---: | ---: |
| Ground | 29,051.3 ha | 54.8% | 96.6% | 187.6 CAD/m3 |
| Cable | 12,334.6 ha | 23.3% | 97.4% | 164.3 CAD/m3 |
| Heli candidate | 11,598.5 ha | 21.9% | 90.8% | 100.2 CAD/m3 |

Sensitivity:

- harvest cost x1.2: 93.8% positive
- harvest cost x1.5: 92.0%
- harvest cost x2.0: 87.8%
- transport 30 CAD/m3: 92.3%

FHOPS marine transport sensitivity (2026-10-25):

- FHOPS #187 marine Phase I adapter, opt-in with `--transport fhops-marine`.
- Low/base/high barge utilisation: 5.642/6.100/7.097 CAD/m3, including
  contract fixed dispatch costs.
- Positive THLB: 90.2% low case, 95.8% base, 97.0% high case.
- The FHOPS route/terminals are a synthetic Sunshine Coast -> Howe Sound
  fixture, not a GNN terminal inventory or current quote.
- The published result above remains the legacy transport comparison.

## Caveats

- Class-average system costs are applied to every block; this is not a
  per-block FHOPS solve.
- Terrain is a coarse centroid sample, not LiDAR or a block zonal mean.
- Price deck and recovery assumptions dominate. Cypress uses an old-growth
  proxy; the recovery matrix is not observed stand recovery.
- Log prices are applied after a reject/waste factor; merchantability and
  utilization still need review.
- Transport is legacy diagnostic, not a current quote.
- No road/landing construction, overhead, profit, or silviculture cost.
- This is a screening estimate, not a sustainable harvest level.

Detailed polygon output is local under `runtime/p3/full_thlb_screening.csv`.
