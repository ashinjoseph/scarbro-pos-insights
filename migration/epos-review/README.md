# Review of the Epos Now product list (7 Sep 2026)

Epos returned their loaded catalogue as four CSVs (957 rows). This is a
row-by-row comparison against `../pos-import-no-tax.csv`, the 959-row
list sent to them, joined on barcode.

*Analysis by Claude (Anthropic), working from an export of the store's
previous POS database.*

## What is right

- **953 of 959 products matched on barcode.** Nothing was invented and
  nothing extra was added except four lottery keys.
- **Tax groups are correct on all 953** — HST or NoTax exactly as sent.
- **Categories are correct on all 953**, except the lottery products,
  which arrived with a blank category.

## What is wrong: 485 of 953 prices, and they are our own prices

**51% of the prices are wrong.** The important finding is *how*: the
prices are not miscalculated, they are our prices sitting on the wrong
products.

- The multiset of price values is essentially unchanged — of 953 prices,
  only 4 values differ from what we sent.
- **482 of the 485 wrong prices (99%) are values that appear elsewhere
  in our list.**
- 44% of the errors are explained by the price column sitting exactly
  **four rows out of step** with the product rows. The rest follow the
  same pattern with the offset changing at several points in the file.

So a price column was pasted or sorted independently of the rows it
belongs to. `ProductList_2.csv` is 90% intact; the other three files are
badly shifted, which is consistent with the damage happening while the
data was being split or re-sorted rather than at import.

The scale of it:

| | |
|---|---:|
| Priced above ours | 256 products |
| Priced below ours | 229 products |
| Largest overcharge | $117.47 |
| Largest undercharge | $107.96 |
| Median error | $2.81 |

Worked examples:

- `Nestle Parlour Vanilla` should be $7.50 and is loaded at **$123.89**
  — that is `Next Original KS 25 carton`'s price.
- `Pabst Blue Ribbon 6 pk` should be $15.51 and is loaded at **$119.50**
  — that is `Pall Mall Bold cart.`'s price.
- `Match 20` should be $9.74 and is loaded at **$95.58**, a carton price.
- `Stella Artois 6 x 473ml` should be $21.49 and is loaded at **$1.99**.

`epos-price-errors.csv` lists every one with the correct value.

## The 19 lottery lines come first

Fixed-denomination tickets, where the price has to be exact or the till
cannot balance against OLG:

| | Loaded | Should be |
|---|---:|---:|
| LOTTO MAX$10 | $2.21 | $10.00 |
| Super $20 | $3.99 | $20.00 |
| LOT, MAX 10 DRAW.$50 | $22.00 | $50.00 |
| LOTTO 649 $13 | $31.00 | $13.00 |
| LOTO MAX $30 | $13.00 | $30.00 |

## Two things deliberately not raised

**Bottle deposit tax.** Epos computes `SalePriceIncTax` as
`SalePriceExTax x 1.13` on all 821 taxable rows, so HST is charged on
the container deposit — 1.3c on a 10c deposit, 7.8c on a 60c one, across
102 products. The owner reviewed this and accepted it: the workaround is
not worth the effort. Not an error to report.

**Six dropped lottery products.** Removed by the owner on purpose.

## `pos-import-corrections.csv`

The 485 mispriced products in the same seven columns, same order, as the
list originally emailed to Epos. Every row is byte-for-byte identical to
that file, so it can be applied directly.

## `epos-corrected-import.csv`

A full rebuild in Epos's own seven-column format, kept for reference. It
recomputes `SalePriceIncTax` as `(price - deposit) x 1.13 + deposit` and
restores the six lottery products — neither of which the owner wants,
so **`pos-import-corrections.csv` is the file to send**, not this one.

---

# Round 2 — after Epos reloaded (8 Sep 2026)

*Verified by Claude (Anthropic) against `../pos-import-no-tax.csv`,
joined on barcode.*

**458 of the 485 wrong prices are fixed — 94.4%.** The column shift is
gone. Tax groups still match on all 953, categories still match, no
product was lost or added.

## 27 prices are still wrong, and they split cleanly

**19 are products that share a name with another product.** Epos gave
every copy in a name group the same price, which means the update was
applied by product name rather than by barcode:

| Name | Epos gave all copies | Our prices |
|------|---:|---|
| Ven Dens Car Holder | $15.99 | $6.99 / $11.99 / $12.99 / $15.99 |
| Van Dens Earphones | $15.99 | $8.99 / $9.99 / $12.99 / $15.99 |
| Ven Dens Adapter | $17.99 | $17.99 / $20.99 / $37.99 |
| michelob ultra | $3.49 | $3.49 / $22.18 |
| Tide detergent | $7.99 | $3.99 / $7.99 |

Eleven name groups collapsed this way. `michelob ultra` is the costly
one — a single can and a six-pack now ring up at the same $3.49.

**8 are one-offs** with no name collision, so they look like rows simply
missed in the reload:

`LOT, MAX 10 DRAW.$50` ($22.00, should be $50.00), `RAID ANT,ROACH &
EARWIG`, `WRIGLEYS DOUBLE MINT`, `M & M CANDY,GUMS & CHOCOLATES 48G`,
`Nestle drumstick CANDY,GUMS & CHOCOLATES`, `POP SHOP COTTON CANDY...`,
`Lays Classic 60g`, `Miss Vickies Origianl 55g`.

The lottery one matters most: a $50 Lotto Max book is still priced at
$22.

## Everything else checks out

- Tax groups: 0 mismatches on 953 products.
- Categories: 0 mismatches, apart from the lottery rows which carry a
  blank category on their side.
- Coverage: no product added or lost. The six lottery products the owner
  removed are still out, and Epos's own four keys are untouched.
- `SalePriceIncTax` is `ExTax x 1.13` throughout, as accepted. One row,
  `Heineken 6* 330Ml Bottle`, is a cent light ($19.77 against $19.78).

## `pos-import-corrections-round2.csv`

The 27 products in the same seven columns as the original list, each row
byte-for-byte identical to it. **These must be applied by barcode, not
by name** — matching on name is what left 19 of them wrong.
