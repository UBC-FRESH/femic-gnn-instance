GNN AOI
=======

Boundary source
---------------

- Service: ``https://maps.gov.bc.ca/arcgis/rest/services/whse/bcgw_pub_reg_legal_and_admin_boundaries/MapServer/1``
- Layer: First Nation Statement of Intent Boundaries BC
- Feature: ``Gwa'Sala-'Nakwaxda'xw Nation (proposed)``
- Query: ``NAME LIKE '%Gwa%'``, EPSG:3005, GeoJSON

This is the proposed Statement of Intent boundary. It is not a final treaty
boundary or a legal title determination. The BC Treaty Commission states that
the SOI map is under review. Confirm with GNN before public or operational use.

Area
----

.. list-table::
   :header-rows: 1
   :widths: 35 35

   * - Intersection
     - Area
   * - GNN SOI total
     - 703,417.95 ha
   * - GNN AOI inside TSA 46/47
     - 682,155.05 ha
   * - TSA 46 overlap
     - 292,930.08 ha
   * - TSA 47 overlap
     - 389,226.32 ha
   * - Outside both TSAs
     - 21,262.91 ha

Files: ``data/source/aoi/gnn_soi.gpkg``, ``gnn_full.gpkg``, and
``gnn_aoi.json``.
