# Operability pilot: 12 real blocks

Date: 2026-10-25
Status: pilot only; not a representative sample and not a net revenue result.

## Method

- Candidate blocks: 10-40 ha, VRI live volume 250-750 m3/ha.
- Random sample: 12 blocks, seed 42.
- Stand attributes: VRI checkpoint clipped to each block.
- Terrain: AWS Terrarium tiles at zoom 12 (coarse), mean and p90 slope inside the
  block polygon.
- Classes:
  - `ground`: mean slope <35% and p90 <45%.
  - `cable`: mean <50% and p90 <65%.
  - `heli_candidate`: anything steeper.
- Costs: FHOPS cable TR125 single-span 300 m / 25 m lateral / 1.6 m3 payload;
  helicopter longline at 1000 m one-way; one machine/one model, no move-in,
  landing, haul, barge, overhead, or profit.

## Result

| Operability | Volume share |
| --- | ---: |
| Ground | 58.4% |
| Cable | 28.3% |
| Heli candidate | 13.2% |

**41.6% of sampled volume is non-ground** under these coarse thresholds. A
single ground-based cost average is not defensible.

Screening cost ranges, before access/haul/barge:

- Cable Skylead C40: 17.61 CAD/m3.
- Cable Cypress 7280: 37.50 CAD/m3.
- Helicopter Bell 214B: 59.66 CAD/m3.
- Helicopter KMAX: 87.09 CAD/m3.

The per-block totals are in the sample CSV. They are screening totals, not
delivered cost.

## Caveats

- 12 blocks is a pilot, not a GNN-wide sample.
- Zoom 12 is a coarse DEM; p90 slope may be smoothed or noisy.
- Class thresholds are operational assumptions, not a geotechnical survey.
- The cost is one productivity model plus one machine rate. It excludes
  move-in, landing, road, truck haul, barge, overhead, and profit.
- Price deck and recovery matrix are still provisional. No net revenue is
  claimed.

## Next

1. Expand the sample across the AOI and by terrain/volume strata.
2. Replace coarse DEM with a finer DEM or LiDAR where available.
3. Add landing/road/transfer/barge cost.
4. Run full FHOPS systems, not single machines.
5. Add validated price and recovery, then net revenue and the gate.

File: `config/cost_revenue/samples/operability_pilot.csv`
