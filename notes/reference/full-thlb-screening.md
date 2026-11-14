# Full-THLB net revenue screening

Date: 2026-10-25
Status: full-THLB screening; not a calibrated or sustainable result.

## Coastal old-growth threshold correction

The earlier screen used **141 years**, the lower bound of BC Age Class 8, to
select old-growth prices and costs. That is not the coastal old-growth
definition. This screen now uses **250 years** for coastal old growth; 141–249
year stands are second growth. The corrected base screen is **95.4% positive**
(493 negative blocks, 4.7% of THLB). Candidate schedules, headroom, access, and
risk reports built on the earlier 141-year screen remain to be rerun.

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
  age (old growth >=250 years, second growth otherwise; cypress old-growth
  proxy). Raw prices are not committed.
- Recovery: provisional `recovery_matrix.csv`; reject/waste factor 2% low, 5%
  base, 10% high.
- Net unit revenue = gross log revenue / volume - harvest cost - transport.

## Result

| Case | Positive THLB | Share |
| --- | ---: | ---: |
| Low price/recovery, high transport | 46,603.35 ha | **88.0%** |
| Base | 50,535.06 ha | **95.4%** |
| High price/recovery, low transport | 51,205.16 ha | **96.6%** |

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

FHOPS marine API test (not a GNN transport sensitivity):

- The adapter and fixture are available, but the fixture is Sunshine
  Coast -> Howe Sound while the GNN AOI is northern Vancouver Island.
- The fixture is a code-path test, not a GNN terminal, distance, or rate deck.
- No FHOPS marine cost is used in the published result above.
- See `notes/reference/gnn-marine-geography.md`.

## Caveats

- Class-average system costs are applied to every block; this is not a
  per-block FHOPS solve.
- Terrain is a coarse centroid sample, not LiDAR or a block zonal mean.
- Price deck and recovery assumptions dominate. Cypress uses an old-growth
  proxy; the recovery matrix is not observed stand recovery.
- Log prices are applied after a reject/waste factor; merchantability and
  utilization still need review.
- Transport is legacy diagnostic, not a current quote.
- FHOPS marine is an API test only; the fixture is not the GNN geography.
- No road/landing construction, overhead, profit, or silviculture cost.
- This is a screening estimate, not a sustainable harvest level.

Detailed polygon output is local under `runtime/p3/full_thlb_screening.csv`.

## External partner cost contract

The screen supports an optional partner cost contract:

```bash
python pipeline/full_thlb_screening.py \
  --checkpoint data/gnn_combined_checkpoint.feather \
  --aoi data/source/aoi/gnn_full.gpkg \
  --prices runtime/p3/price_deck_reviewed.csv \
  --recovery config/cost_revenue/recovery/recovery_matrix.csv \
  --cost-config runtime/gnn/partner_costs.yaml \
  --transport included \
  --out runtime/gnn/full_thlb_screening_partner.csv
```

The contract can supply harvest totals by ground/cable/heli land/heli water and
old/second growth, plus road construction rates. `--transport included` must be
used when the partner totals already include barging. The class-average values
above remain the published comparison; partner rates are not committed.

The current contract records the coastal 250-year old-growth threshold and uses the
land-drop helicopter total unless the contract says otherwise. The earlier 141-year
Age Class 8 boundary was a correction target; 141-249-year stands are classified
as second growth in this coastal screen. Road construction
rates are loaded but not allocated until route lengths, landings, crossings, and
existing-versus-new-road treatment are available.
