# Positive-block candidate schedule

Status: diagnostic candidate schedule. Not the base schedule and not a
sustainable result.

## Question

Can the opening-first schedule meet the same volume band while using only
blocks with non-negative direct revenue?

## Candidate pool

- Positive blocks: **7,370**
- Negative blocks: **478**
- Positive THLB: **50.3 thousand ha**
- Negative THLB: **2.4 thousand ha**

The positive pool was built from the block-level revenue screen. Shared road,
landing, terminal, and overhead costs remain unallocated.

## Rebuilt schedule

The opening-first builder was rerun with the positive pool and the same targets,
topology, patch rules, and 100-year horizon.

- Scheduled blocks: **5,581**
- Scheduled area: **39.4 thousand ha**
- Negative blocks scheduled: **0**
- Openings dropped beyond period capacity: **312**

## Result

All ten decades meet the target band:

| Decade | Realized volume (m3) | Target band | Status |
| ---: | ---: | --- | --- |
| 1 | 2,526,875 | 2,526,000-2,527,000 | met |
| 2 | 2,526,988 | 2,526,000-2,527,000 | met |
| 3 | 2,526,769 | 2,526,000-2,527,000 | met |
| 4 | 2,526,706 | 2,526,000-2,527,000 | met |
| 5 | 2,526,456 | 2,526,000-2,527,000 | met |
| 6 | 2,526,890 | 2,526,000-2,527,000 | met |
| 7 | 2,526,908 | 2,526,000-2,527,000 | met |
| 8 | 2,526,667 | 2,526,000-2,527,000 | met |
| 9 | 2,526,951 | 2,526,000-2,527,000 | met |
| 10 | 2,526,975 | 2,526,000-2,527,000 | met |

The patch-size constraints remain met. The block count is 37 lower than the base
opening-first schedule, and the scheduled area is about 0.18 thousand ha lower.

## Interpretation

At the direct-cost screening level, replacing the negative blocks with other
positive blocks is feasible without changing curves, THLB, AAC, or targets.

This does **not** close the sustainable gate:

- shared road/landing/terminal/overhead costs are unallocated;
- harvest costs are class averages;
- recovery is provisional;
- transport is legacy and not a current quote;
- the price deck is dated and not a forward price.

It is a **positive-block direct-cost candidate**, not a sustainable plan.

## Reproduce

```bash
python pipeline/select_positive_blocks.py
python pipeline/build_opening_schedule.py \
  --dataset runtime/gnn/matrix \
  --topology runtime/gnn/topology.csv \
  --out runtime/gnn/schedules/opening_first_positive.csv \
  --years 100 --min-area 5 --max-area 50 \
  --target-per-decade 2527000 --intermediate-share 0 \
  --allowed-blocks runtime/gnn/schedules/positive_blocks.csv
python -m ws4.cli simulate \
  --dataset runtime/gnn/matrix \
  --schedule runtime/gnn/schedules/opening_first_positive.csv \
  --out runtime/gnn/runs/opening_first_positive \
  --years 100 --topology runtime/gnn/topology.csv \
  --patch-accounts config/patch_accounts.gnn.yaml --patch-membership
python -m ws4.cli report \
  --run runtime/gnn/runs/opening_first_positive \
  --targets config/targets.gnn_opening.yaml \
  --out runtime/gnn/runs/opening_first_positive
```
