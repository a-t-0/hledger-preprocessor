"""Contains the logic for preprocessing Triodos .csv files to prepare them for
hledger."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Union

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
            "account_owner",
            "amount",
            "transaction_code",
            "other_party",
            "other_account",
            "BIC",
            "description",
            "this_is_the_balance",
            "ai_classification",
            "logic_classification",
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
    ai_classification: Optional[Dict[str, str]] = None
    logic_classification: Optional[Dict[str, str]] = None

    @typechecked
    def to_dict(self) -> Dict[str, Union[int, float, str, datetime]]:
        base_dict: Dict[str, Union[int, float, str, datetime]] = (
            self.to_dict_without_classification()
        )
        if self.ai_classification is not None:
            # TODO: determine how to collapse/select/choose the AI model that is exported.
            base_dict["ai_classification"] = self.ai_classification[
                "ExampleAIModel"
            ]
        else:
            base_dict["ai_classification"] = None

        if self.logic_classification is not None:
            # TODO: determine how to collapse/select/choose the AI model that is exported.
            base_dict["logic_classification"] = self.logic_classification[
                "ExampleLogicModel"
            ]
        else:
            base_dict["logic_classification"] = None
        return base_dict

    def to_dict_without_classification(
        self,
    ) -> Dict[str, Union[int, float, str, datetime]]:
        return {
            "nr_in_batch": self.nr_in_batch,
            "account_holder": self.account_holder,
            "bank": self.bank,
            "account_type": self.account_type,
            "date": self.the_date.strftime("%Y-%m-%d"),
            "account_owner": self.account0,
            "amount": self.amount0,
            "transaction_code": self.transaction_code,
            "other_party": self.other_party_name,
            "other_account": self.account1,
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
