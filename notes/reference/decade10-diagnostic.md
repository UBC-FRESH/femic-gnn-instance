# Decade-10 schedule diagnostic

Date: 2026-10-25
Status: diagnosed; no curve, target, THLB, or AAC change.

## Existing benchmark

The opening-first schedule uses a 100-year horizon and a derived decade target of
2,527,000 m3. It meets nine decades. Decade 10 is 2,525,218.6 m3, which is
**781.4 m3 below** the derived band floor of 2,526,000.

## Diagnostic

The scheduler is deterministic; it has no random seed. To test whether the miss
is caused by the target being set too high, the same model was run with the
band floor, 2,526,000 m3:

| Target | Decade 10 | Result |
| --- | ---: | --- |
| 2,527,000 (benchmark) | 2,525,218.6 | 781.4 below band |
| 2,526,000 (diagnostic) | 2,524,255.0 | 1,745.0 below band |

Lowering the target did not fix decade 10. It lowered every decade and left the
last period below the band.

The last period is not short of scheduled blocks:

| Decade | Scheduled blocks |
| --- | ---: |
| 8 | 770 |
| 9 | 819 |
| 10 | 866 |

The 100-year horizon drops 522 openings because they become ready after year
90. The remaining eligible blocks in the last period carry less volume per block
than earlier periods, so the period has many blocks but not enough volume.

## Conclusion

The decade-10 miss is a **horizon and age-structure end-effect**. It is not
evidence that the curves are wrong, and it is not fixed by raising or lowering
the derived target. No curve, target, THLB, AAC, or benchmark change is made.

## Caveats

- The scheduler's builder proxy differs slightly from the ws4 report; the
  diagnostic compares report values, not the builder printout.
- The low-target run is evidence only; it is not a replacement benchmark.
- A longer horizon or a different terminal policy would change the end-effect,
  but that is a policy decision, not a curve fit.

## Files

- `runtime/gnn/runs/opening_first/report_targets.csv` (benchmark)
- `runtime/gnn/runs/opening_lowtarget/report_targets.csv` (diagnostic)
- `runtime/gnn/schedules/opening_lowtarget.csv` (diagnostic schedule)

Runtime files are gitignored.
