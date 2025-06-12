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
model = joblib.load("models/pleuroai_model.pkl")

# Azure OpenAI setup
openai_client = AzureOpenAI(
    api_key=os.getenv("OPENAI_KEY"),
    api_version="2023-05-15",
    azure_endpoint="https://openai-tpe-assistant.openai.azure.com/"
)

# Initialize Cosmos DB
cosmos_client = CosmosClient(
    "https://tpe-cosmosdb.documents.azure.com:443/",
    credential=os.getenv("COSMOS_KEY")
)
db = cosmos_client.get_database_client("TPEAssistant")
container = db.get_container_client("Predictions")


@app.route('/')
def home():
    return "✅ PleuroAI Prediction API is running"


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Step 1: Get input
        input_data = request.get_json()
        df = pd.DataFrame([input_data])

        # Step 2: Predict
      
        proba = model.predict_proba(df)[0]
        prediction_raw = model.predict(df)[0]

        # Get the index of the predicted class
        class_index = list(model.classes_).index(prediction_raw)
        confidence = round(proba[class_index] * 100, 2)

        prediction_label = "Likely Tuberculous Pleural Effusion (TPE)" if prediction_raw == 1 else "Likely Malignant Pleural Effusion (MPE)"

        # Step 3: GPT clinical advice based on prediction class
        if prediction_raw == 1:
            prompt = (
                f"The patient is predicted to have Tuberculous Pleural Effusion (TPE). "
                f"Based on this and the following data: {input_data}, please suggest the next clinical steps, "
                f"including confirmatory diagnostics and treatment recommendations."
            )
        elif prediction_raw == 2:
            prompt = (
                f"The patient is predicted to have Malignant Pleural Effusion (MPE). "
                f"Based on this and the following data: {input_data}, please suggest relevant next clinical steps, "
                f"including investigations to identify underlying malignancy, staging, and management plans."
            )
        else:
            prompt = (
                f"Patient data: {input_data}. Please suggest clinical management options based on the information."
            )

        gpt_response = openai_client.chat.completions.create(
            model="gpt-35-tpebot",
            messages=[
                {"role": "system", "content": "You are a clinical assistant specialized in pleural effusion diagnosis."},
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
            "confidence": f"{confidence}%",
            "gpt_response": advice
        }
        container.create_item(body=record)

        # Step 5: Return result
        return jsonify({
            "prediction": prediction_label,
            "confidence": f"{confidence}%",
            "gpt_response": advice
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=80)
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)
