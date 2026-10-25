Model build
===========

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

   scripts/build_gnn_model.sh

The base instances are expected at ``../femic-tsa46-instance`` and
``../femic-tsa47-instance``. Runtime outputs are gitignored.

Model
-----

- Combined checkpoint rows: 19,467
- Clipped stand area: 250,461.39 ha
- Derived calibrated THLB: 52,984.42 ha
- AUs: 39, TSA-prefixed
- Fragments after export: 19,466
- ``ws4 validate``: pass

Caveats
-------

- No AU harmonization yet.
- No reviewed GNN THLB netdown.
- No legal AAC.
- GNN review is required before public model outputs.
