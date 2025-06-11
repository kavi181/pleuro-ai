import streamlit as st
import requests

st.set_page_config(page_title="TPE Diagnosis Assistant", layout="centered")

st.title("🩺 TPE (Tuberculous Pleural Effusion) Diagnosis Assistant")

st.markdown("Enter patient information below to predict the likelihood of TPE and get clinical advice.")

# Input form
with st.form(key="prediction_form"):
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.selectbox("Gender", options=[0, 1], help="0 = Female, 1 = Male")
    us_echo = st.selectbox("Ultrasound Echo", options=[0, 1])
    us_diaphragm = st.selectbox("Ultrasound Diaphragm", options=[0, 1])
    us_fibrin = st.selectbox("Ultrasound Fibrin", options=[0, 1])
    us_pleural_thickening = st.number_input("Pleural Thickening (mm)", min_value=0.0, step=0.1)
    pf_protein = st.number_input("Pleural Fluid Protein (g/dL)", min_value=0.0, step=0.1)
    pf_ldh = st.number_input("Pleural Fluid LDH (U/L)", min_value=0.0, step=0.1)
    pf_glucose = st.number_input("Pleural Fluid Glucose (mg/dL)", min_value=0.0, step=0.1)
    pf_ada = st.number_input("Pleural Fluid ADA (U/L)", min_value=0.0, step=0.1)

    submit_button = st.form_submit_button("🔍 Predict")

if submit_button:
    with st.spinner("Sending data to TPE Assistant..."):
        input_data = {
            "AGE": age,
            "GENDER": gender,
            "US_ECHO": us_echo,
            "US_DIAPHRAGM": us_diaphragm,
            "US_FIBRIN": us_fibrin,
            "US_PLEURAL_THICKENING": us_pleural_thickening,
            "PF_PROTEIN": pf_protein,
            "PF_LDH": pf_ldh,
            "PF_GLUCOSE": pf_glucose,
            "PF_ADA": pf_ada
        }

        try:
            response = requests.post("http://127.0.0.1:5000/predict", json=input_data)
            result = response.json()

            st.success(f"✅ Prediction: **{result['prediction']}**")
            st.markdown("### 🧠 GPT Clinical Suggestion")
            st.info(result['gpt_response'])

        except Exception as e:
            st.error(f"❌ Failed to connect to backend: {str(e)}")
