Cost and revenue contract
=========================

Status: contract design. Synthetic fixture only; not a GNN result.

Purpose
-------

This contract makes every block and treatment traceable from volume to net
revenue. It is the interface between the WS4 schedule, Forest Harvesting
Operations Planning System (FHOPS) harvest costs, a haul/barge layer, and a
grade/sort price deck.

No row may carry a price, cost, or recovery value without provenance. A
scenario cannot be labelled "sustainable" from this contract alone; it must also
pass the operability and financial gates.

Tables
------

1. ``block_treatment_cost.csv``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
     - `synthetic`, `prototype`, `upstream_fhops_fixture_api_test`, or `reviewed`.

2. ``block_treatment_assortment.csv``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
- Every scheduled block must have ``direct_net_revenue_cad`` and
  ``net_revenue_cad``. A negative block must be excluded or marked
  ``forced_access=true`` with a stated reason.
- The sum of shared-pool allocations must equal the pool total within the
  documented tolerance.
- Cable and helicopter blocks must be reported separately; they may not be
  folded into a ground-based average.

Net revenue and shared costs
----------------------------

For each block x treatment x year:

``direct_net_revenue_cad = sum(revenue_cad) - direct_cost_cad``

``net_revenue_cad = direct_net_revenue_cad - allocated_shared_cost_cad``

Direct costs stay with the block: harvest, move-in, block-specific haul,
block-specific barge/terminal charges, and directly attributable overhead.

Costs that serve multiple blocks are placed in a **shared-cost pool** and
allocated with a documented driver. Examples:

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Shared cost
     - Preferred driver
     - Rule
   * - Road construction, decommissioning, landings, culverts, bridges
     - volume served, area served, or scheduled access-years
     - Pool by road segment/landing. Amortise over the scheduled blocks and
       years that use it; true up any residual at the end of the scenario.
   * - Terminal fixed cost, boom tending, storage
     - volume or trips
     - Allocate to the blocks using that terminal. Do not also charge the same
       terminal cost directly to a block.
   * - Shared truck or barge fixed cost
     - volume, tonne-km, or trips
     - Use one documented driver consistently within a scenario.
   * - General overhead
     - volume or area
     - If a defensible driver is unavailable, report it as unallocated and
       flag the block result as incomplete.

Required fields:

- ``direct_cost_cad``
- ``allocated_shared_cost_cad``
- ``net_revenue_cad``
- ``shared_cost_pool_id``
- ``allocation_method``
- ``allocation_basis``
- ``allocation_year``
- ``forced_access``

Rules:

- A cost belongs to either a block or a shared pool, never both.
- The sum of allocations from a pool must equal the pool total within a stated
  tolerance.
- If a cost cannot be allocated defensibly, report the block's direct result
  and the unallocated balance separately. Do not invent an allocation.
- A block may be negative on direct cost but positive after shared allocation,
  or the reverse. Show both numbers.
- A negative block may be scheduled only if it is explicitly marked
  ``forced_access=true`` and the scenario report states the reason, the shared
  cost it enables, and the scenario-level effect. It is not hidden by a
  positive decade.
- The scenario report must show gross revenue; direct, shared, and total cost;
  direct and allocated net revenue by block; net revenue by year and decade;
  NPV at a documented discount rate; cost/revenue coverage; loss-making blocks;
  and forced-access exceptions.

Sustainable gate
----------------

A scenario cannot be labelled "sustainable" unless:

1. Every scheduled block has a feasible operability class and harvest system.
2. Haul and barge assumptions are explicit and sourced.
3. Every volume has a grade/sort and a dated price, or a documented residual.
4. Every scheduled block has non-negative ``net_revenue_cad`` under the base
   deck after documented shared-cost allocation. A negative block must be
   excluded, or marked ``forced_access=true`` with a stated reason and a
   scenario-level reconciliation.
5. Net revenue is also non-negative by decade under the base deck.
6. NPV is non-negative under the base deck.
7. A documented price/cost sensitivity does not reverse a positive conclusion.

Failure of any item leaves the scenario at "volume-only" or "costed prototype",
not "sustainable".

Synthetic fixture
-----------------

`config/cost_revenue/synthetic/` contains a deliberately small fixture for
schema testing. It is marked `data_status=synthetic` and
`cost_source=SYNTHETIC_FIXTURE_DO_NOT_USE`. It is not a GNN result and must not
be cited as a cost or price estimate.
