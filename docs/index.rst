FEMIC GNN Prototype
===================

A prototype FEMIC/ws4 model for the Gwa'sala-'Nakwaxda'xw Nations (GNN)
traditional territory, built from the stabilized TSA 46 and TSA 47 base
models.

.. warning::

   **Volume-only caveat:** this release has no operability classification,
   harvest cost, haul/barge cost, grade/sort decomposition, log prices, or net
   revenue. It is not a "sustainable harvest level" and it is not financially
   assessed.

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
   * - GNN AOI inside TSA 46/47
     - 682,155.05 ha
   * - Clipped stand area
     - 250,461.39 ha
   * - Derived calibrated THLB
     - 52,984.42 ha
   * - AUs
     - 39 TSA-prefixed
   * - Blocks
     - 26,801
   * - Derived annual AAC
     - 252,636.75 m3/yr
   * - Benchmark
     - 9/10 decades met
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
   aus
   aoi
   review
   release
   economic-screening
   cost-revenue-contract
   api/index
