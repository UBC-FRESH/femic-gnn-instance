# FHOPS hauling marine/barge support

Date: 2026-10-25
Status: upstream gap resolved; GNN adapter implemented as a diagnostic path.

## Resolution

`UBC-FRESH/fhops#187` is closed. FHOPS PR #195 merged as
`f788d7a63113c52159b3a9dbef449d6faf8325e9`.

The hauling layer now has an explicit marine path:

- `TransportMode` distinguishes road and water;
- `BargeType` and `Barge` are first-class vessels, not truck aliases;
- `Port`, `WaterArc`, `PortLeg`, and `MarineRoute` carry the terminal and water
  topology;
- Phase I reports pickup, water, and delivery volumes, barge trips, port
  inventory, and drayage/terminal/barge costs;
- Phase II/III add a deterministic barge-cycle scheduler and synchronized road
  windows; and
- `examples/hauling_marine/` is a synthetic Sunshine Coast -> Howe Sound
  fixture.

## Historical test

FHOPS `main` at `52462d2a` was truck-only. A barge-named `TruckType` validated
as a truck, and `fhops haul plan` was infeasible under the truck model. That
was a schema alias, not marine support. The upstream issue and fixture from
that test are now part of the resolved implementation.

## Consequence for the GNN model

- `pipeline/fhops_marine_transport.py` solves the FHOPS marine fixture and
  reports a cost breakdown.
- The screens support `--transport fhops-marine`; legacy CLEWs/FFCM remains the
  default published comparison.
- The FHOPS case is a representative synthetic fixture, not a GNN terminal
  inventory or a current quote.
- Do not treat the FHOPS Phase I result as a full Phase II/III schedule.
- The sustainable gate must keep transport labelled diagnostic until actual
  terminals, distances, and carrier/terminal quotes are available.

See `notes/reference/fhops-marine-transport.md`.
