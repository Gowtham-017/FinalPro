import streamlit as st
import json
import os

# Set up the page
st.set_page_config(page_title="Intermediary Storage", page_icon="📂", layout="wide")
st.title("Intermediary Storage")

# Define storage file
STORAGE_FILE = "storage.json"

# Function to load stored data
def load_data():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save user data
def save_data(data):
    with open(STORAGE_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load existing data
stored_data = load_data()

# Check if new data is coming from DietRecommendation page
if "user_data" in st.session_state:
    st.write("✅ New user data received from DietRecommendation Page!")
    stored_data = st.session_state["user_data"]
    save_data(stored_data)
    st.success("Data successfully saved to storage.json!")

# Display stored data for debugging
st.subheader("Stored User Data")
st.json(stored_data)