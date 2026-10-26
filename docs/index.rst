FEMIC GNN Prototype
===================

A prototype FEMIC/ws4 model for the Gwa'sala-'Nakwaxda'xw Nations (GNN)
traditional territory, built from the stabilized TSA 46 and TSA 47 base
models.

.. warning::

   **Volume-only caveat:** this release does not contain a validated
   operability, cost, or net revenue model. A diagnostic economic screen and descriptive terrain/VRI
   indicators exist, but they do not change the release label. It is
   not a "sustainable harvest level" and it is not financially assessed.

   The boundary is the **proposed GNN Statement of Intent** polygon, not a
   final treaty boundary or a legal title determination. Confirm it with GNN
   before public or operational use. The THLB and AAC below are derived
   prototype values, not legal determinations.

Model at a glance
-----------------

.. list-table::
   :header-rows: 1
   :widths: 32 55

   * - Quantity
     - Value
   * - GNN AOI inside TSA 46/47 (thousand ha)
     - 682.2
   * - Clipped stand area (thousand ha)
     - 250.5
   * - Derived calibrated THLB (thousand ha)
     - 53.0
   * - AUs
     - 39 TSA-prefixed
   * - Blocks
     - 26,801
   * - Derived annual AAC
     - 252,637 m3/yr
   * - Benchmark
     - All 10 decades within 0.04% of target
   * - LiDAR pilot
     - 181 fragments / 184 blocks / 979 ha (not model-wide)
   * - Public terrain/VRI
     - Descriptive proxies only; not used for operability
   * - Web UI
     - loopback port 8019

Build
-----

The prototype clips the calibrated TSA 46/47 checkpoints to the GNN AOI,
combines the two FEMIC bundles, and exports one Patchworks/ws4 model:

.. code-block:: bash

   pipeline/build_gnn_model.sh
   ./serve_gnn_calibrated.sh

See :doc:`model-build`, :doc:`benchmark`, and :doc:`aoi`.

.. toctree::
   :maxdepth: 2

   benchmark
   model-build
   indicators
   aus
   aoi
   review
   release
   economic-screening
   cost-revenue-contract
   api/index
