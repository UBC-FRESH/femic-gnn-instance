Economic screening
==================

Status: **diagnostic screening**, not a sustainable or financially calibrated
result. The model release remains volume-only.

Coverage
--------

The screen covers **52,984.43 ha of derived THLB** at the VRI checkpoint-polygon
level.

Result
------

Positive net unit revenue:

.. list-table::
   :header-rows: 1
   :widths: 38 30 20

   * - Case
     - Positive THLB
     - Share
   * - Low price/recovery, high transport
     - 46,612.65 ha
     - **88.0%**
   * - Base
     - 50,602.51 ha
     - **95.5%**
   * - High price/recovery, low transport
     - 51,285.26 ha
     - **96.8%**

By operability (base):

.. list-table::
   :header-rows: 1
   :widths: 24 20 18 22

   * - Class
     - THLB
     - Share
     - Positive share
   * - Ground
     - 29,051.3 ha
     - 54.8%
     - 96.6%
   * - Cable
     - 12,334.6 ha
     - 23.3%
     - 97.4%
   * - Heli candidate
     - 11,598.5 ha
     - 21.9%
     - 90.8%

Sensitivity: 87.8% positive at 2x harvest cost; 92.3% at 30 CAD/m3 transport.

Method and limits
-----------------

- Coarse DEM (zoom 11), centroid slope; not LiDAR or a block zonal mean.
- Class-average full-system costs from the FHOPS registry:
  ground 15.37, cable 17.77, helicopter 78.13 CAD/m3.
- Legacy CLEWs/FFCM transport: 10.961 CAD/m3 at 100 km truck + 100 km barge +
  transload; not a current quote.
- Local reviewed BC log price deck for 2026-01-31; raw prices are not
  redistributed.
- Provisional recovery matrix; reject/waste 2/5/10%.
- No road/landing construction, overhead, profit, or silviculture cost.

FHOPS marine API test (not GNN geography)
-----------------------------------------

FHOPS marine/barge hauling is available from upstream issue `#187` (merged as
`f788d7a6`), and the instance has an opt-in adapter:

```bash
python pipeline/fhops_marine_transport.py --out runtime/p4/fhops_marine_cost.csv
python pipeline/full_thlb_screening.py ... --transport fhops-marine
```

The only marine fixture is a synthetic **Sunshine Coast -> Howe Sound** case.
The GNN AOI is **northern Vancouver Island**. The fixture is an API/cost-path
test, not a GNN transport estimate, terminal inventory, or current quote. There
is no GNN-specific terminal, route, distance, or carrier-rate dataset yet. The
published screen remains the legacy CLEWs/FFCM result above.

See `notes/reference/gnn-marine-geography.md
<https://github.com/UBC-FRESH/femic-gnn-instance/blob/main/notes/reference/gnn-marine-geography.md>`_.

A separate internal proxy uses the public Quatsino Sound -> Ladysmith Harbour
route and runs as a solved FHOPS Phase I case. It is diagnostic only, not used in
this screen, and documented in
`notes/reference/gnn-marine-proxy.md
<https://github.com/UBC-FRESH/femic-gnn-instance/blob/main/notes/reference/gnn-marine-proxy.md>`_.

This is a screening estimate. It does not justify a sustainable or profitable
label, and it does not replace a reviewed GNN netdown, current carrier quotes,
or observed grade/sort recovery.

See `notes/reference/fhops-marine-transport.md
<https://github.com/UBC-FRESH/femic-gnn-instance/blob/main/notes/reference/fhops-marine-transport.md>`_.

Notes: `notes/reference/full-thlb-screening.md` and
`notes/reference/net-revenue-screening.md`.
