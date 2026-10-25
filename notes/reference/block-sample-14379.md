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
