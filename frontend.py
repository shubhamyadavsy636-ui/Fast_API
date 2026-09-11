import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Insurance premium Category Predictor")

st.markdown("Enter your detail below")

age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("weight [kg]", min_value=1.0, value=65.00)
height = st.number_input("height [m]", min_value=0.5, value=1.75)
income_lpa = st.number_input("salery in lpa ", min_value=1, value=10)
smoker = st.selectbox("Are you smoker?", options=[True,False])
city = st.text_input("city", value='Mumbai')
occupation = st.selectbox(
    "Occupation",
    [
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job"
    ]
)



if st.button('Predict preminum Category'):
    input_data = {
        'age':age,
        'weight':weight,
        'height':height,
        'income_lpa': income_lpa,
        'smoker':smoker,
        'city': city,
        'occupation': occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code  == 200:
            result = response.json()

            st.success(f"predicted Insurance premium category: **{result['predicted_category']}**")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Could not connecet to the fastAPI server. Make sure Its running on port 8000.")
