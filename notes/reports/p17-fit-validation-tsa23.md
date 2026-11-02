# P17.1 Fit pipeline validation against the published TSA 23 card

Date: 2026-11-02
Status: validation complete; the pipeline reproduces the published TSA 23 cards.

## Source

The public 14-plot TSA 23 INV-01 training table from
`femic-tsa23-instance/notes/reports/inv01-tsa23-training-plots.csv` is copied to
`tests/fixtures/inv01_tsa23_training.csv`. It contains the plot responses and the
CHM-proxy predictors used by the published TSA 23 IDF cards.

## Method

`pipeline/fit_inventory_cards.py` was run with `--plot-features` and `--write-cards`
on the 14 plots. The fitted coefficients, Duan smearing scale, and LOOCV RMSE were
compared with the published cards.

## Result

| Attribute | Parameter | Pipeline | Published |
| --- | --- | ---: | ---: |
| Lorey height | intercept | 1.9441063309517714 | 1.9441063309517714 |
| Lorey height | `Lhp95` | 0.8351084469592212 | 0.8351084469592212 |
| Lorey height | output scale | 1.0 | 1.0 |
| Lorey height | LOOCV RMSE | 0.68848957 | 0.688 |
| Basal area | intercept | -4.724750214946937 | -4.724750214946937 |
| Basal area | `Lhmean` | 0.8686310009684395 | 0.8686310009684395 |
| Basal area | `CC2m` | 1.3794686095244624 | 1.3794686095244624 |
| Basal area | output scale | 1.008780042159369 | 1.008780042159369 |
| Basal area | LOOCV RMSE | 4.41421558 | 4.414 |
| Gross volume | intercept | -4.009416713953133 | -4.009416713953133 |
| Gross volume | `Lhmean` | 1.7395991112544076 | 1.7395991112544076 |
| Gross volume | `CC2m` | 1.1516782963514058 | 1.1516782963514058 |
| Gross volume | output scale | 1.004526898452813 | 1.004526898452813 |
| Gross volume | LOOCV RMSE | 20.66578728 | 20.666 |

The coefficients and scale match to machine precision. The RMSE difference is only
the published cards' three-decimal rounding.

## What it proves

- The fit forms, smearing correction, and LOOCV implementation match the published
  INV-01 TSA 23 cards.
- The private LiDAR pipeline is not only synthetically correct; it reproduces a
  real published fit from public data.

## Limits

- This is the TSA 23 IDF 14-plot pilot, not a GNN calibration.
- The predictors are CHM proxies for the TSA 23 cards; the GNN pipeline will use
  first-return metrics.
- It is not an independent validation of the TSA 23 card.
- No private data was used.

## Test

```bash
python -m pytest tests/test_fit_inventory_cards_tsa23.py -q
```

The test runs the pipeline and asserts the three card coefficient sets, scales, and
LOOCV RMSE.
