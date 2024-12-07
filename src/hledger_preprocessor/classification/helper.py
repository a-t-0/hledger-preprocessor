from typing import List

import pandas as pd


# Example function to convert a list of transactions to a DataFrame
def transactions_to_dataframe(transactions: List[TriodosTransaction]):
    data = pd.DataFrame(
        [
            {
                "amount": txn.amount0,
                "account": txn.account0,
                "description": txn.description,
                "ai_classification": txn.ai_classification,
                "logic_classification": txn.logic_classification,
            }
            for txn in transactions
        ]
    )
    return data
