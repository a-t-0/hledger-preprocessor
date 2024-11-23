"""Contains the logic for preprocessing Triodos .csv files to prepare them for
hledger."""

import csv
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Union

from typeguard import typechecked

from hledger_preprocessor.helper import parse_date


@typechecked
def get_triodos_fields() -> List[str]:
    return [
        "nr_in_batch",
        "date",
        "account0",
        "amount0",
        "transaction_code",
        "other_party",
        "account1",
        "BIC",
        "description",
        "balance0",
    ]


@dataclass
class TriodosTransaction:
    nr_in_batch: int
    the_date: datetime
    account0: str
    amount0: float
    transaction_code: str
    other_party_name: str
    account1: str
    BIC: str
    description: str
    balance0: float

    @typechecked
    def to_dict(self) -> Dict[str, Union[int, float, str, datetime]]:
        return {
            "nr_in_batch": self.nr_in_batch,
            "date": self.the_date.strftime("%Y-%m-%d"),
            "account0": self.account0,
            "amount0": self.amount0,
            "transaction_code": self.transaction_code,
            "other_party": self.other_party_name,
            "account1": self.account1,
            "BIC": self.BIC,
            "description": self.description,
            "balance0": self.balance0,
        }

    def get_year(self) -> int:
        return int(self.the_date.strftime("%Y"))


@dataclass
class TriodosRules:
    nr_of_header_lines: int
    currency: str
    account_holder: str
    bank_name: str
    account_type: str
    status: str

    @typechecked
    def create_rulecontent(self) -> str:
        content = ""
        # Write skip rule
        content += (
            "# If your `.csv` file contains a header row, you skip 1 row, if"
            " it does not have a header row, skip 0 rows.\n"
        )
        content += f"skip {self.nr_of_header_lines}\n\n"

        # Write fields
        content += f"fields {', '.join(get_triodos_fields())}\n\n"

        # Write currency
        content += f"currency {self.currency}\n"

        # Write status
        content += f"status {self.status}\n\n"

        # Write account1 and description format
        content += (
            "account1"
            " Assets:current:"
            f"{self.account_holder}:{self.bank_name}:{self.account_type}\n"
        )

        # TODO: include tag/category in this perhaps.
        # Original: description %desc1/%desc2/%desc3
        content += "description %desc1"
        return content


@typechecked
def write_processed_csv(
    transactions: List[TriodosTransaction], file_name: str
) -> None:
    # Get fieldnames dynamically from the first object in the list
    if transactions:
        fieldnames = transactions[0].to_dict().keys()

        with open(file_name, mode="w", encoding="utf-8", newline="") as outfile:
            # writer = csv.writer(outfile)
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            # Write each transaction as a row in the CSV
            for txn in transactions:
                writer.writerow(txn.to_dict())


@typechecked
def parse_tridos_transaction(
    row: List[str], nr_in_batch: int
) -> TriodosTransaction:

    # Split the row up into separate variables.
    (
        date_string,
        account0,
        amount0,
        transaction_code,
        other_party_name,
        account1,
        BIC,
        description,
        balance0,
    ) = row

    return TriodosTransaction(
        nr_in_batch=nr_in_batch,
        the_date=parse_date(date_string),
        account0=account0,
        amount0=float(amount0),
        transaction_code=transaction_code,
        other_party_name=other_party_name,
        account1=account1,
        BIC=BIC,
        description=description,
        balance0=float(balance0),
    )
