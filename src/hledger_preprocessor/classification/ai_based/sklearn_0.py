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
def transactions_to_dataframe(*, transactions: List[TriodosTransaction]):
    data = pd.DataFrame(
        [
            {
                "amount": txn.amount0,
                "account": txn.account0,
                "description": txn.description,
            }
            for txn in transactions
        ]
    )
    return data


def add_ai_category(
    *, ai_model_name: str, transactions: List[TriodosTransaction]
):
    # Preprocessing: handle missing data
    imputer = SimpleImputer(strategy="most_frequent")
    data = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)

    # Splitting features and target
    X = data[["amount", "account", "time", "description"]]
    y = data["category"]

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define column transformations
    numeric_features = ["amount"]
    categorical_features = ["account", "time"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("text", TfidfVectorizer(), "description"),
            ("cat", "passthrough", categorical_features),
        ]
    )

    # Define the pipeline
    pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(random_state=42)),
        ]
    )

    # Train the model
    pipeline.fit(X_train, y_train)

    # Evaluate the model
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the model locally
    joblib.dump(pipeline, "expense_category_model.pkl")


# Example of prediction
def predict_category(amount, account, time, description):
    model = joblib.load("expense_category_model.pkl")
    input_data = pd.DataFrame(
        {
            "amount": [amount],
            "account": [account],
            "time": [time],
            "description": [description],
        }
    )
    return model.predict(input_data)[0]


# Example usage
category = predict_category(
    50.0, "personal:bank:checking", "morning", "grocery shopping"
)
print("Predicted Category:", category)
