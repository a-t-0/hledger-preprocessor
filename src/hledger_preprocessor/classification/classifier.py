from typing import List

from hledger_preprocessor.parser_logic_structure import Transaction


# Function to classify transactions (AI and logic-based classifications)
def classify_transactions(
    transactions: List[Transaction], ai_models, logic_models
):
    for txn in transactions:
        for ai_model in ai_models:
            # AI-based classification (replace `ai_model.predict` with your actual model logic)
            ai_classification = ai_model.predict(
                {
                    "amount": txn.amount0,
                    "account": txn.account0,
                    "description": txn.description,
                }
            )
            txn.ai_classification = {ai_model.name: ai_classification}

        # Logic-based classification (replace `logic_model.classify` with your actual logic logic)
        for logic_model in logic_models:
            logic_classification = logic_model.classify(
                {
                    "amount": txn.amount0,
                    "account": txn.account0,
                    "description": txn.description,
                }
            )
            txn.logic_classification = {logic_model.name: logic_classification}

    return transactions
