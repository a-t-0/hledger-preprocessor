import os

from gpt4all import GPT4All
from transformers import pipeline


# Example usage
class ExampleAIModel:
    name = "ExampleAIModel"

    def default(self, data):
        return "ai_filler"

    def get_debet_question(self, data: str) -> str:
        llm_classification_question: str = (
            f"""What kind of an expense is this transaction? Some example
 categories are:
- groceries:EkoPlaza
- rent
- travel:train
- travel:bus
- ..
Give a category and/or subcategory('s) in format:
  <category>:<subcategory1>:subcategory2>
 with a depth of 0 to 2 max. Do not give any explanation, only give the above
 format for the following transaction:\n{data}"""
        )
        return llm_classification_question

    def get_credit_question(self, data: str) -> str:
        llm_classification_question: str = (
            f"""What kind of an income is this transaction? Some example
categories are:
- income:salary
- loan_repayment:friend
- income:zorgtoeslag
- ..
Give a category and/or subcategory('s) in format:
  <category>:<subcategory1>:subcategory2>
with a depth of 0 to 2 max. Do not give any explanation, only give the above
format for the following transaction:\n{data}"""
        )
        return llm_classification_question

    def predict(self, data):

        # Try loading a model from the internets.
        print("Start loading gpt4all model.")
        # model = GPT4All("gpt4all-lora-quantized")
        # model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
        # model = GPT4All("llama-2-7b-chat.ggmlv.q4_K_M.bin") # DOn't have file

        # Load local model.
        main_user_path = os.path.expanduser("~")
        model_filename: str = "Meta-Llama-3.1-8B-Instruct-Q5_K_S.gguf"
        local_model_filepath: str = f"{main_user_path}/.models/{model_filename}"
        assert os.path.exists(
            local_model_filepath
        ), f"File does not exist: {local_model_filepath}"
        model = GPT4All(
            local_model_filepath,
        )

        print("Done loading gpt4all model.")
        # TODO: Generalise to support for all Transaction types.
        if data["transaction_code"] == "Debet":
            prompt = self.get_debet_question(data=data)
        elif data["transaction_code"] == "Credit":
            prompt = self.get_credit_question(data=data)
        else:
            raise ValueError(f"Unknown transaction_code for:{data}")

        print(f"\nAsking Question:\n{prompt}\n")
        result = model.generate(prompt)
        print("Answer:\n")
        print(result)
        print("\n")
        return result.strip()

    def try0(self, data):

        text = (
            f"{data['description']} | Amount: {data['amount']} | Account:"
            f" {data['account']}"
        )
        result = self.classifier(text)
        print(f"result=")
        print(result)
        return result[0]["label"]

    def try1(self, data):
        # Load a text classification pipeline with a pre-trained model
        classifier = pipeline(
            "text-classification", model="distilbert-base-uncased"
        )
        labels = [
            "groceries",
            "electricity_bill",
            "rent",
            "entertainment",
            "others",
        ]

        # Perform classification.
        text = (
            f"{data['description']} | Amount: {data['amount']} | Account:"
            f" {data['account']}"
        )
        preprocessed_text = preprocess_text(text)  # Preprocess the text

        # Create a tensor from the preprocessed text
        input_tensor = tf.convert_to_tensor([preprocessed_text])

        # Make the prediction
        prediction = self.model.predict(input_tensor)
        print("prediction=")
        print(prediction)

        # Convert the prediction to a class label
        predicted_class = class_labels[tf.argmax(prediction)]

        return predicted_class

    def try2(self, data):
        # Load a text classification pipeline with a pre-trained model
        classifier = pipeline(
            "text-classification", model="distilbert-base-uncased"
        )
        labels = [
            "groceries",
            "electricity_bill",
            "rent",
            "entertainment",
            "others",
        ]

        # Perform classification.
        text = (
            f"{data['description']} | Amount: {data['amount']} | Account:"
            f" {data['account']}"
        )
        result = self.classifier(text, candidate_labels=self.labels)
        print(f"result: {result}")
        return result["labels"][0]  # Top label (most likely category)

    def try3(self, data):
        import fasttext

        fasttext.load_model("lid.176.ftz")  # Language ID model as placeholder
        text = (
            f"{data['description']} | Amount: {data['amount']} | Account:"
            f" {data['account']}"
        )
        prediction = model.predict(text)
        print(prediction)
        return prediction[0][0]  # Return top prediction
