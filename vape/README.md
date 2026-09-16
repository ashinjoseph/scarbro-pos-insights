# YV Vape Shop — product list from supplier receipts (Aug–Sep 2026)

Built from eight purchase records: Big Smoke Distro invoices 9007
(25 Aug) and 9160 (2 Sep), Pinnacle Commerce invoices 19583
(12 Aug) and 19825 (1 Sep), a STLTH wholesaler order, a Flavour Beast /
Level X order (26 Aug), order #1373225 (1 Sep), and the order
confirmation behind invoice 19825.

**77 distinct products** across STLTH, Elf Bar, OVNS, Krave, Allo,
Drip'n, Flavour Beast and Level X.

## Files

| File | What |
|------|------|
| `vape-products.csv` | One row per product: pack size, invoice price, excise, unit and carton cost, suggested retail, source |
| `vape-epos-import.csv` | Epos seven-column format, **148 rows** — a single-unit line and a carton line for every product |
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
checked against every receipt that itemises it and reproduces all five
to the cent: $322.56, $461.44, $33.60, $257.60 and $380.80. That check also settled the
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

## Barcodes: 22 from the Big Smoke invoices, 55 still to find

Big Smoke prints each item's barcode above the product name, so 22
products carry a code read straight off invoices 9007 and 9160. Their
prefixes match the known manufacturer ranges (STLTH `691584`, Allo /
Flavour Beast / Drip'n `827152`, Elf Bar `694197`, OVNS `693705`), with
one caveat: `641961` appears on both an Elf Bar and an Allo product, so
it is a Canadian distributor prefix rather than a manufacturer one —
those three are worth one confirming scan. Big Smoke's own SKU numbers
(`100000xxxxxx`, `3858`) are not barcodes and were left out.

The invoice code is the one Big Smoke uses to identify the carton line;
it is most likely the unit UPC, but one scan of a unit against a carton
will settle it, and both Epos lines want their own code.

`claude-chrome-barcode-prompt.txt` is the prompt for the remaining 55,
covering only those products. From this environment every
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

---

# Website catalogue — products added 14–15 Sep 2026

Source: `RetailPOS_DB_16-09-2026_10-28-27.bak` (16 Sep, 20,571 invoices,
23,745 products — the container now runs this backup).

**162 products were added on 14–15 Sep, every one of them VAPE & CIGAR.**
`vape-web-catalog.csv` holds the 161 with a retail price, ready for a web
product catalogue.

| Column | Notes |
|--------|-------|
| Barcode | from the POS; all 161 present and distinct |
| SKU | `YV-<PID>`, stable handle for the website |
| Product Name | rebuilt from brand + line + flavour |
| Brand / Product Line / Flavour / Type | parsed from the till name |
| Nicotine, E-liquid (mL) | from the product line |
| Price (ex tax) / Price (incl HST) | till price, and x1.13 |
| Supplier Cost / Margin % | matched from the purchase invoices, 56 of 161 |
| Data Flags | rows needing a human before they go live |

## Names had to be rebuilt, not copied

The till names are heavily abbreviated and carry typos — `STRBRY KIWI
ICE`, `PMPDUP PINAPL`, `JUICT PEACH`, `SMOTTH TOBACCO`, `BEAST MODZ`,
`PRACHY PEACE ICE`. None of that belongs on a website, so `Product Name`
is rebuilt from the parsed brand, line and flavour with the
abbreviations expanded and the obvious typos corrected. The original
till name stays in the POS untouched.

One correction worth noting: seven products are named `ALLO ULTRA 1K
POD` in the till but are the 10K pod — the catalogue says 10K.

## The POS barcode is not the invoice barcode

None of the 22 barcodes read off the Big Smoke invoices appear among
these 162, even for products that are clearly the same item. Where both
are known the codes sit close together — the three STLTH ECO Mini
flavours differ by exactly 99 — which is consistent with the invoice
carrying the **carton** code and the POS the **unit** code. Three pairs
is not enough to generalise, so no barcode was derived that way; the
catalogue uses the POS code, which is the one that scans at the till.

## Margin

Where an invoice cost could be matched (56 products), margin runs 0% to
45%, median 33%. The two ends are worth a look before publishing:
`ALLO Ultra 10K Pod Watermelon Ice` sells at $18.99 against a $18.93
cost — effectively zero — while the Krave Pulse X pair run at 45%.

`PurchaseCost` is 0.00 on all 162 rows in the POS itself; the cost here
comes entirely from the supplier invoices.

## 12 rows to fix before going live

- **1 row holds five barcodes in one field** (`OVNS 50K`) — it needs
  splitting into five products, and a sixth `OVNS 50K` row duplicates
  one of them.
- **12 rows have no flavour in the name**: five `STLTH Loop 25K Pod`,
  two `STLTH Loop Max 70K Pod`, two `Flavour Beast 60K`, two `OVNS 50K`,
  one `Level X Boost G2`. They are distinct products with distinct
  barcodes, so the flavour has to come from the box.
- One product (`VAPE`, barcode 24586) is an open-price key, not a
  product, and is excluded.
