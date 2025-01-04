# Hledger .csv bank statement preprocessor for hledger-flow

[![Python 3.12][python_badge]](https://www.python.org/downloads/release/python-3120/)
[![License: AGPL v3][agpl3_badge]](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style: Black][black_badge]](https://github.com/ambv/black)

For double-entry bookkeeping, transactions need to be classified into
categories, e.g. groceries, rent, income etc. This preprocessing repo aims to
support:

- Pure logic based transaction classification.
- AI-based auto-transaction classification.

## Dev Instructions

See [Developer_instructions.md](Developer_instructions.md).

## Context

This pip package is called by the
[modified hledger-flow repository](https://github.com/a-t-0/hledger-flow)
to pre-processes bank `.csv` files so that hledger-flow can convert them into
`hledger` journals.

## Prerquisites

First install this pip package with:

```bash
pip install hledger_preprocessor
```

## TL;DR call from hledger-flow

First run `hledger-flow` which calls this code.

## TL;DR run directly

1. Start by creating the relevant directory structure and adding the `.csv`
   files you got from your bank/place into them with:

```sh
clear && hledger_preprocessor \
--new \
--csv-filepath ~/Downloads/some_unprocessed.csv \
--start-path ~/finance/retry \
--account-holder swag \
--bank some_bank \
--account-type some_type
```

2. Check if your classification logic covers all your transactions with:

```sh
clear && hledger_preprocessor \
--input-file ~/finance/import/swag/some_bank/some_type/1-in/2024/some_unprocessed.csv \
--start-path ~/finance \
--account-holder swag \
--bank some_bank \
--account-type some_type \
--pre-processed-output-dir=2-preprocessed
```

If your classification logic is complete, it is silent. Otherwise, it will say something like:

```txt
print("\n Please add a rule for expense/income (and run again):")
<some bank transaction>
```

If it does, go to file:
`src/hledger_preprocessor/classification/logic_based/private_logic.py` and add
that rule to the functions: `def private_debit_classification(` and
`def private_credit_classification(` depending on whether the transaction and
expense or income.

To see how to add rules, look at:
`def classify_debit(self, transaction: Transaction) -> str:` In essence you add
more `if dict_contains_string(..) then return <some category>` lines until all your
transactions are classified using your classification logic.

3. Go back to step 2 until your logic classifies all your transactions.
1. Generate the `.rules` file for `hledger-flow`:

```sh
clear && hledger_preprocessor \
--generate-rules \
--start-path ~/finance \
--account-holder swag \
--bank some_bank \
--account-type some_type
```

<!-- Un-wrapped URL's below (Mostly for Badges) -->

[agpl3_badge]: https://img.shields.io/badge/License-AGPL_v3-blue.svg
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[python_badge]: https://img.shields.io/badge/python-3.6-blue.svg
