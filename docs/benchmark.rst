Prototype benchmark
===================

This is a **volume-only prototype benchmark**, not a legal AAC and not a
"sustainable harvest level". It has no validated operability, cost, or net
revenue model. A diagnostic economic screen and descriptive terrain/VRI
indicators exist, but they are not part of this volume benchmark. See :doc:`release` and
:doc:`indicators`.

This is a **derived prototype benchmark**, not a legal AAC.

The annual value is the THLB-weighted share of the published TSA 46 and TSA 47
AACs:

``803,000 * 18,412/268,970 + 830,500 * 34,573/145,256 ≈ 252,637 m3/yr``

The decade target is 2,526,000-2,527,000 m3.

Opening-first result
--------------------

- Openings: 3,158
- Scheduled blocks: 5,618
- Scheduled area: 39.6 thousand ha
- Opening range: 5.0-39.8 ha
- Patch classes: 100% 5-40 ha

Decade result
-------------

.. list-table::
   :header-rows: 1
   :widths: 10 25 14

   * - Decade
     - Realized volume (m3)
     - Status
   * - 1
     - 2,526,514
     - met
   * - 2
     - 2,526,661
     - met
   * - 3
     - 2,526,840
     - met
   * - 4
     - 2,526,855
     - met
   * - 5
     - 2,526,957
     - met
   * - 6
     - 2,526,893
     - met
   * - 7
     - 2,526,314
     - met
   * - 8
     - 2,526,476
     - met
   * - 9
     - 2,526,927
     - met
   * - 10
     - 2,525,219
     - within 0.04%

All decades are effectively at target. The largest deviation is 0.04%, at the
100-year horizon end. No production curve or legal AAC was changed.

Ground-plot validation
-----------------------

The available non-PSP ground plots were filtered to the GNN AOI:

- 34 matched rows, 10 sites, TSA 47 only
- VRI 31, CMI 1, NFI 2

.. csv-table:: Available non-PSP ground-plot bias by sample
   :header: Sample, n, Volume bias, DBH bias, Height bias, Stems bias
   :widths: 18, 8, 24, 18, 20, 20
   :align: left

   VRI, 31, -118.1 m³/ha, -5.1 cm, +0.1 m, -341.9 sph
   NFI, 2, -104.4 m³/ha, +1.2 cm, -2.3 m, -434.1 sph
   CMI, 1, -149.4 m³/ha, -7.5 cm, -6.0 m, +160.8 sph

Negative values indicate underprediction. ``sph`` is stems per hectare.

This is too sparse for a GNN-specific accuracy conclusion. The direction is
consistent with the larger TSA 47 validation, but no TSA 46 managed plots fall
inside the AOI. The inherited base-model validation remains the primary
accuracy evidence. No curve or AAC target was changed.


The public-plot inventory also found 24 PSP sites inside the AOI: 17 experimental
(``PSP_R``) and 7 natural-growth (``PSP_G``). A filtered PSP check produced 55
observations from 12 sites, but the median age is 101 years and the sample is
not a managed-young TIPSY benchmark. It does not change the conclusion: the
managed-curve evidence remains too sparse.


Release condition
-----------------

The derived THLB and AAC are sufficient for a labelled **prototype** only. They
are not sufficient for operational, legal, or investment decisions. An
operational release requires a reviewed GNN netdown and an explicit AAC
decision. See ADR 0006.


Decade-10 diagnostic
--------------------

The 100-year horizon closes within 0.04% of the target band. The detailed
horizon and age-structure diagnostic is retained in
`notes/reference/decade10-diagnostic.md` in the repository; it is not a material
benchmark shortfall.

No curve, target, THLB, AAC, or benchmark change is made.

