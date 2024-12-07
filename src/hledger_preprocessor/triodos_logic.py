"""Contains the logic for preprocessing Triodos .csv files to prepare them for
hledger."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Union

from typeguard import typechecked

from hledger_preprocessor.helper import parse_date


class TriodosParserSettings:
    def get_field_names(self) -> List[str]:
        return [
            "nr_in_batch",
            "account_holder",
            "bank",
            "account_type",
            "date",
            "some_account",
            "amount",
            "transaction_code",
            "category",
            "other_party",
            "another_account",
            "BIC",
            "description",
            "balance",
        ]

    def uses_header(self) -> bool:
        return True


@dataclass
class TriodosTransaction:
    account_holder: str
    bank: str
    account_type: str
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
            "account_holder": self.account_holder,
            "bank": self.bank,
            "account_type": self.account_type,
            "date": self.the_date.strftime("%Y-%m-%d"),
            "some_account": self.account0,
            "amount": self.amount0,
            "transaction_code": self.transaction_code,
            "category": "assets:HELLO",
            "other_party": self.other_party_name,
            "another_accont": self.account1,
            "BIC": self.BIC,
            "description": self.description,
            "balance": self.balance0,
        }

    def get_year(self) -> int:
        return int(self.the_date.strftime("%Y"))


@typechecked
def parse_triodos_transaction(
    row: List[str],
    nr_in_batch: int,
    account_holder: str,
    bank: str,
    account_type: str,
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
        account_holder=account_holder,
        bank=bank,
        account_type=account_type,
        nr_in_batch=nr_in_batch,
        the_date=parse_date(date_string),
        account0=account0,
        # amount0 = float(amount0.replace(',', '.')),
        amount0=float(amount0.replace(".", "").replace(",", ".")),
        transaction_code=transaction_code,
        other_party_name=other_party_name,
        account1=account1,
        BIC=BIC,
        description=description,
        # balance0 = float(balance0.replace(',', '.'))
        balance0=float(balance0.replace(".", "").replace(",", ".")),
    )
