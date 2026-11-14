# Diagnostic block-exclusion scenario

Status: diagnostic sensitivity. This is not the base schedule, a sustainable
plan, or a financial result.

## What was tested

The opening-first schedule was filtered to remove every block with negative
direct net revenue in the block-level screen.

- Blocks removed: **276**
- Scheduled rows removed: **276**
- THLB removed: **1.44 thousand ha**
- Volume removed: **0.838 million m3**
- Direct net revenue removed: **-18.4 million CAD**
- `forced_access` exceptions: none

Shared road, landing, terminal, and overhead costs remain **unallocated**.

## Result

All ten decades fall below the derived target band:

| Decade | Base volume (m3) | Block-gate volume (m3) | Shortfall (m3) | Shortfall |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 2,526,514 | 2,503,783 | 22,731 | 0.9% |
| 2 | 2,526,661 | 2,474,836 | 51,825 | 2.1% |
| 3 | 2,526,840 | 2,385,618 | 141,221 | 5.6% |
| 4 | 2,526,854 | 2,425,676 | 101,178 | 4.0% |
| 5 | 2,526,957 | 2,403,539 | 123,419 | 4.9% |
| 6 | 2,526,893 | 2,469,761 | 57,132 | 2.3% |
| 7 | 2,526,314 | 2,346,196 | 180,118 | 7.1% |
| 8 | 2,526,476 | 2,387,869 | 138,608 | 5.5% |
| 9 | 2,526,927 | 2,366,929 | 159,998 | 6.3% |
| 10 | 2,525,219 | 2,325,449 | 199,769 | 7.9% |

Total ten-decade shortfall: **1.176 million m3** (4.7% of the base total).

The patch-size constraints remain met. The base schedule, curves, THLB, AAC,
targets, and benchmark are unchanged.

## Interpretation

The direct-cost block gate conflicts with the current volume schedule at this
screening level. Removing known loss-making blocks is not free: it removes
volume that the current opening-first schedule relies on.

This result does **not** say the block gate is wrong. It says:

- the current schedule is not economically screened;
- a full solution would need a different block/opening selection, more area, or
  explicit forced-access treatment;
- neither response should be chosen by tuning curves, AAC, or targets.

## Caveats

- Direct costs only; shared road/landing/terminal/overhead costs are not
  allocated.
- The block-level screen uses class-average harvest costs, provisional recovery,
  legacy transport, and a dated public price deck.
- The block screen covers 7,848 screened blocks (99.4% of screened THLB); 0.3
  thousand ha is unallocated.
- This is not a sustainable or profitable result.

## Reproduce

```bash
python pipeline/screen_block_exclusion.py
python -m ws4.cli simulate \
  --dataset runtime/gnn/matrix \
  --schedule runtime/gnn/schedules/opening_first_block_gate.csv \
  --out runtime/gnn/runs/opening_first_block_gate \
  --years 100 --topology runtime/gnn/topology.csv \
  --patch-accounts config/patch_accounts.gnn.yaml --patch-membership
python -m ws4.cli report \
  --run runtime/gnn/runs/opening_first_block_gate \
  --targets config/targets.gnn_opening.yaml \
  --out runtime/gnn/runs/opening_first_block_gate
```
