Prototype release notes
=======================

Status: **volume-only prototype / pre-release**. Not a legal or operational release.

.. warning::

   **Volume-only caveat:** this release does not contain a validated
   operability, cost, or net revenue model. A P3 diagnostic screen and P9
   descriptive indicators exist, but the release label remains volume-only. It
   is not a "sustainable harvest level" and it is not financially assessed.

v0.1.0-prototype is a public model and method release for the proposed GNN
Statement of Intent area. It combines the TSA 46 and TSA 47 portions of the
proposed boundary.

At a glance
-----------

.. list-table::
   :header-rows: 1
   :widths: 45 40

   * - Item
     - Value
   * - GNN AOI inside TSA 46/47
     - 682,155.05 ha
   * - Clipped stand area
     - 250,461.39 ha
   * - Derived calibrated THLB
     - 52,984.42 ha
   * - AUs
     - 39 TSA-prefixed
   * - Derived annual AAC
     - 252,636.75 m3/yr
   * - Opening-first benchmark
     - All 10 decades within 0.04% of target

Known gaps
----------

- The boundary is the proposed SOI polygon. P1.1 was closed as deferred by the
  maintainer; no external review is claimed.
- The THLB and AAC are derived and non-legal. Operational use requires a
  reviewed GNN netdown.
- TSA 46 SI/origin remains a base-model dependency
  (`UBC-FRESH/femic#343 <https://github.com/UBC-FRESH/femic/issues/343>`_).
- The managed/young ground-plot sample is too sparse for a confident accuracy
  claim.
- TSA-prefixed AUs are retained; the reporting crosswalk is not a model merge.
- **P9 indicators.** Public LidarBC covers only 2.5% of the AOI and 978.63 ha of
  block support (181 direct fragments / 184 blocks). The 30 m Terrarium/VRI
  proxies are descriptive only and failed validation for absolute operability
  use. There are 39 terrain gaps. See :doc:`indicators`.


Economic screening (diagnostic)
--------------------------------

A P3 screening covers the full derived THLB: **95.5% positive** in the base
case, 88.0-96.8% across the price/recovery range. It uses class-average system
costs, coarse DEM centroid terrain, provisional recovery, and legacy barge/truck
rates. The P9 descriptive fields are not used in this screen. It is
**not** a financial assessment, not a current quote, and not a sustainable
label. See :doc:`economic-screening`.

Links
-----

- Repository: https://github.com/UBC-FRESH/femic-gnn-instance
- Docs: https://ubc-fresh.github.io/femic-gnn-instance/
- Full notes: `notes/releases/v0.1.0-prototype.md` in the repository
