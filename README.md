# 🩺 PleuroAI Assistant - AI-Powered Clinical Decision Support Tool

This project is developed for the Microsoft Azure Hackathon 2025. The **PleuroAI Assistant** is a clinical support tool designed to assist in diagnosing **Tuberculous Pleural Effusion (TPE) or Malignant Pleural Effusion (MPE)** using machine learning, with guidance provided by GPT-based suggestions.

## 🔍 Project Overview

The assistant receives a patient's diagnostic input, predicts the likelihood of TPE/MPE, and recommends the next clinical steps using GPT (OpenAI) integration.

---

## 🚀 Future Development

We plan to:
- Extend the model for **multi-class classification** to include other pleural diseases
- Enhance GPT prompts for **differential diagnosis**
  

## ⚙️ Tech Stack

- **Python 3.11**
- **Scikit-learn** – for machine learning model
- **Flask** – for serving API
- **Streamlit** – for interactive UI
- **Azure OpenAI** – GPT model for clinical advice
- **Azure Cosmos DB** – to store input, prediction, and advice
- **GitHub** – source code repository

---

## 🧠 AI Model

- Trained using cleaned dataset of 133 samples.
- Uses patient features such as:
  - Age, Gender
  - Ultrasound findings (ECHO, DIAPHRAGM, FIBRIN, THICKENING)
  - Pleural Fluid Tests (PROTEIN, LDH, GLUCOSE, ADA)
- Output: Prediction (Likely TPE / Not TPE)

---

## 🧪 Sample Input Format

```json
{
  "AGE": 45,
  "GENDER": 1,
  "US_ECHO": 1,
  "US_DIAPHRAGM": 0,
  "US_FIBRIN": 1,
  "US_PLEURAL_THICKENING": 1.2,
  "PF_PROTEIN": 4.3,
  "PF_LDH": 250,
  "PF_GLUCOSE": 4.9,
  "PF_ADA": 45
}
