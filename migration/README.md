# Product migration shortlist

Built from `RetailPOS_DB 09-03-2026_21-53-25.bak` (19,787 invoices,
15 Apr – 3 Sep 2026, 23,581 products in the catalogue).

The catalogue carries a large tail of products that have never been
sold. On **14 April 2026** — migration day — 23,177 products were
bulk-loaded in a single batch. Only 404 products have been added since.
These lists separate the live catalogue from that import residue.

## Files

| File | Rows | Contents |
|------|-----:|----------|
| `1-products-added-since-apr15.csv` | 404 | `AddedDate >= 2026-04-15` |
| `2-products-sold-distinct-barcode.csv` | 874 | one row per barcode with at least one sale |
| `3-product-migration-list.csv` | 992 | union of the two (404 + 874 − 286 overlap) |

All three share the same columns, so they can be diffed directly.

`Source` records which list each row came from: `both` 286,
`sold only` 588, `added only` 118.

## Barcodes

All 23,581 products have a unique, non-blank barcode — 0 blanks,
0 collisions. Deduplicating by barcode is therefore a no-op, and
list 3 is already one row per barcode.

Genuine duplicates are by **name**: 38 groups covering 95 products,
flagged in `DuplicateNameGroup` (e.g. `CASH BACK`, `Tide`). They are
flagged rather than merged — each has its own barcode and its own
sales history, so they may be different sizes or a repackaged SKU
rather than a data-entry error. These need a human decision.

## MigrationAction

A first-pass triage, not a verdict:

| Value | Rows |
|-------|-----:|
| `MIGRATE` | 574 |
| `REVIEW - 2 units or fewer` | 174 |
| `REVIEW - no sale in 90+ days` | 126 |
| `REVIEW - new, no sales yet` | 118 |

The 118 "new, no sales yet" were added after 15 Apr and have not sold.
Absence of sales is not yet evidence against them.

Revenue covered by list 3 is $263,242.89 — effectively all of it,
since anything that sold is included by construction.

## Method

`Product` left-joined to an aggregate over `Invoice_Product` /
`InvoiceInfo` giving transactions, units, revenue, and first/last
sale date per product. Lists 1 and 2 are filters over that base;
list 3 is their union with `Source` and `MigrationAction` derived
in post-processing.
