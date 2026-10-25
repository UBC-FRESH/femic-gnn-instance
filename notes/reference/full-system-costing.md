# Full harvest-system screening costs

Date: 2026-10-25
Status: registry-based screening; not a solved FHOPS shift schedule.

## Systems

Using the FHOPS pre-configured harvest-system registry:

- `ground_fb_skid`: feller-buncher -> grapple skidder -> processor -> loader
- `cable_running_sr54`: feller-buncher -> grapple yarder (SR54) -> processor -> loader
- `helicopter`: hand faller -> helicopter longline (Bell 214B) -> processor -> loader

Representative blocks:

| Block | System | Volume | Slope |
| --- | --- | ---: | ---: |
| 14924 | ground_fb_skid | 9,050 m3 | 3.48% |
| 14811 | cable_running_sr54 | 8,941 m3 | 39.12% |
| 5620 | helicopter | 3,569 m3 | 78.01% |

## Method

For each system:

1. Read the role chain from the FHOPS registry.
2. Estimate the primary-transport productivity with the FHOPS model and
   system overrides.
3. Sum machine rates / utilisation for all roles, using one machine per role.
4. Divide by the primary-transport productivity (bottleneck approximation).
5. Add hand-falling (TN98 cedar, 1.11 CAD/m3) where the system requires it.
6. Add move-in cost / block volume.

## Result

| Block | System | System cost |
| --- | --- | ---: |
| 14924 | ground | **15.37 CAD/m3** |
| 14811 | cable | **17.77 CAD/m3** |
| 5620 | helicopter | **78.13 CAD/m3** |

Adding the legacy 100 km truck + 100 km barge + transload allowance
(10.961 CAD/m3) gives roughly:

- ground: 26.33 CAD/m3
- cable: 28.73 CAD/m3
- helicopter: 89.09 CAD/m3

These are screening costs before landing/road construction, overhead, profit,
and any current carrier quote.

## Caveats

- The bottleneck approximation is not a solved FHOPS shift schedule. It ignores
  queueing, shift calendars, landing capacity, and machine balance.
- `cable_running_sr54` uses mechanised felling; the 39% slope block may be at or
  beyond safe feller-buncher limits. A hand-felled cable system may be required.
- The helicopter hand-fall cost is a TN98 cedar estimate.
- Machine rates are 2024 CAD reference rates, not contractor quotes.
- No road/landing construction, overhead, or profit.
- No current barge/truck/terminal quotes.

File: `config/cost_revenue/samples/full_system_costs.csv`
