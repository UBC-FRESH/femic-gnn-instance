Model build
===========

Workflow versus pipeline
------------------------

``scripts/`` holds the workflow validator and green dashboard. ``pipeline/``
holds the build and analysis entry points. The strict lint, type, docstring,
and coverage gates apply to ``scripts/`` and ``tests/``; the pipeline is
validated by execution and ``ws4 validate``. See ``pipeline/README.md`` in the
repository.

Method
------

The prototype reuses the stabilized base models:

1. Clip the calibrated TSA 46/47 checkpoints to the GNN AOI.
2. Combine the clipped checkpoints; keep TSA-prefixed AU ids.
3. Combine the TSA 46/47 FEMIC bundles.
4. Export one Patchworks XML/fragments model.
5. Merge safe slivers and build/validate the ws4 matrix.
6. Build the topology and opening-first schedule.
7. Simulate and report the derived benchmark.

Command
-------

.. code-block:: bash

   pipeline/build_gnn_model.sh

The base instances are expected at ``../femic-tsa46-instance`` and
``../femic-tsa47-instance``. Runtime outputs are gitignored.

Optional terrain and canopy indicators
---------------------------------------

``build_gnn_model.sh`` builds the growth/scheduling model only. The terrain and canopy
indicator fields are a separate, optional integration and are not model
semantics:

.. code-block:: bash

   # LidarBC materialization is about 5.5 GiB and data/lidar/ is gitignored.
   python -m femic lidar materialize \
     --selection-manifest metadata/lidar/lidarbc_selection_dem_dsm.json \
     --output-root data/lidar

   python pipeline/build_gnn_lidar_products.py \
     --aoi data/source/aoi/gnn_full.gpkg \
     --materialization data/lidar/materialization.json \
     --output-dir data/lidar/gnn_10m \
     --bundle-dir data/lidar/products/lidarbc-gnn-10m

   python pipeline/integrate_gnn_lidar.py \
     --dataset runtime/gnn/matrix \
     --bundle data/lidar/products/lidarbc-gnn-10m \
     --fragments output/patchworks_gnn/fragments_merged/fragments.shp

   python pipeline/build_gnn_public_indicators.py \
     --dataset runtime/gnn/matrix \
     --cache-dir runtime/gnn/public_terrain/terrarium_z12 \
     --output-dir runtime/gnn/public_terrain

Requirements: the FEMIC LiDAR producer and the WS4 LiDAR consumer
(including the multi-track block fix). The LiDAR result is a bounded
181-fragment / 184-block pilot; the 30 m Terrarium/VRI fields are descriptive
only. Do not use them for operability thresholds or CHM claims. See
:doc:`indicators` and the indicator reports.

Model
-----

- Combined checkpoint rows: 19,467
- Clipped stand area: 250.5 thousand ha
- Derived calibrated THLB: 53.0 thousand ha
- AUs: 39, TSA-prefixed
- Fragments after export: 19,466
- ``ws4 validate``: pass

Caveats
-------

- No AU harmonization yet.
- No reviewed GNN THLB netdown.
- No legal AAC.
- GNN review is required before public model outputs.
