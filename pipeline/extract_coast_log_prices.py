#!/usr/bin/env python3
"""Extract the BC Coast Log Market Report species/grade AMV table to a local CSV.

The BC report restricts redistribution. Write the output to a gitignored path;
do not commit the extracted price values.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pdfplumber
import pandas as pd

SPECIES = (
    "Alder",
    "Birch",
    "Cedar",
    "Cottonwood",
    "Cypress",
    "Fir",
    "Hembal",
    "Maple",
    "Pine",
    "Spruce",
)
NUMBER = re.compile(r"^-?\d+(?:\.\d+)?$")


def _header_positions(words: list[dict[str, object]]) -> dict[str, float]:
    positions: dict[str, float] = {}
    for word in words:
        text = str(word["text"]).strip()
        if text in SPECIES:
            top = float(word["top"])
            if 195 <= top <= 215:
                positions[text] = float(word["x0"])
    return positions


def _nearest_species(x: float, headers: dict[str, float]) -> str | None:
    if not headers:
        return None
    species, distance = min(
        ((name, abs(x - position)) for name, position in headers.items()),
        key=lambda item: item[1],
    )
    return species if distance <= 65 else None


def _extract_page(page: pdfplumber.page.Page) -> list[dict[str, object]]:
    words = page.extract_words()
    headers = _header_positions(words)
    if not headers:
        raise ValueError("species header row not found")
    grade_rows: list[tuple[str, float]] = []
    for word in words:
        text = str(word["text"]).strip()
        if len(text) == 1 and text.isalpha() and float(word["x0"]) < 120:
            grade_rows.append((text, float(word["top"])))
    records: list[dict[str, object]] = []
    for grade, top in grade_rows:
        row_values = [
            word
            for word in words
            if NUMBER.match(str(word["text"]).strip())
            and float(word["x0"]) > 400
            and top - 2 <= float(word["top"]) <= top + 12
        ]
        for word in row_values:
            value = float(str(word["text"]).replace(",", ""))
            species = _nearest_species(float(word["x0"]), headers)
            if species is None:
                continue
            records.append(
                {
                    "species": species,
                    "grade": grade,
                    "price_per_m3_cad": value,
                }
            )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--sale-type", required=True)
    parser.add_argument("--period", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--retrieved", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    records: list[dict[str, object]] = []
    with pdfplumber.open(args.pdf) as pdf:
        for page in pdf.pages:
            records.extend(_extract_page(page))
    frame = pd.DataFrame.from_records(records)
    frame["sale_type"] = args.sale_type
    frame["period"] = args.period
    frame["source_url"] = args.source_url
    frame["retrieved"] = args.retrieved
    frame = frame.drop_duplicates(["species", "grade"])
    frame = frame.sort_values(["species", "grade"])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.out, index=False)
    print(f"wrote {len(frame)} species/grade prices to {args.out}")


if __name__ == "__main__":
    main()
