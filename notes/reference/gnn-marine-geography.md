# GNN marine geography and terminal data

Date: 2026-10-25
Status: public-source audit; public route identified, current terminal and rates unconfirmed.

## Why this note exists

The GNN AOI is on northern Vancouver Island. The FHOPS marine fixture used in
P4 is a synthetic Sunshine Coast -> Howe Sound case. Those are different
geographies. The FHOPS adapter is therefore a cost-path/API test, not a GNN
transport estimate.

## GNN AOI

Source: `data/source/aoi/gnn_full.gpkg`, computed in EPSG:4326.

- Centroid: approximately **51.185 N, -127.408 W**.
- Bounds: approximately 50.747-51.555 N, -128.396 to -126.468 W.
- Area: 682,155.05 ha inside the TSA 46/47 union.
- The AOI includes northern Vancouver Island, Johnstone Strait, and adjacent
  mainland inlets.

The proposed-boundary caveat remains: this is not a legal title or treaty
boundary.

## FHOPS fixture

Source: `config/cost_revenue/transport/fhops_marine/scenario.yaml`, derived from
`UBC-FRESH/fhops` `examples/hauling_marine/` at `f788d7a6`.

- Origin: synthetic Sunshine Coast pickup; Sechelt terminal.
- Destination: synthetic Howe Sound terminal and sort yard.
- Water leg: **80 km**.
- Drayage legs: **28 km** pickup and **24 km** delivery.
- Barge: 3,000 m3; 505-minute round trip including handling.
- All route, distance, terminal, and rate values are fixture assumptions.

This is a valid test of FHOPS marine machinery. It is not a GNN route, terminal,
or rate deck.

## Candidate public infrastructure

These are **candidate public infrastructure points**, not confirmed GNN
log-barge terminals. Public harbour or industrial use does not establish log
handling, ownership, capacity, seasonality, or rates.

| Candidate | Approximate WGS84 | Public evidence | What it does not prove |
| --- | --- | --- | --- |
| Port Hardy | 50.725 N, -127.499 W | District of Port Hardy forestry and marine business listings; public reporting of a barge dock at Canadian Fishing Company | A log-barge terminal, GNN use, capacity, or rates |
| Port McNeill | 50.590 N, -127.084 W | Port McNeill harbour report documents a barge ramp/loading dock; BC Ferries terminal | Log-sort use, ownership, or rates |
| Beaver Cove | 50.535 N, -126.857 W | Atli Chip barge shipments to coastal pulp mills; 2026 closure reporting | Log-barge use, current operation, or GNN use |
| Coal Harbour | 50.601 N, -127.583 W | Public harbour/community location; no log-terminal source found | Any log-barge terminal |
| Alert Bay | 50.584 N, -126.930 W | Public harbour/ferry location; no log-terminal source found | Any log-barge terminal |
| Port Alice | 50.383 N, -127.433 W | Public harbour/community location; no log-terminal source found | Any log-barge terminal |

Sources:

- District of Port Hardy forestry: https://porthardy.ca/business/industries/forestry
- District of Port Hardy marine/charter listings: https://porthardy.ca/business/business-license-listing/tourism-fishing-and-marine-charters
- Port Hardy barge-dock report: https://www.timescolonist.com/local-news/barge-sinks-at-port-hardy-dock-9896383
- Port McNeill harbour development report: https://islandcoastaltrust.ca/wp-content/uploads/2014/01/Port-McNeill-Harbour-Development-Project-Final-Report.pdf
- Beaver Cove chip-barge report: https://pqbnews.com/2021/05/27/first-barge-of-logging-waste-chips-successfully-loaded-in-new-first-nations-partnership/
- Beaver Cove closure report: https://www.timescolonist.com/business/first-nations-owned-vancouver-island-wood-chip-plant-set-to-close-in-march-11776159
- Holbrook Dyson Logging (northern Vancouver Island; dry-land sorting and log booming): https://hdlogging.com/
- NorthPac Forestry Group (log shipping by boom/barge, not GNN-specific): https://northpacforestry.com/transportation-shipping

## Distance mismatch check

Approximate great-circle distances from candidate origins to potential southern
destinations, in kilometres. These are **not** road or water-route distances and
are not cost inputs.

| Origin | Vancouver | Howe Sound | Powell River | Nanaimo |
| --- | ---: | ---: | ---: | ---: |
| Port Hardy | 352 | 334 | 230 | 308 |
| Port McNeill | 319 | 301 | 197 | 275 |
| Beaver Cove | 302 | 284 | 180 | 259 |
| Coal Harbour | 351 | 334 | 231 | 306 |
| Alert Bay | 309 | 291 | 187 | 266 |
| Port Alice | 333 | 316 | 213 | 285 |

The FHOPS fixture's 80 km water leg is materially shorter than any of these
straight-line distances. Using its solved cost as a GNN transport estimate would
understate the water leg and misstate the geography.

## Public route evidence

Seaspan's public log-barging description identifies a common route from
**Quatsino Sound to Ladysmith Harbour**, around Vancouver Island via Johnstone
Strait, Queen Charlotte Strait, Cape Scott, and the west coast. The same article
describes dumping logs at Ladysmith for sorting by species and grade.

Historical TFL 6 annual reports identify the **Quatsino Dryland Log Sort** as a
central facility on Quatsino Sound, name Seaspan International as the barging
contractor and Pacific Towing as the towing contractor, and list southern
processors including Ladysmith, Duke Point, Cowichan Bay, Squamish, and Nanaimo.

These are public route and historical terminal facts. They do not confirm the
current status, capacity, ownership, or rates of either end.

Source: https://www.seaspan.com/stories/log-barging-101/

## Public-route proxy

P6.1 adds a diagnostic proxy using the public Quatsino -> Ladysmith route and
explicit assumptions for capacity, rates, road legs, and terminal handling. It
is labelled `public_route_assumption_rates` and is not the published base.

The proxy is documented in `notes/reference/gnn-marine-proxy.md`.

## FHOPS multi-day limitation

FHOPS Phase I limits a barge fleet to one day of working minutes. The Quatsino
-> Ladysmith barge cycle is about 3,955 minutes, so a single barge is infeasible
and adding extra barges would fake the fleet. The proxy therefore uses an
analytical calculation from the validated FHOPS marine lane contract, not a
solved Phase I plan. Tracked upstream at `UBC-FRESH/fhops#196`.

## Missing data

A GNN-specific FHOPS scenario needs all of the following:

- confirmed origin log-barge terminal(s) and operator;
- confirmed destination sort yard, mill, or export terminal;
- road route and distance from candidate blocks/landings to each origin terminal;
- water route and distance, including any intermediate stops;
- barge type, capacity, load/unload times, and utilisation;
- current carrier rates, fuel/operating charges, and terminal handling charges;
- seasonality, tide/weather constraints, and availability; and
- evidence that the selected destination actually accepts the GNN sort mix.

Current carrier and terminal quotes are not public. They must come from the
maintainer, a carrier, or a terminal operator, and must be dated and cited.

## Decision

Do not switch the published transport base or claim a GNN barge cost until the
missing current data is supplied. The P6 proxy is a diagnostic scenario, not a
quote. Keep the legacy CLEWs/FFCM path as the published comparison and the P4
FHOPS fixture as an API cost-path test.
