Prototype benchmark
===================

This is a **volume-only prototype benchmark**, not a legal AAC and not a
"sustainable harvest level". It has no operability, harvest cost, haul/barge
cost, grade/sort revenue, or net revenue. See :doc:`release`.

This is a **derived prototype benchmark**, not a legal AAC.

The annual value is the THLB-weighted share of the published TSA 46 and TSA 47
AACs:

``803,000 * 18,411.68/268,970 + 830,500 * 34,572.74/145,256 = 252,636.75 m3/yr``

The decade target is 2,526,000-2,527,000 m3.

Opening-first result
--------------------

- Openings: 3,158
- Scheduled blocks: 5,618
- Scheduled area: 39,558.5 ha
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
     - 2,526,514.4
     - met
   * - 2
     - 2,526,660.9
     - met
   * - 3
     - 2,526,839.9
     - met
   * - 4
     - 2,526,854.5
     - met
   * - 5
     - 2,526,957.3
     - met
   * - 6
     - 2,526,892.9
     - met
   * - 7
     - 2,526,314.0
     - met
   * - 8
     - 2,526,476.2
     - met
   * - 9
     - 2,526,926.8
     - met
   * - 10
     - 2,525,218.6
     - **below by 781.4**

The decade-10 miss is recorded, not hidden. It is a prototype result; no
production curve or legal AAC was changed.

Ground-plot validation
-----------------------

The available non-PSP ground plots were filtered to the GNN AOI:

- 34 matched rows, 10 sites, TSA 47 only
- VRI 31, CMI 1, NFI 2

| Sample | n | Volume bias | DBH bias | Height bias | Stems bias |
| --- | ---: | ---: | ---: | ---: | ---: |
| VRI | 31 | -118.1 m3/ha | -5.1 cm | +0.1 m | -341.9 sph |
| NFI | 2 | -104.4 m3/ha | +1.2 cm | -2.3 m | -434.1 sph |
| CMI | 1 | -149.4 m3/ha | -7.5 cm | -6.0 m | +160.8 sph |

This is too sparse for a GNN-specific accuracy conclusion. The direction is
consistent with the larger TSA 47 validation, but no TSA 46 managed plots fall
inside the AOI. The inherited base-model validation remains the primary
accuracy evidence. No curve or AAC target was changed.


The P1.2 inventory also found 24 PSP sites inside the AOI: 17 experimental
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

The scheduler is deterministic. Lowering the target to the band floor
(2,526,000 m3) did not fix decade 10: it produced 2,524,255.0 m3, still below
the band. The last period already has the most scheduled blocks (866), so the
miss is a 100-year horizon and age-structure end-effect, not a curve or target
error. The 522 openings that become ready after year 90 are dropped.

No curve, target, THLB, AAC, or benchmark change is made. See
`notes/reference/decade10-diagnostic.md` in the repository.

