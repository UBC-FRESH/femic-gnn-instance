Cost and revenue contract
=========================

Status: P3.2 contract design. Synthetic fixture only; not a GNN result.

Purpose
-------

This contract makes every block and treatment traceable from volume to net
revenue. It is the interface between the ws4 schedule, FHOPS harvest costs, a
haul/barge layer, and a grade/sort price deck.

No row may carry a price, cost, or recovery value without provenance. A
scenario cannot be labelled "sustainable" from this contract alone; it must also
pass the operability and financial gates in P3.5.

Tables
------

### 1. `block_treatment_cost.csv`

One row per block x treatment x year.

.. list-table::
   :header-rows: 1
   :widths: 28 12 60

   * - Field
     - Unit
     - Meaning
   * - `schema_version`
     - text
     - Contract version, currently `1`.
   * - `block_id`
     - text
     - ws4 block identifier.
   * - `treatment`
     - text
     - Treatment code, such as `CC`.
   * - `year`
     - integer
     - Harvest year.
   * - `operability_class`
     - text
     - `ground`, `cable`, `heli`, or `unknown`.
   * - `harvest_system`
     - text
     - FHOPS harvest-system ID.
   * - `area_ha`
     - ha
     - Harvest area.
   * - `volume_m3`
     - m3
     - Total harvested volume.
   * - `harvest_cost_cad`
     - CAD
     - FHOPS machine/harvest cost.
   * - `move_in_cost_cad`
     - CAD
     - Mobilisation/move-in.
   * - `road_cost_cad`
     - CAD
     - Road/landing cost attributable to the block.
   * - `haul_cost_cad`
     - CAD
     - Truck haul to the transfer/sort/water point.
   * - `barge_cost_cad`
     - CAD
     - Marine/barge cost, if used.
   * - `overhead_cost_cad`
     - CAD
     - Allocated overhead.
   * - `total_cost_cad`
     - CAD
     - Sum of the cost fields.
   * - `currency`
     - text
     - `CAD`.
   * - `cost_source`
     - text
     - Source or model version.
   * - `cost_date`
     - ISO date
     - Date of the cost deck.
   * - `confidence`
     - text
     - `low`, `medium`, or `high`.
   * - `data_status`
     - text
     - `synthetic`, `prototype`, `representative_fhops_phase_i`, or `reviewed`.

### 2. `block_treatment_assortment.csv`

One row per block x treatment x year x species/grade/sort.

.. list-table::
   :header-rows: 1
   :widths: 28 12 60

   * - Field
     - Unit
     - Meaning
   * - `schema_version`
     - text
     - Contract version.
   * - `block_id`
     - text
     - Join key.
   * - `treatment`
     - text
     - Join key.
   * - `year`
     - integer
     - Join key.
   * - `species`
     - text
     - Species or species group.
   * - `grade`
     - text
     - Log grade.
   * - `sort`
     - text
     - Destination/product sort.
   * - `volume_m3`
     - m3
     - Assortment volume.
   * - `price_per_m3_cad`
     - CAD/m3
     - Delivered or at-destination price.
   * - `revenue_cad`
     - CAD
     - `volume_m3 * price_per_m3_cad`.
   * - `price_date`
     - ISO date
     - Price deck date.
   * - `price_source`
     - text
     - Price deck source.
   * - `recovery_source`
     - text
     - Grade/sort recovery source.
   * - `confidence`
     - text
     - `low`, `medium`, or `high`.

Integration boundary
--------------------

- **ws4** supplies the block, treatment, year, area, age, and volume. It remains
  the growth and scheduling model.
- **FHOPS** supplies the harvest system, machine productivity, and machine cost
  for each block/treatment/system.
- **This pipeline** supplies the operability class, road/landing/transfer
  assumptions, truck haul, barge rate, grade/sort recovery, and price deck.
- The first implementation writes sidecar cost and assortment tables joined to
  the ws4 schedule. It does not change the ws4 growth curves or the volume
  benchmark. A later step may add ws4 cost/revenue accounts if the sidecar
  proves stable.

Validation rules
----------------

- Join keys must be unique in the cost table and present in the assortment table.
- `volume_m3` and prices must be non-negative.
- Assortment volumes for a join key must sum to the cost-table volume within a
  documented tolerance.
- `total_cost_cad` must equal the sum of the five cost components.
- `revenue_cad` must equal `volume_m3 * price_per_m3_cad` within rounding.
- Provenance fields must be non-empty.
- A `sustainable` scenario may not contain `operability_class=unknown`,
  `data_status=synthetic`, or missing prices/costs.
- Cable and helicopter blocks must be reported separately; they may not be
  folded into a ground-based average.

Net revenue
-----------

For each block x treatment x year:

``net_revenue_cad = sum(revenue_cad) - total_cost_cad``

The scenario report must show:

- gross revenue,
- harvest, move-in, road, haul, barge, and overhead cost,
- net revenue by year and decade,
- NPV at a documented discount rate,
- the share of volume with complete cost/revenue coverage,
- loss-making blocks and unsupported systems.

Sustainable gate
----------------

A scenario cannot be labelled "sustainable" unless:

1. Every scheduled block has a feasible operability class and harvest system.
2. Haul and barge assumptions are explicit and sourced.
3. Every volume has a grade/sort and a dated price, or a documented residual.
4. Net revenue is non-negative by decade under the base deck.
5. NPV is non-negative under the base deck.
6. A documented price/cost sensitivity does not reverse a positive conclusion.

Failure of any item leaves the scenario at "volume-only" or "costed prototype",
not "sustainable".

Synthetic fixture
-----------------

`config/cost_revenue/synthetic/` contains a deliberately small fixture for
schema testing. It is marked `data_status=synthetic` and
`cost_source=SYNTHETIC_FIXTURE_DO_NOT_USE`. It is not a GNN result and must not
be cited as a cost or price estimate.
