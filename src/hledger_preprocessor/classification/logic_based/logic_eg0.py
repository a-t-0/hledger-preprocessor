from typing import Dict

from hledger_preprocessor.classification.logic_based.private_logic import (
    private_credit_classification,
    private_debit_classification,
)
from hledger_preprocessor.parser_logic_structure import Transaction


class ExampleLogicModel:
    name = "ExampleLogicModel"

    def classify(self, transaction: Transaction) -> str:
        if transaction is None:
            raise ValueError("Transaction cannot be None.")
        # TODO: Generalise to support for all Transaction types.
        if transaction.transaction_code == "Debet":
            return self.classify_debit(transaction=transaction)
        elif transaction.transaction_code == "Credit":
            return self.classify_credit(transaction=transaction)
        else:
            raise ValueError(f"Unknown transaction_code for:{transaction}")

    def classify_debit(self, transaction: Transaction) -> str:

        tnx_dict = transaction.to_dict_without_classification()
        if self.dict_contains_string(
            d=tnx_dict, substr="IKEA BV", case_sensitive=False
        ):
            return "house:furniture:Ikea"
        if self.dict_contains_string(
            d=tnx_dict, substr="Eko Plaza", case_sensitive=False
        ):
            return "groceries:eko_plaza"
        if private_debit_classification(transaction=transaction) is not None:
            return private_debit_classification(transaction=transaction)
        else:
            print("\n write a rule for expense:")
            input(transaction)

    def classify_credit(self, transaction: Transaction) -> str:
        tnx_dict = transaction.to_dict_without_classification()
        if dict_contains_string(
            d=tnx_dict, substr="IKEA BV", case_sensitive=False
        ):
            return "restitution:furniture:Ikea"
        if private_credit_classification(transaction=transaction) is not None:
            return private_credit_classification(transaction=transaction)
        else:
            print("\n write a rule for income:")
            input(transaction)

    def dict_contains_string(
        self, d: Dict, substr: str, case_sensitive: bool
    ) -> bool:
        if case_sensitive:
            return any(substr in str(value) for value in d.values())
        else:
            return any(
                substr.lower() in str(value).lower() for value in d.values()
            )
