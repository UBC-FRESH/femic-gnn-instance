# Coastal log price sources and use limits

Date: 2026-10-25
Status: source identified; price deck not published; recovery matrix still missing.

## Primary public source

BC Ministry of Forests, Timber Pricing Branch, **Coast Log Market Reports**:

- https://www2.gov.bc.ca/gov/content/industry/forestry/competitive-forest-industry/timber-pricing/coast-timber-pricing/coast-log-market-reports
- Vancouver Log Market (VLM) average domestic prices, one-month and three-month,
  by species and grade, in CAD/m3.
- Available: old growth and second growth; 2019-2026 historical versions.
- Latest checked: three months ending January 2026.

Useful species columns include cedar, fir, hemlock/balsam, spruce, cypress, and
others. Grades run from B through Y, including H/I/J sawlog and U/X/Y lower
grades. The report also publishes species shares and grade shares for the
reported sales.

## Use limit

The BC report carries a copyright notice that restricts reproduction or
distribution, including posting the tables on the internet, without a licence.
The project may use the reports for private study/research, but the raw tables
should not be committed to this public repository.

Working rule:

- Keep the extracted deck in a gitignored local research path.
- Record the URL, report period, extraction date, and row-level provenance.
- Do not republish the raw BC table in the public docs or release.
- Public outputs may show a documented method, and any aggregate/derived values
  only after a licence/provenance review.
- Do not describe the deck as current without checking the report date.

## Extraction status

A draft extractor is at `pipeline/extract_coast_log_prices.py`. It writes a local
deck under `runtime/p3/`; the values are not committed. The first run produced 47
old-growth and 29 second-growth species/grade prices, but the PDF cell mapping is
not yet validated: merged/centered cells can shift a value to a neighbouring
species column. The draft deck must be checked against the PDF before use.

## Extraction plan

1. Download the old-growth and second-growth three-month PDFs for the chosen
   period.
2. Extract species x grade AMV (`$/m3`) and volume/share into a long table:
   `species`, `grade`, `price_per_m3_cad`, `period`, `source_url`, `retrieved`.
3. Keep the file under `runtime/p3/` or another gitignored path.
4. Treat missing species/grade cells as missing, not zero.
5. Convert species codes to the model's species groups in a separate crosswalk.
6. Freeze the deck for a run; record its hash.

## Still missing

The price deck is only half of the revenue signal. We still need a **grade/sort
recovery matrix** that maps harvested volume by species, age, site, and log
quality into the grades/sorts sold. The BC market report gives the market mix of
reported sales, not the recovery from a GNN block.

Until a documented recovery source or a clearly labelled assumption set exists,
net revenue is not credible. Do not use the market mix as a stand-level
recovery matrix without saying so.

## Candidate recovery sources

- BC coast cruise/sort tables and scaling data.
- Ministry grade-recovery studies for coastal species.
- Mill sort-yard recovery data, if a partner can provide it.
- A documented expert-assumption matrix with low/medium/high cases, clearly
  labelled as an assumption rather than observation.

None of these is in the repository yet.

## Decision

P3.3 remains open. The next step is a **local, dated price deck** plus a
**recovery matrix with provenance**. The public repo will carry the method and
schema, not the restricted raw table.
