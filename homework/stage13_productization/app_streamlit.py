# app_streamlit.py

import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# --- Page Setup ---
st.set_page_config(page_title="Model Prediction Dashboard", layout="wide")
st.title("Simple Model Prediction Dashboard")
st.write("This dashboard allows you to make predictions using a trained model.")

# --- Load Model ---
MODEL_PATH = 'model/model.pkl'
model = None

# Load the pickled model with error handling
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        st.error(f"Error loading the model: {e}")
else:
    st.error(f"Model file not found at '{MODEL_PATH}'. Please train and save the model first.")

# --- Sidebar for User Input ---
st.sidebar.header("Input Features")
st.sidebar.write("Enter values for the model to predict.")

# Disable inputs if the model fails to load
disable_inputs = model is None

try:
    feature1 = st.sidebar.number_input("Enter Feature 1", value=1.5, format="%.2f", disabled=disable_inputs)
    feature2 = st.sidebar.number_input("Enter Feature 2", value=2.5, format="%.2f", disabled=disable_inputs)
except Exception as e:
    st.sidebar.error(f"Invalid input. Please enter valid numbers. Error: {e}")
    disable_inputs = True

# --- Prediction and Results ---
if not disable_inputs:
    st.subheader("Prediction")

    if st.button("Get Prediction"):
        try:
            # Format features for the model (2D array)
            features = np.array([[feature1, feature2]])
            
            # Predict using the loaded model
            prediction = model.predict(features)
            
            st.metric(label="Predicted Value", value=f"{prediction[0]:.4f}")
            st.success("Prediction successful!")
            
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
else:
    st.warning("Prediction is disabled because the model could not be loaded.")

# --- Bonus: Sample Data Visualization ---
st.subheader("Sample Data Visualization")
st.write("This is a simple chart displaying some sample data.")

# Create and display sample data
sample_data = pd.DataFrame({
    'x': np.arange(10),
    'y': np.random.randn(10).cumsum()
})

st.line_chart(sample_data)
st.dataframe(sample_data)