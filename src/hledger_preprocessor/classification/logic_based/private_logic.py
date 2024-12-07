from typing import Dict, Optional

from hledger_preprocessor.classification.helper import dict_contains_string
from hledger_preprocessor.parser_logic_structure import Transaction


def private_debit_classification(
    *, transaction: Transaction, tnx_dict: Dict
) -> Optional[str]:
    return None


def private_credit_classification(
    *, transaction: Transaction, tnx_dict: Dict
) -> Optional[str]:
    return None
