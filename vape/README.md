# YV Vape Shop — product list from supplier receipts (Aug–Sep 2026)

Built from six purchase records: Pinnacle Commerce invoices 19583
(12 Aug) and 19825 (1 Sep), a STLTH wholesaler order, a Flavour Beast /
Level X order (26 Aug), order #1373225 (1 Sep), and the order
confirmation behind invoice 19825.

**70 distinct products** across STLTH, Elf Bar, OVNS, Krave, Allo,
Drip'n, Flavour Beast and Level X.

## Files

| File | What |
|------|------|
| `vape-products.csv` | One row per product: pack size, invoice price, excise, unit and carton cost, suggested retail, source |
| `vape-epos-import.csv` | Epos seven-column format, **134 rows** — a single-unit line and a carton line for every product |
| `build_vape_lists.py` | Regenerates both from the receipt data |

## Cost basis: excise is in, HST is out

Vape excise is a real cost of goods and the receipts handle it three
different ways, so every cost here is normalised to **excise-inclusive,
HST-exclusive**:

- Pinnacle and Flavour Beast prices already include excise (Pinnacle
  shows HST only; Flavour Beast prints "federal tax included").
- The STLTH wholesaler order and order #1373225 bill excise as separate
  lines, so it is added back per unit.

The excise model — $1.12 per 2 mL for the first 10 mL, $1.12 per 10 mL
after that, with Ontario's provincial duty equal to the federal — was
checked against every receipt that itemises it and reproduces all three
to the cent: $322.56, $461.44 and $33.60. That check also settled the
pack sizes the receipts do not state (Drip'n 5 per carton, Loop Max 70K
4 per carton, Allo 2500 at 8 mL) — no other combination balances.

Where the same product was bought twice at different prices (Loop Max
70K Green Apple Ice: $23.52 then $25.09 a pod), the later price is used
and the earlier one is in the `Note` column.

## Suggested retail is a placeholder

`Selling Price` is cost x 1.45, rounded to .99. That multiplier is
roughly where Ontario vape retail sits (ECO 6 mL at ~$20, GH20K at
~$38, Geek Bar 80K at ~$48), but it is a starting point, not the
store's pricing. Adjust before import.

## Barcodes could not be sourced from here

The barcode column is empty on all 134 rows. From this environment every
vape retailer, every manufacturer site and every public UPC database
(upcitemdb, barcodelookup, go-upc, barcodespider) is blocked by the
network egress policy — 18 of 18 attempts. Search snippets surfaced two
codes, neither for a product on these receipts.

The fastest way to fill them is from a normal browser: the official
stores are Shopify, and Shopify publishes barcodes in its product JSON.
Open these, save the page, and the codes can be matched in:

- https://stlthvape.com/products.json?limit=250 (add `&page=2` if 250 come back)
- https://flavourbeast.com/products.json?limit=250
- https://shopelfbar.ca/products.json?limit=250
- https://www.allovapor.com/products.json?limit=250

OVNS, Krave and Drip'n do not have official Shopify stores; a retailer
that stocks them (bayvape.ca, hazetownvapes.com) exposes the same JSON.
Otherwise, scan the box — the carton and the unit usually carry
different codes, and both lines in the Epos file want their own.

Known manufacturer prefixes, for checking whatever comes back:
STLTH `691584`, Allo / Flavour Beast / Level X `827152`.
