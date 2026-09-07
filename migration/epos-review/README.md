# Review of the Epos Now product list (7 Sep 2026)

Epos returned their loaded catalogue as four CSVs (957 rows). This is a
row-by-row comparison against `../pos-import-no-tax.csv`, the 959-row
list sent to them, joined on barcode.

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

## Second fault: HST is being charged on the bottle deposit

Separate from the shift, and present on rows whose price is otherwise
correct.

**821 of 822 HST rows have `SalePriceIncTax` = `SalePriceExTax` x 1.13**,
with no allowance for the container deposit built into the price. A
deposit is not taxable, and the old till never taxed it — verified
against 5,060 deposit-bearing invoice lines, on every one of which
`VAT = (rate x qty - discount) x VATPer/100`, with the deposit added
after.

All **102** deposit-bearing products are affected: 1.3c overcharged on a
10c deposit, 7.8c on a 60c deposit.

## Third: six lottery products were dropped

`$12 LOTTO MAX`, `$20 LOTTO MAX.2 DRA`, `11 $LOTTO MAX`, `649 $7.00`,
`649/LIGHTING LOTTO`, `POKER LIGHT/LOTTO MAX` are in our list and absent
from theirs. Epos added four keys of their own — `LOTTO IN`,
`LOTTO OUT`, `INSTANT`, `INSTANT OUT` — with no barcode.

## `epos-corrected-import.csv`

Their exact seven-column format, ready to re-import: every price restored
from our list, `SalePriceIncTax` recomputed as
`(price - deposit) x 1.13 + deposit`, the six missing lottery products
added back, and their four new keys left untouched. 963 rows.
