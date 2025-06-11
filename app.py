from flask import Flask, request, jsonify
import joblib
import pandas as pd
from openai import AzureOpenAI
from azure.cosmos import CosmosClient
import uuid
import os

from dotenv import load_dotenv
load_dotenv()

# Flask app
app = Flask(__name__)

# Load model
model = joblib.load("models/tpe_model.pkl")

# Azure OpenAI setup
openai_client = AzureOpenAI(
    api_key = os.getenv("OPENAI_KEY"),
    api_version="2023-05-15",
     azure_endpoint="https://openai-tpe-assistant.openai.azure.com/"
)

# Initialize Cosmos DB
cosmos_client = CosmosClient("https://tpe-cosmosdb.documents.azure.com:443/", 
credential=os.getenv("COSMOS_KEY"))
db = cosmos_client.get_database_client("TPEAssistant")
container = db.get_container_client("Predictions")



@app.route('/')
def home():
    return "✅ TPE Prediction API is running"


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Step 1: Get input
        input_data = request.get_json()
        df = pd.DataFrame([input_data])

        # Step 2: Predict
        prediction = model.predict(df)[0]
        prediction_label = "Likely TPE" if prediction == 1 else "Not TPE"

        # Step 3: GPT clinical advice
        prompt = f"Patient information: {input_data}\nPrediction: {prediction_label}\nWhat should be the next clinical step?"
        gpt_response = openai_client.chat.completions.create(
            model="gpt-35-tpebot",
            messages=[
                {"role": "system", "content": "You are a clinical assistant specialized in TPE."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=500
        )
        advice = gpt_response.choices[0].message.content

        # Step 4: Save to Cosmos DB
        record = {
            "id": str(uuid.uuid4()),
            "input": input_data,
            "prediction": prediction_label,
            "gpt_response": advice
        }
        container.create_item(body=record)

        # Step 5: Return result
        return jsonify({
            "prediction": prediction_label,
            "gpt_response": advice
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)