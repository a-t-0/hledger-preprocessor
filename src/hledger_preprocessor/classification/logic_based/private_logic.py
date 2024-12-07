from typing import Dict,Optional

from hledger_preprocessor.parser_logic_structure import Transaction

def private_debit_classification(*, transaction: Transaction) -> Optional[str]:
    return None
def private_credit_classification(*, transaction: Transaction) -> Optional[str]:
    return None