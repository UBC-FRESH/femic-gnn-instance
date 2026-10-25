#!/usr/bin/env python3
"""Full-THLB net revenue screening at the VRI checkpoint-polygon level.

Coarse-DEM operability, full-system class costs, local reviewed prices,
provisional recovery, and legacy transport. This is a screening run, not a
calibrated net revenue model.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer

from sample_block_terrain import _mosaic, _slope_percent

COSTS = {"ground": 15.37, "cable": 17.77, "heli_candidate": 78.13}
TRANSPORT = {"low": 7.77, "base": 10.961, "high": 14.54}
REJECT = {"low": 0.02, "base": 0.05, "high": 0.10}
GRADES = {
    "high": {
        "Hembal": ["D", "F"],
        "Cedar": ["D", "F"],
        "Fir": ["B", "C", "F"],
        "Spruce": ["D", "F"],
        "Cypress": ["D", "F"],
    },
    "sawlog": {
        "Hembal": ["H", "I", "J"],
        "Cedar": ["H", "I", "J"],
        "Fir": ["H", "I", "J"],
        "Spruce": ["H", "I", "J"],
        "Cypress": ["H", "I", "J"],
    },
    "utility": {
        "Hembal": ["U", "X"],
        "Cedar": ["U", "X"],
        "Fir": ["U", "X"],
        "Spruce": ["U", "X"],
        "Cypress": ["U", "X"],
    },
    "pulp": {
        "Hembal": ["Y"],
        "Cedar": ["Y"],
        "Fir": ["Y"],
        "Spruce": ["Y"],
        "Cypress": ["Y"],
    },
}
SPECIES = {
    "H": "Hembal",
    "BA": "Hembal",
    "HM": "Hembal",
    "CW": "Cedar",
    "YC": "Cypress",
    "FD": "Fir",
    "S": "Spruce",
    "SX": "Spruce",
    "SE": "Spruce",
}


def _prices(prices: pd.DataFrame, species: str, product: str, age: float) -> tuple[float, float, float]:
    grades = GRADES[product].get(species, [])
    sale = "old_growth" if age >= 141 or species == "Cypress" else "second_growth"
    values = prices[
        (prices.species_group == species)
        & (prices.sale_type == sale)
        & (prices.grade.isin(grades))
    ]["price_per_m3_cad"]
    if values.empty:
        return (0.0, 0.0, 0.0)
    return (float(values.min()), float(values.mean()), float(values.max()))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--aoi", type=Path, required=True)
    parser.add_argument("--prices", type=Path, required=True)
    parser.add_argument("--recovery", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--zoom", type=int, default=11)
    args = parser.parse_args()

    import geopandas as gpd

    aoi = gpd.read_file(args.aoi).to_crs(3005)
    min_x, min_y, max_x, max_y = aoi.total_bounds
    to_wgs = Transformer.from_crs(3005, 4326, always_xy=True)
    corners = [to_wgs.transform(min_x, min_y), to_wgs.transform(max_x, max_y)]
    lons = [p[0] for p in corners]
    lats = [p[1] for p in corners]
    bbox = (min(lons), min(lats), max(lons), max(lats))
    elevation, x0, y0, _, _ = _mosaic(bbox, args.zoom)
    slope = _slope_percent(elevation, zoom=args.zoom, origin_x=x0, origin_y=y0)

    checkpoint = pd.read_feather(args.checkpoint)
    checkpoint = checkpoint[
        pd.to_numeric(checkpoint["thlb_raw_calibrated"], errors="coerce").fillna(0) > 0
    ].copy()
    area_ha = pd.to_numeric(checkpoint["FEATURE_AREA_SQM"], errors="coerce") / 10000.0
    thlb_ha = area_ha * pd.to_numeric(checkpoint["thlb_raw_calibrated"], errors="coerce") / 100.0
    volume_ha = pd.to_numeric(checkpoint["LIVE_STAND_VOLUME_125"], errors="coerce").fillna(0)
    volume = volume_ha * thlb_ha
    age = pd.to_numeric(checkpoint["PROJ_AGE_1"], errors="coerce").fillna(0)
    x = pd.to_numeric(checkpoint["LABEL_CENTRE_X"], errors="coerce")
    y = pd.to_numeric(checkpoint["LABEL_CENTRE_Y"], errors="coerce")
    lon, lat = to_wgs.transform(x.to_numpy(), y.to_numpy())
    count = 2**args.zoom
    col = np.floor((lon + 180.0) / 360.0 * count * 256.0 - x0 * 256.0).astype(int)
    row = np.floor(
        (1.0 - np.arcsinh(np.tan(np.radians(lat))) / math.pi) / 2.0 * count * 256.0
        - y0 * 256.0
    ).astype(int)
    valid = (col >= 0) & (col < slope.shape[1]) & (row >= 0) & (row < slope.shape[0])
    point_slope = np.full(len(checkpoint), np.nan)
    point_slope[valid] = slope[row[valid], col[valid]]

    prices = pd.read_csv(args.prices)
    recovery = pd.read_csv(args.recovery)
    base_shares = {
        group: dict(zip(recovery[recovery.species_group == group].product_group,
                        recovery[recovery.species_group == group].base_share))
        for group in recovery.species_group.unique()
    }
    low_shares = {
        group: dict(zip(recovery[recovery.species_group == group].product_group,
                        recovery[recovery.species_group == group].low_share))
        for group in recovery.species_group.unique()
    }
    high_shares = {
        group: dict(zip(recovery[recovery.species_group == group].product_group,
                        recovery[recovery.species_group == group].high_share))
        for group in recovery.species_group.unique()
    }

    # Species shares by polygon.
    shares = np.zeros((len(checkpoint), len(set(SPECIES.values()))))
    species_names = sorted(set(SPECIES.values()))
    for idx in range(1, 7):
        code = checkpoint[f"SPECIES_CD_{idx}"].astype(str).str.upper().str.strip()
        pct = pd.to_numeric(checkpoint[f"SPECIES_PCT_{idx}"], errors="coerce").fillna(0) / 100.0
        for j, name in enumerate(species_names):
            shares[:, j] += np.where(code.map(SPECIES) == name, pct, 0.0)

    price_maps: dict[tuple[str, str, str], tuple[float, float, float]] = {}
    for sale in ("old_growth", "second_growth"):
        for name in species_names:
            for product in ("high", "sawlog", "utility", "pulp"):
                grades = GRADES[product].get(name, [])
                values = prices[
                    (prices.species_group == name)
                    & (prices.sale_type == sale)
                    & (prices.grade.isin(grades))
                ]["price_per_m3_cad"]
                if values.empty and product == "high":
                    values = prices[
                        (prices.species_group == name)
                        & (prices.sale_type == sale)
                        & (prices.grade.isin(GRADES["sawlog"].get(name, [])))
                    ]["price_per_m3_cad"]
                price_maps[(sale, name, product)] = (
                    (float(values.min()), float(values.mean()), float(values.max()))
                    if not values.empty
                    else (0.0, 0.0, 0.0)
                )

    revenue = {case: np.zeros(len(checkpoint)) for case in ("low", "base", "high")}
    age_values = age.to_numpy(dtype=float)
    for j, name in enumerate(species_names):
        old = (age_values >= 141) | (name == "Cypress")
        for product in ("high", "sawlog", "utility", "pulp"):
            for case, share_map, price_index in (
                ("low", low_shares, 0),
                ("base", base_shares, 1),
                ("high", high_shares, 2),
            ):
                p_old = price_maps[("old_growth", name, product)][price_index]
                p_second = price_maps[("second_growth", name, product)][price_index]
                price = np.where(old, p_old, p_second)
                share = share_map.get(name, {}).get(product, 0.0)
                revenue[case] += volume.to_numpy() * shares[:, j] * share * price

    operability = np.where(
        point_slope < 35, "ground",
        np.where(point_slope < 50, "cable", "heli_candidate"),
    )
    operability = np.where(np.isfinite(point_slope), operability, "unknown")
    cost = np.array([COSTS.get(name, np.nan) for name in operability])
    for case, reject in REJECT.items():
        revenue[case] *= (1.0 - reject)
    result = pd.DataFrame(
        {
            "thlb_ha": thlb_ha,
            "volume_m3": volume,
            "age": age,
            "slope_pct": point_slope,
            "operability": operability,
            "revenue_low_cad": revenue["low"],
            "revenue_base_cad": revenue["base"],
            "revenue_high_cad": revenue["high"],
            "harvest_cost_per_m3": cost,
            "transport_base_per_m3": TRANSPORT["base"],
            "net_base_per_m3": (revenue["base"] / volume.where(volume > 0)) - cost - TRANSPORT["base"],
            "net_high_per_m3": (revenue["high"] / volume.where(volume > 0)) - cost - TRANSPORT["low"],
            "net_low_per_m3": (revenue["low"] / volume.where(volume > 0)) - cost - TRANSPORT["high"],
        }
    )
    result = result[np.isfinite(result["net_base_per_m3"])]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.out, index=False)
    total = result.thlb_ha.sum()
    print(f"THLB covered: {total:.2f} ha")
    for case in ("low", "base", "high"):
        col = f"net_{case}_per_m3"
        positive = result[result[col] > 0].thlb_ha.sum()
        print(f"{case}: positive THLB {positive:.2f} ha = {100*positive/total:.1f}%")
    print(result.groupby("operability").agg(thlb=("thlb_ha", "sum"), net_base=("net_base_per_m3", "mean")).to_string())


if __name__ == "__main__":
    main()
