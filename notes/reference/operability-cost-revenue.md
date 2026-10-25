# Operability, cost, and net revenue: capability audit

Date: 2026-10-25
Status: P3.1 audit. No scenario is financially or operationally assessed yet.
Phase: P3 (parent #22)
Related: P3.1 (#23), `notes/releases/v0.1.0-prototype.md`

## Bottom line

The current release is a **volume-only growth and scheduling prototype**. It is
not an operable, costed, profitable, or "sustainable harvest level" model. The
9/10 decade result is a volume benchmark, not a financial or operational claim.

No price, slope, haul, barge, or grade recovery may be invented to close that
gap. The next work is data acquisition and a cost/revenue contract.

## FHOPS capability audit

FHOPS source is available at the sibling `fhops` checkout. It is **not installed
in the current Python environment** (`python -m fhops` fails with
`No module named fhops`). It can be installed editable or used with
`PYTHONPATH=src`.

FHOPS is strong where we need it:

- Ground, cable, steep-tethered, and helicopter harvest systems, with machine
  roles and sequencing.
- Machine owning/operating/repair rates and productivity models.
- Per-machine `$/m3` costing from stand attributes and utilisation.
- Tactical-operational options per block x system x period, with product
  yields, transport arcs, facilities, road access, and discounted
  profit/NPV objective profiles.
- Product-specific `value_per_m3` and transport `cost_per_m3` fields.

FHOPS does not supply, by itself:

- A coastal BC log **grade/sort price deck**.
- A **barge/marine** network or barge rates.
- A block **operability classifier** from terrain/access data.
- A direct ws4 account bridge.
- A defensible 2026 price deck or current coastal market assumptions.

## GNN data audit

The current block table has only `block_id`, `track_id`, `offset`, and `area_ha`.
The ws4 fragments add age and track. The combined checkpoint has VRI species,
volume, and age fields, but no DEM-derived slope, road/landing access, barge
terminal, grade recovery, or price fields.

Missing or not yet materialized:

- DEM/slope/terrain and cable/heli feasibility.
- Roads, landings, water/barge terminals, and haul distances.
- Block-level species/volume/stem-size for FHOPS productivity.
- Harvest-system assignment.
- Grade/sort recovery matrix.
- Log price deck by sort/grade/destination.
- Barge and truck haul cost assumptions.
- Road construction/maintenance and move-in costs.

## Proposed architecture

1. **ws4 stays the growth/scheduling model.** It supplies the candidate block,
   treatment, year, volume, age, and area.
2. **FHOPS evaluates operability and harvest cost.** For each scheduled block
   and treatment, assign a system (ground/cable/heli), run the FHOPS
   productivity/machine-cost layer, and add move-in and road/landing cost.
3. **A custom transport layer** adds truck haul and barge cost by block/landing
   to destination. FHOPS tactical transport arcs can carry the cost, but the
   network and rates are ours.
4. **A custom grade/sort revenue layer** decomposes volume into
   species/grade/sort and applies a dated price deck.
5. **Net revenue** = gross log revenue - harvest - move-in - road/landing -
   truck haul - barge - overhead. Report per block, per decade, and NPV.
6. **The sustainable gate** requires both:
   - operability coverage: every scheduled block has a feasible system and
     access assumption; cable/heli blocks are explicit; and
   - financial feasibility: net revenue is non-negative by decade and NPV is
     non-negative under the base deck, with price/cost sensitivity.
   A volume result alone cannot pass.

## Data acquisition order

1. DEM/slope and terrain; roads/landings; water/barge terminals.
2. Block-level species/volume/stem size from the model and VRI.
3. FHOPS install and a one-block cost smoke test.
4. Coastal log price deck with date/source and sort definitions.
5. Grade/sort recovery assumptions and sensitivity.
6. Contract and gate tests.

## What this changes

- The public release gets a prominent volume-only caveat.
- P3 becomes the active phase; no "sustainable" label is allowed until the gate
  passes.
- No curves, AAC, THLB, or volume targets are changed to make a cost result look
  better.

- One-block sample: `notes/reference/block-sample-14379.md`
- Price source and use limits: `notes/reference/log-price-sources.md`
- FHOPS smoke test: `notes/reference/fhops-smoke-test.md`
- FHOPS data contract: `fhops/docs/howto/data_contract.rst`
- FHOPS harvest systems: `fhops/docs/reference/harvest_systems.rst`
- FHOPS tactical-operational contract:
  `fhops/docs/howto/tactical_operational.rst`
- FHOPS machine costing: `fhops/src/fhops/costing/machines.py`
- GNN AU/area evidence: `config/tsr/gnn_au/`
- Current release caveat: `notes/releases/v0.1.0-prototype.md`
