# Net revenue screening ranges

Date: 2026-10-25
Status: screening only; not a net revenue result.

## Method

- Samples: random 40-block operability pilot and species-stratified pilot.
- Price deck: local reviewed BC Coast Log Market deck for 2026-01-31; not
  redistributed.
- Recovery: provisional `config/cost_revenue/recovery/recovery_matrix.csv`
  (all rows `data_status=assumption`).
- Harvest: one cable or helicopter productivity model plus one machine rate;
  ground blocks are excluded because a full ground system is not yet costed.
- Transport: legacy CLEWs/FFCM diagnostic 100 km truck + 100 km barge + 4.57
  CAD/m3 transload, with 7.77-14.54 CAD/m3 range. An opt-in FHOPS marine path
  is available with `--transport fhops-marine`; its synthetic fixture is not a
  current quote.
- Revenue range uses low/high recovery shares and low/high prices; net range is
  best/worst case, not a confidence interval.

## Aggregate result

Random 40-block pilot:

- 25 priced cable/heli blocks, 229,015 m3
- net range **+5.21M to +50.30M CAD**
- 0% unprofitable even in the optimistic case

Species-stratified pilot:

- 25 priced cable/heli blocks, 232,482 m3
- net range **-1.70M to +36.32M CAD**
- **13.1% of priced volume unprofitable even in the best case**

Ground blocks remain unpriced, so these totals are not scenario net revenue.

## Interpretation

The result is not "the scenario is profitable." The spread between low and high
is larger than the result itself, and it is driven by provisional prices,
recovery shares, one-machine harvest rates, and legacy transport. The only
defensible conclusion is that price/recovery/operability uncertainty dominates,
and some cable/heli volume may be uneconomic.

## Next

1. Replace the price deck and recovery assumptions with accepted data.
2. Cost full ground systems.
3. Use actual road/water distances and current carrier/terminal quotes.
4. Re-run as a scenario net revenue with the sustainable gate.
5. Keep the release volume-only until then.

Detailed per-block tables are local under `runtime/p3/`.
