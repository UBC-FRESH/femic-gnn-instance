Economic screening
==================

Status: **diagnostic screening**, not a sustainable or financially calibrated
result. The model release remains volume-only.

What This Page Shows
--------------------

This page asks a limited question:

> If the current class-average harvest and transport assumptions are applied,
> which part of the assumed timber harvesting land base has positive net
> revenue?

The answer is an area share under those assumptions. It is not a financial
forecast, a current quote, or a sustainable harvest level.

The screen is at the polygon level of the **Vegetation Resources Inventory
(VRI)**. The **timber harvesting land base (THLB)** is the area assumed
available for timber harvest in this prototype. It is derived, not a legal
land-base determination. See :doc:`glossary` for terms.

Coverage
--------

The screen covers **53.0 thousand ha of derived THLB**.

Results
-------

Positive net revenue by case:

.. list-table::
   :header-rows: 1
   :widths: 38 30 20

   * - Case
     - Positive THLB (thousand ha)
     - Share
   * - Low price/recovery, high transport
     - 46.6
     - **88.0%**
   * - Base
     - 50.6
     - **95.5%**
   * - High price/recovery, low transport
     - 51.3
     - **96.8%**

"Positive THLB" means area where modeled log value exceeds modeled harvest and
transport cost. It does not include road/landing construction, overhead,
profit, or silviculture cost.

This page is an area screen, not a schedule. A block-level gate is defined in
:doc:`cost-revenue-contract`: do not schedule a block with negative net revenue
under the base deck unless it is explicitly marked as a forced access or
infrastructure block with a stated reason. The 4.5% of THLB that is non-positive
in the base case is the area that gate would exclude.

Block-level diagnostic
~~~~~~~~~~~~~~~~~~~~~~

A direct-cost pass mapped the screen to **7,848 screened blocks** (of 19,366
block supports). It found **478 negative blocks**, covering **2.4 thousand ha**
of THLB (**4.5%**). The negative share is highest for helicopter candidates
(**9.3%**), then ground (**3.4%**) and cable (**2.6%**). About **0.3 thousand ha**
of the screened THLB did not map to block support.

This is still a partial gate: shared road, landing, terminal, and overhead
costs are unallocated. The block list is available in
`notes/reports/block-level-revenue-screen.md
<https://github.com/UBC-FRESH/femic-gnn-instance/blob/main/notes/reports/block-level-revenue-screen.md>`_.

By harvest system in the base case:

.. list-table::
   :header-rows: 1
   :widths: 24 20 18 22

   * - Harvest system
     - THLB (thousand ha)
     - Share
     - Positive share
   * - Ground
     - 29.1
     - 54.8%
     - 96.6%
   * - Cable
     - 12.3
     - 23.3%
     - 97.4%
   * - Helicopter candidate
     - 11.6
     - 21.9%
     - 90.8%

Sensitivity: **87.8%** of the THLB is positive at twice the modeled harvest
cost; **92.3%** is positive at a transport cost of **$30/m³**.

Assumptions and Limits
----------------------

- **Terrain.** The screen uses a coarse digital elevation model (DEM) sampled
  at one point per polygon. It is not LiDAR and not a block-level slope mean.
- **Newer terrain fields.** The 30 m public terrain and VRI fields are
  descriptive and are **not used** here. The 10 m LiDAR pilot is not
  model-wide. See :doc:`indicators`.
- **Harvest cost.** Class-average whole-system costs from the Forest Harvesting
  Operations Planning System (FHOPS): ground **$15.37/m³**, cable
  **$17.77/m³**, helicopter **$78.13/m³**. These are registry averages, not
  current contractor rates.
- **Transport cost.** The legacy assumption is 100 km truck + 100 km barge +
  transload at **$10.96/m³**. A transload is a transfer between truck and
  barge. This is an assumption, not a current carrier quote.
- **Prices.** BC Coast Log Market Reports for the three months ending
  2026-01-31. The public source reports are the
  `second-growth report <https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/timber-pricing/coast-timber-pricing/coast-log-reports/3m2gc_jan_26.pdf>`_
  and the
  `old-growth report <https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/timber-pricing/coast-timber-pricing/coast-log-reports/3mc_jan_26.pdf>`_.
  The local extracted deck and its manual check are recorded in the
  `price-source note <https://github.com/UBC-FRESH/femic-gnn-instance/blob/main/notes/reference/log-price-sources.md>`_
  and the `price-deck validation note <https://github.com/UBC-FRESH/femic-gnn-instance/blob/main/notes/reference/price-deck-validation.md>`_.
  The extracted table is retained locally for reproducibility and is not
  redistributed; use the linked public reports to review or challenge the
  prices.
- **Recovery.** A provisional log grade and product recovery matrix, with
  reject/waste cases of 2%, 5%, and 10%.
- **Missing costs.** Road and landing construction, overhead, profit, and
  silviculture are excluded.

Marine Transport Test
---------------------

FHOPS includes a marine/barge transport test. The test route is a synthetic
**Sunshine Coast to Howe Sound** case. It is not a GNN route or a current quote,
and it is not used in this screen. A separate internal route test uses
**Quatsino Sound to Ladysmith Harbour**; it is diagnostic only and is not used
here.

The GNN area of interest is northern Vancouver Island. There is no confirmed
GNN terminal, current carrier rate, or observed route distance in this
prototype.

What This Does Not Mean
-----------------------

This is a screening estimate. It does not establish that a block is profitable,
operable, or sustainable. It does not replace:

- a reviewed land-base determination,
- current contractor and carrier quotes,
- observed log grade and product recovery, or
- field validation of terrain and stand data.

Terms are defined in :doc:`glossary`. Inputs and limits are also recorded in
the internal reference notes.
