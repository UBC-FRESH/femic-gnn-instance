# FHOPS hauling gap: barge/marine legs

Date: 2026-10-25
Status: upstream feature request open; no barge support in FHOPS hauling yet.

## Tested

FHOPS `main` at `52462d2a` (P11 log hauling and mill delivery).

The new `fhops.hauling` layer models truckloads, truck types, trucks, depots, sort yards, haul
arcs, loader locations, and driver policy. It has no transport mode, vessel/barge entity, port,
or barge-cycle structure.

A Sunshine Coast -> Howe Sound barge-shaped case was derived from `examples/hauling/`:

- one `log_barge` `TruckType` with 3,000 m3 capacity
- one barge-named `Truck`
- three water-length haul arcs (240-280 minutes)
- one sort yard

`fhops haul validate` accepts it as a truck scenario. `fhops haul plan` returns infeasible under
the truck-only model. Validation is a schema alias, not marine support.

## Upstream issue

`UBC-FRESH/fhops#187`:
https://github.com/UBC-FRESH/fhops/issues/187

Requested: explicit water mode, barge/vessel type, ports/terminals, water arcs, terminal handling,
barge cycles, Phase I/II/III support, a Sunshine Coast -> Howe Sound fixture, and tests/docs.

## Consequence for the GNN model

- Do not treat a `log_barge` `TruckType` as marine support.
- The GNN transport layer currently uses the legacy CLEWs/FFCM diagnostic barge rates, not the FHOPS
  hauling optimizer.
- Until FHOPS #187 lands, barge scheduling and port synchronization remain a separate screening
  assumption, not a solved haul plan.
- The sustainable gate must keep transport labelled diagnostic for barge legs.
