from transformers import pipeline


# Example usage
class ExampleAIModel:
    name = "ExampleAIModel"

    # Load a text classification pipeline with a pre-trained model
    classifier = pipeline(
        "text-classification", model="distilbert-base-uncased"
    )

    def predict(self, data):

        text = (
            f"{data['description']} | Amount: {data['amount']} | Account:"
            f" {data['account']}"
        )
        result = self.classifier(text)
        print(f"result=")
        print(result)
        return result[0]["label"]
        # Replace with real prediction logic
        # return "some_ai_category


# Replace ExampleAIModel with the Hugging Face-based classifier
# class HuggingFaceAIModel:
# name = "HuggingFace-DistilBERT"


# Use HuggingFaceAIModel in your workflow
# huggingface_model = HuggingFaceAIModel()
# classified_transactions = classify_transactions(transactions, huggingface_model, logicmodel)
