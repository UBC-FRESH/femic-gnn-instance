# FEMIC GNN Instance

- Public prototype: https://github.com/UBC-FRESH/femic-gnn-instance
- Documentation: https://ubc-fresh.github.io/femic-gnn-instance/
- Registered in `femic` as `external/femic-gnn-instance`.

A third FEMIC/ws4 model covering the Gwa'sala-'Nakwaxda'xw Nations (GNN)
traditional territory, built from the TSA 46 and TSA 47 portions of the
proposed GNN Statement of Intent boundary.

## Status

Phase 1 (validation and hardening) is active. `ROADMAP.md` is the plan of
record, and the GitHub issues carry the live status. The model is a **prototype**,
not a release.

> **Warning:** The boundary is the **proposed GNN Statement of Intent** polygon,
> not a final treaty boundary or a legal title determination. Confirm the
> boundary and the public-output plan with GNN before operational use. The THLB
> and AAC are derived prototype values, not legal determinations.

## Prototype result

- Combined calibrated THLB: **52,984.42 ha**
- Derived annual AAC: **252,636.75 m3/yr** (not legal)
- Opening-first: 3,158 openings, 5,618 blocks, 39,558.5 ha
- 100% 5-40 ha patches
- 9/10 decades met; decade 10 is 781.4 m3 below the derived band
- GNN-area ground-plot sample: 34 rows / 10 sites, too sparse for an accuracy conclusion
- AUs: 39 TSA-prefixed; TSA 46/47 curves are not interchangeable

See `notes/reference/model-build.md`, `notes/reference/validation.md`, and
`notes/reference/au-harmonization.md`.

## How this project works

This project follows the UBC-FRESH dev workflow. Work is planned as phases,
tasks, and subtasks in `ROADMAP.md`, mirrored in GitHub issues, and recorded in
`CHANGE_LOG.md`. The agent operating contract is in `AGENTS.md`. Read `AGENTS.md`
and `ROADMAP.md` before changing anything.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
pre-commit install
python scripts/dashboard.py
```

## Repository map

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Operating contract for coding agents |
| `ROADMAP.md` | Plan of record and issue tracker map |
| `CHANGE_LOG.md` | Dated narrative of changes |
| `docs/` | Documentation site |
| `notes/` | ADRs, reference notes, plans, and close-out reports |
| `scripts/` | Workflow tooling: validator and green dashboard |
| `pipeline/` | Model build and analysis entry points |
| `config/` | Run profiles, targets, and patch accounts |
| `data/source/` | AOI source polygons and provenance |
| `tests/` | Workflow tooling tests |
| `serve_gnn_calibrated.sh` | Loopback web UI launcher |

## Build

```bash
pipeline/build_gnn_model.sh
./serve_gnn_calibrated.sh
```

The build script expects the base instances at `../femic-tsa46-instance` and
`../femic-tsa47-instance`. Runtime outputs are gitignored.

## AOI

- `data/source/aoi/gnn_soi.gpkg` — proposed GNN SOI polygon, EPSG:3005.
- `data/source/aoi/gnn_full.gpkg` — SOI clipped to the TSA 46/47 union.
- `data/source/aoi/gnn_aoi.json` — area and provenance summary.

| Item | Area |
| --- | ---: |
| GNN SOI total | 703,417.95 ha |
| GNN AOI inside TSA 46/47 | 682,155.05 ha |
| TSA 46 overlap | 292,930.08 ha |
| TSA 47 overlap | 389,226.32 ha |
| Outside both TSAs | 21,262.91 ha |

Source: BCGW `WHSE_LEGAL_AND_ADMIN_BOUNDARIES.QSOI_BC_REGIONS`,
feature `Gwa'Sala-'Nakwaxda'xw Nation (proposed)`.

## Dependencies

- TSA 46 and TSA 47 base models (P1.7) are merged and stable.
- A TSA-prefixed AU decision and a reporting-only crosswalk.
- A derived THLB/AAC benchmark, clearly labelled non-legal.
- GNN review of the proposed boundary and any public output.

Tracking issue: `UBC-FRESH/femic#341`.
