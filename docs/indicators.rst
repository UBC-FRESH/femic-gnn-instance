Terrain, VRI, and LiDAR Indicators
==================================

Status: **current; descriptive and pilot-only. No model semantics.**

The GNN instance carries three indicator families. They are not interchangeable:

- **Model-wide public terrain proxy** from AWS Open Data Terrarium.
- **Model-wide VRI stand proxy** from the existing public inventory checkpoint.
- **Bounded LiDAR pilot** from LidarBC, covering only a small southern part of
  the AOI.

None of these fields changes the volume-only release. None is used as a
validated operability threshold, CHM, biomass measurement, or biodiversity
claim.

At a Glance
-----------

.. list-table::
   :header-rows: 1
   :widths: 26 20 28 26

   * - Indicator
     - Source
     - Coverage
     - Use
   * - `terrain_*`
     - AWS Open Data Terrarium, zoom 12, 30 m
     - 26,762 / 26,801 fragments; 19,331 / 19,366 block supports; 39 gaps
     - Descriptive public terrain proxy
   * - `vri_*`
     - GNN VRI checkpoint
     - 26,801 / 26,801 fragments; 19,366 / 19,366 block supports
     - Stand-inventory proxy
   * - `lidar_*`
     - LidarBC 10 m DEM/DSM
     - 181 direct fragments; 184 blocks; 979 ha
     - Bounded validation pilot

The 10 m LiDAR tile union intersects only **2.5%** of the GNN AOI. The valid
10 m land area inside the AOI is **4,660 ha**. The model-wide terrain and VRI
fields are the only fields available across the AOI.

Fields
------

Terrain
~~~~~~~

- ``terrain_source`` = ``aws-terrarium-z12-30m``
- ``terrain_resolution_m`` = ``30``
- ``terrain_method`` = ``block_zonal_terrarium_horn``
- ``terrain_valid_fraction``
- ``terrain_elev_mean_m``
- ``terrain_slope_mean_pct``
- ``terrain_slope_p90_pct``
- ``terrain_slope_max_pct``
- ``terrain_available``
- ``terrain_valid_pixels``
- ``terrain_valid_area_ha``

The terrain is a coarse public DEM. It is not LiDAR, a survey, or a
geotechnical product.

VRI
~~~

- ``vri_source`` = ``gnn-vri-checkpoint``
- ``vri_join_method`` = ``block_area_weighted_vri``
- ``vri_height_m``
- ``vri_crown_closure_pct``
- ``vri_live_volume_125_m3_ha``
- ``vri_whole_stem_biomass_ha``
- ``vri_available``
- ``vri_valid_area_ha``

``vri_height_m`` comes from the VRI ``LABEL_HEIGHT`` field. The checkpoint
stores label height in decimetres; it is converted to metres. It is not CHM,
DBH, true stems/ha, or measured biomass.

LiDAR
~~~~~

- ``lidar_slope_mean``, ``lidar_slope_p95``
- ``lidar_slope_valid_pixels``
- ``lidar_chm_mean``, ``lidar_chm_p95``
- ``lidar_chm_cover_ge_2``, ``_5``, ``_10``, ``_20``
- ``lidar_chm_valid_pixels``
- ``lidar_available``
- ``lidar_supported_ha``

The LiDAR bundle is ``lidarbc-1b7b79757e98cfe5`` /
``2026.10.0-gnn-10m``. It contains derived ``slope``, ``chm``, and ``canopy``
products. The source DEM/DSM are not packaged because the FEMIC plan labels
them as non-derived source products.

Validation
----------

The public proxies were compared with the 181 direct fragments / 184 blocks
that have LiDAR support. The comparison is block-level; the public proxies are
30 m and the LiDAR is 10 m.

.. list-table::
   :header-rows: 1
   :widths: 34 7 13 13 14 10 10 7

   * - Comparison
     - n
     - Proxy mean
     - LiDAR mean
     - Bias
     - MAE
     - RMSE
     - r
   * - Terrarium mean slope vs LiDAR mean slope
     - 184
     - 19.33%
     - 32.99%
     - -13.66
     - 13.97
     - 16.18
     - 0.63
   * - Terrarium p90 slope vs LiDAR p95 slope
     - 184
     - 28.77%
     - 68.78%
     - -40.01
     - 40.13
     - 43.07
     - 0.67
   * - VRI height vs LiDAR CHM mean
     - 184
     - 11.10 m
     - 10.60 m
     - +0.50
     - 4.09
     - 5.06
     - -0.38
   * - VRI height vs LiDAR CHM p95
     - 184
     - 11.10 m
     - 19.56 m
     - -8.46
     - 8.95
     - 10.70
     - -0.28

Decision:

- The Terrarium fields are **descriptive screening proxies only**.
- Do not replace ground/cable/heli slope thresholds with Terrarium values
  without local calibration and specialist review.
- The VRI height fields are **stand-inventory proxies only**; they are not CHM
  and do not predict canopy height reliably at block scale.
- Keep the LiDAR pilot as the only high-resolution terrain/canopy evidence.
- Do not extrapolate, impute, or tune a correction from this pilot.
- The release remains volume-only.

Provenance and Integration
--------------------------

The compiled dataset is ``runtime/gnn/matrix``. The manifest records:

- ``metadata.lidar_fields``: bundle id/version, field list, mapping checksums.
- ``metadata.public_indicators``: terrain/VRI source, resolution, join method,
  field list.

Backups:

- ``runtime/gnn/matrix_pre_lidar`` — before LiDAR integration.
- ``runtime/gnn/matrix_pre_public`` — before public terrain/VRI integration.

Only ``fragments.parquet``, ``blocks.parquet``, and ``manifest.json`` change
during these integrations. Curves, treatments, tracks, strata, features,
products, accounts, protoaccounts, groups, and messages are unchanged.

Rebuild
-------

The main model build (``pipeline/build_gnn_model.sh``) does **not** run the optional indicator build.
Install or expose the FEMIC LiDAR producer and the WS4 LiDAR consumer
(including the multi-track block fix), then run:

.. code-block:: bash

   # 1. Materialize 549 LidarBC DEM/DSM tiles. Large payloads stay out of git.
   python -m femic lidar materialize \
     --selection-manifest metadata/lidar/lidarbc_selection_dem_dsm.json \
     --output-root data/lidar

   # 2. Build and validate the 10 m strategic bundle.
   python pipeline/build_gnn_lidar_products.py \
     --aoi data/source/aoi/gnn_full.gpkg \
     --materialization data/lidar/materialization.json \
     --output-dir data/lidar/gnn_10m \
     --bundle-dir data/lidar/products/lidarbc-gnn-10m

   # 3. Register, map, integrate, and validate the LiDAR fields.
   python pipeline/integrate_gnn_lidar.py \
     --dataset runtime/gnn/matrix \
     --bundle data/lidar/products/lidarbc-gnn-10m \
     --fragments output/patchworks_gnn/fragments_merged/fragments.shp

   # 4. Build the model-wide Terrarium/VRI descriptive fields.
   python pipeline/build_gnn_public_indicators.py \
     --dataset runtime/gnn/matrix \
     --cache-dir runtime/gnn/public_terrain/terrarium_z12 \
     --output-dir runtime/gnn/public_terrain

The 549-tile materialization is about **5.5 GiB**. ``data/lidar/`` and
``runtime/`` are gitignored. The selection manifests under ``metadata/lidar/``
are tracked. Do not commit tile payloads, the bundle payloads, or the compiled
dataset.

Evidence
--------

- ``notes/reports/p9-lidar-indicators.md`` — LiDAR coverage and pilot limits.
- ``notes/reports/p9.2-public-data-indicators.md`` — public proxy validation.
- ``notes/plans/p9.2-public-data-indicators.md`` — public-data plan.
- ``notes/reference/operability-cost-revenue.md`` — why terrain/operability
  remains diagnostic.

See also :doc:`model-build`, :doc:`economic-screening`, and :doc:`release`.
