import streamlit as st
import requests

st.set_page_config(page_title="PleuroAI Assistant", layout="centered")

st.title("🩺 PleuroAI - Pleural Effusion Diagnosis Assistant")
st.markdown("Enter patient information below to predict the likelihood of TPE/MPE and get clinical advice.")

# Input form
with st.form(key="prediction_form"):
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.selectbox("Gender", options=["Female", "Male"])
    us_echo = st.selectbox("Ultrasound Echo", options=["No", "Yes"])
    us_diaphragm = st.selectbox("Ultrasound Diaphragm",  options=["No", "Yes"])
    us_fibrin = st.selectbox("Ultrasound Fibrin",  options=["No", "Yes"])
    us_pleural_thickening = st.number_input("Pleural Thickening (mm)", min_value=0.0, step=0.1)
    pf_protein = st.number_input("Pleural Fluid Protein (g/dL)", min_value=0.0, step=0.1)
    pf_ldh = st.number_input("Pleural Fluid LDH (U/L)", min_value=0.0, step=0.1)
    pf_glucose = st.number_input("Pleural Fluid Glucose (mg/dL)", min_value=0.0, step=0.1)
    pf_ada = st.number_input("Pleural Fluid ADA (U/L)", min_value=0.0, step=0.1)

    submit_button = st.form_submit_button("🔍 Predict")

if submit_button:
    binary_map = {"No": 0, "Yes": 1}
    gender_map = {"Female": 0, "Male": 1}

    input_data = {
        "AGE": age,
        "GENDER": gender_map[gender],
        "US_ECHO": binary_map[us_echo],
        "US_DIAPHRAGM": binary_map[us_diaphragm],
        "US_FIBRIN": binary_map[us_fibrin],
        "US_PLEURAL_THICKENING": us_pleural_thickening,
        "PF_PROTEIN": pf_protein,
        "PF_LDH": pf_ldh,
        "PF_GLUCOSE": pf_glucose,
        "PF_ADA": pf_ada
    }


    if any(v is None or v == '' for v in input_data.values()):
        st.warning("⚠️ Please fill in all required input fields before predicting.")
    else:
        with st.spinner("Sending data to PleuroAI Assistant..."):
            try:
                response = requests.post("http://127.0.0.1:5000/predict", json=input_data)

                if response.status_code == 200:
                    result = response.json()
                    if 'prediction' in result:
                        st.markdown("### 🧪 Prediction Result")
                        st.success(f"**Diagnosis:** {result['prediction']}")
                        st.info(f"**Confidence Level:** {result['confidence']}")

                        st.markdown("### 🧠 GPT Clinical Suggestion")
                        st.info(result['gpt_response'])
                    else:
                        st.error("❌ Unexpected response format from backend.")
                else:
                    st.error(f"❌ Failed to connect to backend: {response.text}")
            except Exception as e:
                st.error(f"❌ Backend error: {str(e)}")
