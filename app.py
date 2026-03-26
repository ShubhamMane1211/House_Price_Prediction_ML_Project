import streamlit as st
import pandas as pd
import numpy as np
import joblib


model = joblib.load("house_price_model.pkl")
columns = joblib.load("columns.pkl")

st.title("House Price Prediction App")
st.write("Enter Property Details")

git ls-files
bhk = st.number_input("Number of BHK", min_value=1, max_value=10, step=1)
area = st.number_input("Area (sq ft)", min_value=100, max_value=10000)
type_option = st.selectbox(
    "Property Type", ["Apartment", "Villa", "Studio", "Penthouse", "Independent House"]
)
status_option = st.selectbox("Status", ["Ready to move", "Under Construction"])
age_option = st.selectbox("Age", ["New", "Resale"])
locality = st.selectbox("Locality", ["Andheri West", "Borivali West", "Other"])
region = st.selectbox("Region", ["Western Suburbs", "Navi Mumbai", "Other"])


area_per_bhk = area / bhk if bhk != 0 else 0

locality_map = {"Andheri West": 1500, "Borivali West": 1200, "Other": 100}
region_map = {"Western Suburbs": 5000, "Navi Mumbai": 3000, "Other": 500}

if st.button("Predict Price"):

    input_data = pd.DataFrame(columns=columns)
    input_data.loc[0] = 0

    input_data["bhk"] = bhk
    input_data["area"] = area
    input_data["area_per_bhk"] = area_per_bhk

    input_data["locality_freq"] = locality_map[locality]
    input_data["region_freq"] = region_map[region]

    if type_option == "Villa":
        input_data["type_Villa"] = 1
    elif type_option == "Studio Apartment":
        input_data["type_Studio Apartment"] = 1
    elif type_option == "Penthouse":
        input_data["type_Penthouse"] = 1
    elif type_option == "Independent House":
        input_data["type_Independent House"] = 1

    if status_option == "Under Construction":
        input_data["status_Under Construction"] = 1

    if age_option == "Resale":
        input_data["age_Resale"] = 1
    elif age_option == "Unknown":
        input_data["age_Unknown"] = 1

    if area < 600:
        pass  # small (baseline)
    elif area < 1200:
        input_data.loc[0, "size_category_medium"] = 1
    elif area < 2000:
        input_data.loc[0, "size_category_large"] = 1
    else:
        input_data.loc[0, "size_category_luxury"] = 1

    prediction = model.predict(input_data)

    price = prediction[0]

    st.success(f"Estimated Price: Rs {price:.2f} lakh.")
