# GNN public-route marine proxy

Date: 2026-10-25
Status: diagnostic proxy; public route, assumed rates and capacity.

## Route evidence

Seaspan's public log-barging description states that its log barges commonly
deliver logs from **Quatsino Sound to Ladysmith Harbour**, transiting Johnstone
Strait, Queen Charlotte Strait, Cape Scott, and the west coast of Vancouver
Island before rounding the south end and entering Ladysmith Harbour. The same
article describes the barge dumping logs in Ladysmith for sorting by species and
grade.

Sources:

- Seaspan, Log Barging 101 (2023-05-12):
  https://www.seaspan.com/stories/log-barging-101/
- TFL 6 Annual Report 1999, transportation and processing sections:
  https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/timber-tenures/tree-farm-licence/annual-reports/tfl-06-annual-reports-1999.pdf
- TFL 6 Annual Report 2000:
  https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/timber-tenures/tree-farm-licence/annual-reports/tfl-06-annual-reports-2000.pdf

The TFL 6 reports identify the **Quatsino Dryland Log Sort** as a central
facility on Quatsino Sound, state that Seaspan International held the barging
contract and Pacific Towing the towing contract, and list southern processing
facilities including Ladysmith, Duke Point, Cowichan Bay, Squamish, and Nanaimo.

## Proxy scenario

Location: `config/cost_revenue/transport/fhops_marine_quatsino_ladysmith/`.
Config: `config/cost_revenue/transport/fhops_marine_quatsino_ladysmith.yaml`.

The scenario models:

- one aggregate block at the Quatsino Sound load point;
- road drayage to the origin terminal;
- a 589 km approximate water leg, 1,910 minutes one way at 10 knots;
- terminal handling at Quatsino and Ladysmith;
- road delivery to a Ladysmith sort yard; and
- a 10,000 m3 proxy barge.

Approximate route waypoints are Quatsino Sound mouth -> Cape Scott -> west coast
-> Barkley Sound -> Juan de Fuca -> Victoria -> Ladysmith. This is a distance
check, not a navigation route.

## Assumed values

Every value below is an assumption, not a current quote:

| Item | Proxy value | Basis |
| --- | ---: | --- |
| Barge capacity | 10,000 m3 | FHOPS proxy assumption; not a confirmed vessel |
| Barge fixed cost | 1,500 CAD/day | FHOPS fixture proxy |
| Barge variable cost | 5 CAD/min | FHOPS fixture proxy |
| Truck capacity | 45 m3 | FHOPS fixture proxy |
| Truck fixed cost | 120 CAD/day | FHOPS fixture proxy |
| Truck variable cost | 1.20 CAD/min | FHOPS fixture proxy |
| Road block-to-Quatsino | 50 km, 60 min | Proxy assumption |
| Road Ladysmith-to-yard | 10 km, 20 min | Proxy assumption |
| Origin handling | 150 CAD/trip, 30 min | Proxy assumption |
| Destination handling | 180 CAD/trip, 45 min | Proxy assumption |
| Water leg | 589 km, 1,910 min one way | Approximate waypoint distance at 10 knots |
| Horizon | 8 days | One multi-day voyage |

The data status is `public_route_assumption_rates`.

## Results

Run:

```bash
python pipeline/fhops_marine_transport.py \
  --config config/cost_revenue/transport/fhops_marine_quatsino_ladysmith.yaml \
  --out runtime/p6/quatsino_ladysmith_proxy.csv
```

| Case | Volume | Utilization | CAD/m3 |
| --- | ---: | ---: | ---: |
| Low cost | 10,000 m3 | 100% | 8.125 |
| Base | 7,500 m3 | 75% | 9.203 |
| High cost | 5,000 m3 | 50% | 11.360 |

The P4 API fixture was 5.642/6.100/7.097 CAD/m3. The public-route proxy is
higher because the water leg is much longer and the route cycle spans days.

## FHOPS limitation

FHOPS Phase I cannot solve this voyage directly. Its barge fleet constraint
allows `regular_minutes` (510) of barge work per day. The Quatsino -> Ladysmith
barge cycle is 3,955 minutes, so a single barge is infeasible and adding eight
barges would be a fake fleet.

The adapter therefore uses an **analytical proxy** built from the validated
FHOPS marine lane contract:

- barge trips = ceil(volume / barge capacity);
- barge variable cost from the lane's cycle and per-minute rate;
- drayage from the lane's pickup/delivery cost per m3;
- terminal handling from the lane's per-trip costs;
- barge fixed cost for the number of days the cycle spans; and
- truck fixed cost for a feasible peak drayage fleet.

It is not a solved Phase I plan. Tracked upstream at `UBC-FRESH/fhops#196`.

## Limits

- The terminal is not confirmed to be currently open or accepting GNN volume.
- The barge is not a confirmed vessel or capacity.
- Rates are FHOPS fixture proxies, not current carrier or terminal quotes.
- The route is a waypoint approximation, not a navigation survey.
- Road distances to the load point are assumptions.
- The proxy is not the published transport base and must not be used for a
  sustainable or profitable label.
- The sustainable gate must reject `public_route_assumption_rates`.
