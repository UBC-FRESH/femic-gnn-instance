# GNN ground-plot validation

Date: 2026-10-25

## Method

The TSA 46/47 non-PSP ground-plot validation rows were filtered to FAIB sites
inside the proposed GNN SOI AOI. The inherited TSR curves and AU assignments
are unchanged.

## Sample

- Matched rows: **34**
- Sites: **10**
- Source TSA: **TSA 47 only** (no TSA 46 managed plots fall inside the AOI)
- Sample types: VRI 31, CMI 1, NFI 2

This is not enough for a GNN-specific accuracy conclusion. It is a check on the
available public ground plots, not a validation of the prototype.

## Directional signal

| Sample | n | Volume bias | DBH bias | Height bias | Stems bias |
| --- | ---: | ---: | ---: | ---: | ---: |
| VRI | 31 | -118.1 m3/ha | -5.1 cm | +0.1 m | -341.9 sph |
| NFI | 2 | -104.4 m3/ha | +1.2 cm | -2.3 m | -434.1 sph |
| CMI | 1 | -149.4 m3/ha | -7.5 cm | -6.0 m | +160.8 sph |

VRI volume relative bias is about **-26%**; stems are also underpredicted.
Height is essentially unbiased in the VRI sample.

The direction is consistent with the larger TSA 47 validation, but the GNN
sample is too sparse to separate AU, age, and sample-type effects.

## Caveats

- VRI plots are inventory audits, not remeasured PSP/CMI plots.
- No TSA 46 managed plots fall inside the AOI.
- The model has not been re-fit or tuned to this sample.
- No production curve or AAC target was changed.

## Next

- Acquire more ground plots inside the GNN AOI, especially managed/young plots.
- Keep the inherited TSA 46/47 validation as the primary accuracy evidence.
- GNN review of the proposed boundary and public outputs.

## P1.2 public-plot inventory and PSP check

The public-plot inventory inside the AOI contains 51 sites:

| Source | Sample type | Sites |
| --- | --- | ---: |
| PSP | PSP_G | 7 |
| PSP | PSP_R | 17 |
| non-PSP GBR North | CMI | 3 |
| non-PSP GBR North | YSM | 1 |
| non-PSP GBR South | CMI | 3 |
| non-PSP GBR South | NFI | 1 |
| non-PSP GBR South | VRI | 19 |

The full PSP manifest was filtered to the AOI and validated against the TSA 46
TSR curves. It produced **55 observations from 12 sites**:

| Sample | n | Sites | Volume bias | DBH bias | Height bias | Stems bias |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PSP_R (experimental) | 52 | 10 | -216.5 m3/ha | -11.5 cm | -4.5 m | +104.3 sph |
| PSP_G (natural) | 3 | 2 | -101.0 m3/ha | -11.3 cm | -2.1 m | -498.5 sph |

The PSP rows span ages 34-176 years (median 101), so they are not a
managed-young TIPSY benchmark. PSP_R is experimental and PSP_G is natural
growth. The volume and DBH underprediction is consistent with the TSA 46 SI
issue, but this sample does not isolate managed-curve accuracy.

The existing non-PSP matched sample remains **34 rows / 10 sites** (TSA 47
only). The combined evidence is still too sparse and too unmanaged to support a
GNN-specific managed-curve accuracy conclusion.

Files:

- `config/tsr/gnn_ground_plot_inventory.csv`
- `config/tsr/gnn_psp_validation_tsa46.csv`
- `config/tsr/gnn_psp_validation_tsa46_summary.csv`

No curve or AAC target was changed.
