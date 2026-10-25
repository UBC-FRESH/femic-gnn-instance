# One-block operability sample: block 14379

Date: 2026-10-25
Status: one-block coarse sample; not a full operability survey.

## Why this block

Selected from blocks 10-40 ha with a VRI live volume between 250 and 750 m3/ha,
to get a productive stand that is not an old low-volume outlier. It is a test of
the data path, not a representative GNN block.

## Stand attributes

| Attribute | Value |
| --- | ---: |
| Area | 17.005 ha |
| Live volume | 12,746.6 m3 |
| Volume per ha | 749.6 m3/ha |
| Live stems | 13,297.8 |
| Stems per ha | 782.0 |
| Average stem size | 0.959 m3 |

Source: VRI checkpoint clipped to the block.

## Terrain

Sampled from AWS Open Data Terrarium terrain tiles at zoom 13, then averaged
inside the block polygon:

| Attribute | Value |
| --- | ---: |
| Mean slope | 58.75% |
| P90 slope | 79.05% |
| Mean elevation | 548.9 m |
| Data status | coarse DEM sample |

This is a coarse 20-30 m DEM sample, not a LiDAR or field survey. It is enough
to show that the block is steep, not enough for a final cable/heli layout.

## Operability finding

FHOPS's ground-based Lahrsen productivity model rejects this block because
`ground_slope=58.75` is outside the observed range `[1.5, 48.9]`. The block
cannot be honestly costed with a ground-based machine rate. It needs a
cable/heli system and a system-specific cost model.

This is the first real evidence that the GNN area will not be well represented
by a single ground-based cost average.

## Next

1. Run FHOPS cable/heli productivity models or a documented cable/heli cost
   model for this block.
2. Repeat for a stratified sample of ground/cable/heli blocks.
3. Add roads, landings, and barge/transfer points.
4. Only then aggregate to a scenario net revenue.

No GNN net revenue is claimed from this sample.

## Cable/heli screening costs

Using the block's actual stand and terrain, with documented assumptions for
distance/payload, the FHOPS cable/heli productivity models and machine rates give:

| System | Model | Productivity | Cost |
| --- | --- | ---: | ---: |
| Helicopter longline | KMAX, 1000 m | 29.82 m3/PMH | 87.09 CAD/m3 |
| Helicopter longline | Bell 214B, 1000 m | 47.91 m3/PMH | 59.66 CAD/m3 |
| Cable yarder | Skylead C40, TR125 300 m | 19.03 m3/PMH | 17.61 CAD/m3 |
| Cable yarder | Cypress 7280, TR125 300 m | 19.03 m3/PMH | 37.50 CAD/m3 |

These are **screening costs**: one productivity model plus one machine rate.
They exclude move-in, landing construction, truck haul, barge, overhead, and
profit. They are not a delivered cost and not a net revenue result.

Using the legacy CLEWs/FFCM diagnostic transport values at 100 km truck + 100 km
barge + transload adds about 10.961 CAD/m3. That makes cable ~28.57 CAD/m3 and
helicopter KMAX ~98.05 CAD/m3 before move-in, landing, overhead, and profit.
Those are still diagnostic, not quotes.

The range is large enough to change the conclusion: at 12,746.6 m3, the
helicopter KMAX harvest cost alone is about 1.11 million CAD; cable is roughly
0.22-0.48 million CAD. A ground-based average would have hidden this.

Files:

- `config/cost_revenue/samples/block_14379_cost_screening.csv`
- `config/cost_revenue/samples/block_14379.csv`
