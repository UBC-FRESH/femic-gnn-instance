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
