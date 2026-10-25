#!/usr/bin/env python3
"""Screen net revenue ranges for cable/heli blocks.

This is a range-based screening exercise, not a calibrated net revenue result.
It uses a local reviewed price deck, the provisional recovery matrix, legacy
CLEWs transport rates, and one-machine cable/heli screening costs.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

# Legacy CLEWs/FFCM diagnostic transport, 100 km truck + 100 km barge + transload.
TRANSPORT_BASE = 10.961
TRANSPORT_LOW = 7.77
TRANSPORT_HIGH = 14.54
CABLE_LOW = 17.61
CABLE_HIGH = 37.50
HELI_LOW = 59.66
HELI_HIGH = 87.09
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


def _price_range(prices: pd.DataFrame, species: str, product: str) -> tuple[float, float, float]:
    grades = GRADES[product].get(species, [])
    values = prices[(prices.species_group == species) & (prices.grade.isin(grades))][
        "price_per_m3_cad"
    ]
    if values.empty:
        return (0.0, 0.0, 0.0)
    return (float(values.min()), float(values.mean()), float(values.max()))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument("--prices", type=Path, required=True)
    parser.add_argument("--recovery", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    sample = pd.read_csv(args.sample)
    prices = pd.read_csv(args.prices)
    recovery = pd.read_csv(args.recovery)
    shares = {
        group: dict(zip(recovery[recovery.species_group == group].product_group, recovery[recovery.species_group == group].base_share))
        for group in recovery.species_group.unique()
    }
    low_shares = {
        group: dict(zip(recovery[recovery.species_group == group].product_group, recovery[recovery.species_group == group].low_share))
        for group in recovery.species_group.unique()
    }
    high_shares = {
        group: dict(zip(recovery[recovery.species_group == group].product_group, recovery[recovery.species_group == group].high_share))
        for group in recovery.species_group.unique()
    }

    records: list[dict[str, object]] = []
    for row in sample.itertuples(index=False):
        if row.operability == "ground":
            harvest_low = harvest_high = None
            net_low = net_high = None
            cost_status = "ground_full_system_pending"
        else:
            harvest_low = CABLE_LOW if row.operability == "cable" else HELI_LOW
            harvest_high = CABLE_HIGH if row.operability == "cable" else HELI_HIGH
            cost_status = "screening_only"
        revenue_low = revenue_base = revenue_high = 0.0
        for species in ("hembal", "cedar", "cypress", "fir", "spruce"):
            share = float(getattr(row, f"{species}_share_pct", 0.0) or 0.0) / 100.0
            if share <= 0:
                continue
            species_label = species.capitalize()
            for product in ("high", "sawlog", "utility", "pulp"):
                pmin, pmean, pmax = _price_range(prices, species_label, product)
                revenue_low += row.volume_m3 * share * low_shares.get(species_label, {}).get(product, 0.0) * pmin
                revenue_base += row.volume_m3 * share * shares.get(species_label, {}).get(product, 0.0) * pmean
                revenue_high += row.volume_m3 * share * high_shares.get(species_label, {}).get(product, 0.0) * pmax
        if harvest_low is not None and harvest_high is not None:
            net_low = revenue_low - harvest_high * row.volume_m3 - TRANSPORT_HIGH * row.volume_m3
            net_high = revenue_high - harvest_low * row.volume_m3 - TRANSPORT_LOW * row.volume_m3
        records.append(
            {
                "block_id": row.block_id,
                "volume_m3": row.volume_m3,
                "operability": row.operability,
                "dominant_species_group": row.dominant_species_group,
                "revenue_low_cad": round(revenue_low, 0),
                "revenue_base_cad": round(revenue_base, 0),
                "revenue_high_cad": round(revenue_high, 0),
                "harvest_low_cad": None if harvest_low is None else round(harvest_low * row.volume_m3, 0),
                "harvest_high_cad": None if harvest_high is None else round(harvest_high * row.volume_m3, 0),
                "transport_low_cad": round(TRANSPORT_LOW * row.volume_m3, 0),
                "transport_high_cad": round(TRANSPORT_HIGH * row.volume_m3, 0),
                "net_low_cad": None if net_low is None else round(net_low, 0),
                "net_high_cad": None if net_high is None else round(net_high, 0),
                "cost_status": cost_status,
                "data_status": "screening_only",
            }
        )
    frame = pd.DataFrame.from_records(records)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.out, index=False)
    priced = frame[frame.cost_status == "screening_only"]
    print(f"priced blocks={len(priced)} volume={priced.volume_m3.sum():.0f} m3")
    if not priced.empty:
        print(
            f"net range: {priced.net_low_cad.sum()/1e6:.2f}M to "
            f"{priced.net_high_cad.sum()/1e6:.2f}M CAD"
        )
        print(
            "share of priced volume unprofitable even in best case: "
            f"{100*priced.loc[priced.net_high_cad < 0, 'volume_m3'].sum()/priced.volume_m3.sum():.1f}%"
        )
    print(frame.groupby(["operability", "cost_status"]).volume_m3.sum().to_string())


if __name__ == "__main__":
    main()
