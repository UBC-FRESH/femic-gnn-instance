# Local price deck validation

Date: 2026-10-25
Status: partial validation; raw values not redistributed.

## Source

BC Ministry of Forests, Timber Pricing Branch, Coast Log Market Reports,
Vancouver Log Market, three months ending 2026-01-31. Old-growth and second-growth
PDFs were downloaded to a local scratch directory.

## What was checked

The local deck `runtime/p3/price_deck_reviewed.csv` was manually checked against
the PDFs for:

- second-growth cedar: D/H/I/J/K/L/M/U/X/Y
- second-growth fir: C/H/I/J/U/X/Y
- second-growth Hembal: H/I/J/U/X/Y
- second-growth spruce: H/I/J/U/X/Y
- old-growth Hembal, cedar, fir, spruce, and cypress for range/proxy use

The second-growth deck is the preferred basis for managed stands. Old-growth
values are used only for the cypress proxy and for a price range.

Local deck SHA-256:

```text
ca54404ac903d14bb541d528ec8fd36efa27023969b9ab57c98da99b2561b680  runtime/p3/price_deck_reviewed.csv
```

The deck is kept under `runtime/p3/` and is not committed because the BC report
restricts redistribution.

## What is not checked or missing

- Second-growth cypress is not available in the extracted table; the old-growth
  cypress row is a proxy, not a second-growth price.
- The deck is a market sales table, not a block-level sort recovery model.
- Price date is 2026-01-31; it is not a forward price.
- No delivered-price adjustment or buyer-specific netback.
- No carrier/terminal quote.

## Consequence

A net revenue calculation using this deck is a **screening range**, not a
calibrated result. The cypress proxy and provisional recovery matrix are the
largest remaining price-side uncertainties.
