# Positive net revenue share of sampled THLB

Date: 2026-10-25
Status: screening only; not a full-THLB answer.

## Question

What fraction of THLB has positive net unit revenue now?

## Answer

It cannot be answered for the full THLB from the current model.

The current net screening covers only **242.5 ha of priced cable/heli THLB**,
which is **0.46% of the 52,984.42 ha derived GNN THLB**. Ground blocks are
unpriced. In total, the sample covers 328.5 ha, or 0.62% of THLB.

Of the priced cable/heli THLB:

| Case | Positive THLB | Share of priced THLB | Positive volume share |
| --- | ---: | ---: | ---: |
| Best case (`net_high > 0`) | 214.7 ha | **88.5%** | 93.4% |
| Worst case (`net_low > 0`) | 154.0 ha | **63.5%** | 55.8% |

Ground THLB in the sample: 86.0 ha, unpriced.

## Method

- Combined the random 40-block and species-stratified net screening outputs,
  deduplicated by block.
- Joined each block to the VRI checkpoint and computed calibrated THLB as
  clipped area x `thlb_raw_calibrated / 100`.
- Classified a block positive if net revenue was > 0 in the best or worst price/
  cost case.
- Priced blocks are cable/heli only; ground blocks have no full-system cost in
  the net screen.

## Caveats

- 0.46% THLB coverage is not representative; do not extrapolate.
- The net screen uses one-machine cable/heli costs, not the full-system costs.
  The three full-system checks were higher, so these shares are optimistic.
- Price and recovery assumptions dominate the range.
- Legacy transport values; not current quotes.
- No road/landing/overhead/profit.
- No sustainable label.

Detailed net tables are local under `runtime/p3/`.
