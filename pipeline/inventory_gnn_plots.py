#!/usr/bin/env python3
"""Inventory public ground-plot sites inside the GNN AOI."""

from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd


def _inside_sites(header: Path, aoi: gpd.GeoDataFrame) -> pd.DataFrame:
    frame = pd.read_csv(header).dropna(subset=["BC_ALBERS_X", "BC_ALBERS_Y"])
    points = gpd.GeoDataFrame(
        frame,
        geometry=gpd.points_from_xy(frame["BC_ALBERS_X"], frame["BC_ALBERS_Y"]),
        crs="EPSG:3005",
    )
    inside = gpd.sjoin(points, aoi[["geometry"]], predicate="within", how="inner")
    return pd.DataFrame(
        {
            "site_identifier": inside["SITE_IDENTIFIER"].astype(str),
            "sample_type": inside["SAMPLE_ESTABLISHMENT_TYPE"].astype(str),
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aoi", type=Path, required=True)
    parser.add_argument("--psp-header", type=Path, required=True)
    parser.add_argument("--nonpsp-north-header", type=Path, required=True)
    parser.add_argument("--nonpsp-south-header", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    aoi = gpd.read_file(args.aoi).to_crs(3005)
    sources = {
        "PSP": args.psp_header,
        "non-PSP GBR North": args.nonpsp_north_header,
        "non-PSP GBR South": args.nonpsp_south_header,
    }
    frames = []
    for source, header in sources.items():
        frame = _inside_sites(header, aoi)
        frame["source"] = source
        frames.append(frame)
    combined = pd.concat(frames, ignore_index=True)
    inventory = (
        combined.groupby(["source", "sample_type"], as_index=False)
        .agg(sites=("site_identifier", "nunique"))
        .sort_values(["source", "sample_type"])
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    inventory.to_csv(args.out, index=False)
    print(inventory.to_string(index=False))
    print(f"total sites: {combined['site_identifier'].nunique()}")


if __name__ == "__main__":
    main()
