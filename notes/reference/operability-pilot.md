# Operability pilot: 40 real blocks

Date: 2026-10-25
Status: pilot only; not a representative GNN sample and not a net revenue result.

## Method

- Candidate blocks: 10-40 ha, VRI live volume 250-750 m3/ha.
- Random sample: 40 blocks, seed 42.
- Stand attributes: VRI checkpoint clipped to each block.
- Terrain: AWS Terrarium tiles at zoom 12 (coarse), mean and p90 slope inside the
  block polygon.
- Classes:
  - `ground`: mean slope <35% and p90 <45%.
  - `cable`: mean <50% and p90 <65%.
  - `heli_candidate`: anything steeper.
- Costs: FHOPS cable TR125 single-span 300 m / 25 m lateral / 1.6 m3 payload;
  helicopter longline at 1000 m one-way; one machine/one model, no move-in,
  landing, road, truck haul, barge, overhead, or profit.

## Result

| Operability | Volume share |
| --- | ---: |
| Ground | 36.9% |
| Cable | 34.8% |
| Heli candidate | 28.3% |

**63.1% of sampled volume is non-ground** under these coarse thresholds. A
single ground-based cost average is not defensible.

Screening cost ranges, before access/haul/barge:

- Cable Skylead C40: 17.61 CAD/m3.
- Cable Cypress 7280: 37.50 CAD/m3.
- Helicopter Bell 214B: 59.66 CAD/m3.
- Helicopter KMAX: 87.09 CAD/m3.

The per-block totals are in `operability_pilot_40.csv`. They are screening
totals, not delivered cost.

## Species composition

The sampled blocks are dominated by cedar and cypress, with a smaller Hembal
share. This is a property of this random sample, not the GNN AOI. Fir and spruce
shares were low in this sample, so the pilot does not yet cover the full species
range.

## Caveats

- 40 blocks is a pilot, not a GNN-wide sample.
- Zoom 12 is a coarse DEM; p90 slope may be smoothed or noisy.
- Class thresholds are operational assumptions, not a geotechnical survey.
- The cost is one productivity model plus one machine rate. It excludes
  move-in, landing, road, truck haul, barge, overhead, and profit.
- Price deck and recovery matrix are still provisional. No net revenue is
  claimed.

## Next

1. Expand across the AOI and target the underrepresented species/terrain strata.
2. Replace coarse DEM with a finer DEM or LiDAR where available.
3. Add landing/road/transfer/barge cost.
4. Run full FHOPS systems, not single machines.
5. Add validated price and recovery, then net revenue and the gate.

File: `config/cost_revenue/samples/operability_pilot_40.csv`
## Species-stratified sensitivity

A second pilot sampled up to 8 blocks per leading-species group (cedar, cypress,
hembal, fir, spruce, other; seed 42). Fir and spruce were not represented in the
candidate set at this sampling depth, so this is not a balanced species sample.
The available groups produced:

| Operability | Volume share |
| --- | ---: |
| Ground | 18.7% |
| Cable | 36.2% |
| Heli candidate | 45.1% |

**81.3% of this stratified sample is non-ground.** The gap from the random
40-block pilot (63.1%) shows how sensitive the result is to sample composition.
The defensible conclusion is not a single percentage; it is that non-ground
volume is large enough that a ground-only cost assumption is unacceptable.

File: `config/cost_revenue/samples/operability_pilot_stratified.csv`
