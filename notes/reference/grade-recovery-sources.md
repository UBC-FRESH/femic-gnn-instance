# Grade and sort recovery sources

Date: 2026-10-25
Status: provisional assumption matrix only; not a stand-level observed matrix.

## What the public sources give

- **BC Cruise Compilation Manual**, Amendment No. 2 (effective 2023-07-01),
  sections 15.9.11 and 15.9.12: cedar and spruce high-grade distributions by
  Natural Resource District, sourced from the Coast Grade Distribution Report
  2021-04-01 to 2023-03-31.
- **CGNF Compilation Standards for the Coast Forest Area**, Appendix 5: spruce
  high-grade tables.
- **Coast Concurrent Residual Harvest System (CRHS)** tables: HemBal/Fir
  pulp/CNS grade profiles and species profiles.
- **Coast Appraisal Manual**: log grade percentage definitions and the cruise
  basis for grade percentages.

These sources do not provide a complete, current, stand-level recovery matrix
for all species, ages, sites, and quality classes in the GNN AOI. The CRHS
profiles are for residual/pulp strata; the cruise-grade tables cover selected
high-grade splits. They are not a substitute for a cruise or mill recovery
sample.

## The provisional matrix

`config/cost_revenue/recovery/recovery_matrix.csv` is a **UBC-FRESH assumption
set**. It maps species groups to high-grade, sawlog, utility, and pulp shares
with low/base/high cases. Every row is marked `data_status=assumption`.

It exists to make the arithmetic testable. It is not evidence of GNN recovery.

## What must replace it

- A GNN-area cruise grade distribution by species and age class.
- Mill or sort-yard recovery data, if a partner can provide it.
- A documented local sort specification (sawlog/peeler/utility/pulp) and
  destination.

Until one of those exists, a scenario using this matrix is a **costed
prototype**, not a sustainable harvest level. The P3.5 gate must reject
`data_status=assumption` for a sustainable label.

## Why not use the market sales mix

The BC market report publishes the grade/species mix of logs sold into the
Vancouver Log Market. That is a market composition, not the recovery from a
particular block. Using it as block recovery would systematically confuse what
was sold with what a stand can produce.
