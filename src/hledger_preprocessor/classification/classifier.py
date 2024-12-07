from typing import List

from hledger_preprocessor.parser_logic_structure import Transaction


# Function to classify transactions (AI and logic-based classifications)
def classify_transactions(
    transactions: List[Transaction], ai_models, logic_models
):
    for txn in transactions:
        for ai_model in ai_models:
            # AI-based classification (replace `ai_model.predict` with your actual model logic)
            # ai_classification = ai_model.predict(
            #     {
            #         "bank": txn.bank,
            #         "account_type": txn.account_type,
            #         "date": txn.the_date.strftime("%Y-%m-%d"),
            #         "account_owner": txn.account0,
            #         "amount": txn.amount0,
            #         "transaction_code": txn.transaction_code,
            #         "other_account": txn.account1,
            #         "other_party": txn.other_party_name,
            #         "BIC": txn.BIC,
            #         "description": txn.description,
            #     }
            # )
            # txn.ai_classification = {ai_model.name: ai_classification}
            txn.ai_classification = {ai_model.name: "filler"}

        for logic_model in logic_models:

            logic_classification = logic_model.classify(transaction=txn)
            txn.logic_classification = {logic_model.name: logic_classification}

    return transactions
