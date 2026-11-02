# ADR 0007: Private raw LiDAR, public derived datasets

Date: 2026-11-02
Status: accepted.

## Context

A partner is preparing a private LAZ upload for the GNN area. The raw point files are
private and must not be committed, published, or served from the public repository.
The project still needs public evidence, coverage summaries, and derived inventory
products.

## Decision

- Raw LAS/LAZ files, private manifests, and private path listings stay private.
- Derived datasets may be public after review. This includes:
  - aggregated inventory and coverage summaries;
  - a tile index that uses stable `tile_id` values rather than source filenames;
  - DEM/DSM/CHM or other raster products derived from the point cloud;
  - first-return metric tables and inventory predictions;
  - model cards and validation summaries.
- Public derived products must cite the private source at the dataset level without
  exposing raw filenames, personal paths, or point payloads.
- Publication of a derived product requires a provenance note and a review of the
  source licence/permission.
- Raw point data is never committed to Git and is not redistributed.

## Consequences

- `pipeline/ingest_private_lidar.py` writes a private summary and, optionally, a
  redacted public summary and tile index.
- Public tile indexes use `tile_id` values; the private summary holds the filename
  mapping.
- A derived product is not automatically public: it needs review and a provenance
  note before it is committed or published.
- The private upload can support a public model result, but not a public raw dataset.

## References

- `notes/reports/p13-pointcloud-acquisition-request.md`
- `notes/reports/p14-ingest-runbook.md`
