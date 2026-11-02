# P14 private LiDAR ingest runbook

Date: 2026-11-02
Status: ready before the upload; no private data received yet.

## Governance

- Raw LAS/LAZ and private manifests stay private.
- Derived datasets may be public after review. See
  `notes/adr/0007-private-lidar-derived-public.md`.
- Never commit raw point files, private filenames, personal paths, or credentials.
- The ingest script is read-only. It does not copy, move, delete, or publish a raw
  file.

## Upload destination

- Globus collection: `GNN TSR LiDAR Upload`
- Collection ID: `40487994-e1d0-4b74-bbf5-56a6b4947c80`
- Point data: `/incoming/<dataset-folder>/`
- Manifest: `/manifests/<dataset>.SHA256SUMS.txt`

As of 2026-11-02, `/incoming/` and `/manifests/` were both empty.

## First check after the upload

```bash
globus ls -l 40487994-e1d0-4b74-bbf5-56a6b4947c80:/incoming/
globus ls -l 40487994-e1d0-4b74-bbf5-56a6b4947c80:/manifests/
```

Do not process a partial transfer. Confirm the manifest is present and the file
count matches the expected upload.

## Stage the data privately

Copy the uploaded folder to the private data workspace, not the public repository.
Keep the directory layout and the `SHA256SUMS.txt` file.

## Run the ingest audit

```bash
python pipeline/ingest_private_lidar.py \
  --root /path/to/private/<dataset-folder> \
  --aoi data/source/aoi/gnn_full.gpkg \
  --request-csv notes/reports/p13-gnn-pointcloud-acquisition-request.csv \
  --output-dir /path/to/private/<dataset-folder>/ingest-private \
  --public-dir /path/to/private/<dataset-folder>/ingest-public \
  --verify-hashes
```

Hashing 2 TB is slow. For a first structural check, omit `--verify-hashes` and run
the full hash check once the transfer is confirmed complete.

## Review before any publication

Check the private summary:

- manifest entries, missing files, extra files, and hash mismatches;
- file CRS, vertical datum, point counts, and density;
- coverage against the GNN AOI;
- which P13 high-priority plots are covered;
- any untransformed tiles with unknown CRS.

Do not publish the private summary. If the dataset is usable, review the public
summary and tile index, add provenance, and cite the private source at the dataset
level. The public tile index uses `tile_id` values, not filenames.

## Withdraw the P13 request for covered plots

If the private dataset covers a P13 high-priority plot, mark that plot as satisfied
in the acquisition memo and do not request a duplicate public acquisition for it.

## Next processing step

Only after the coverage review:

1. derive DEM/DSM/CHM and first-return metrics for the covered plots;
2. join the metrics to the FAIB plot visits;
3. fit a GNN-specific card with a temporal or spatial holdout;
4. publish only the reviewed derived products.
