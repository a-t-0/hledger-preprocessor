from dataclasses import dataclass
from typing import Dict, List, Optional

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


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
