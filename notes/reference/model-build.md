# GNN prototype build

Date: 2026-10-25
Status: prototype matrix and derived benchmark; not a release.

## Method

The GNN prototype reuses the stabilized TSA 46 and TSA 47 base models rather
than rerunning VRI/VDYP:

1. Clip the calibrated TSA 46 and TSA 47 checkpoints to the GNN AOI.
2. Combine the clipped checkpoints; keep TSA-prefixed AU ids.
3. Combine the TSA 46/47 FEMIC bundles.
4. Export one Patchworks XML/fragments model with the FEMIC exporter.
5. Merge safe slivers, build and validate the ws4 matrix.
6. Build the touching-block topology and opening-first schedule.
7. Simulate and report against the derived benchmark.

## Model

- Combined checkpoint rows: 19,467
- Clipped stand area: 250,461.39 ha
- Derived calibrated THLB: **52,984.42 ha**
- Fragments after export: 19,466
- AUs: 39 (TSA-prefixed, no harmonization)
- ws4 validation: pass

## Benchmark

The derived annual AAC is **252,636.75 m3/yr**, the THLB-weighted share of the
TSA 46 and TSA 47 published AACs:

`803,000 * 18,411.68/268,970 + 830,500 * 34,572.74/145,256`

This is **not a legal AAC**. It is a prototype benchmark only.

Opening-first schedule:

- Openings: 3,158
- Scheduled blocks: 5,618
- Scheduled area: 39,558.5 ha
- Opening range: 5.0-39.8 ha
- Patch classes: 100% 5-40 ha
- Decade result: 9/10 met; decade 10 is 2,525,218.6 m3, **781.4 m3 below**
  the derived band.

The decade-10 miss is recorded, not hidden.

## Caveats

- Proposed GNN Statement of Intent boundary, not a final treaty boundary.
- TSA-prefixed AUs preserved; no harmonization.
- Derived THLB/AAC, not a reviewed GNN netdown or legal determination.
- No UI, docs site, or public release yet.
- Needs GNN review before public model outputs.

## Reproduce

```bash
scripts/build_gnn_model.sh
```

The script expects the base instances at `../femic-tsa46-instance` and
`../femic-tsa47-instance`.
