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

    def uses_header(self) -> bool:
        return True


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
