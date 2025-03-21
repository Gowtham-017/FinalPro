import streamlit as st
import json
import os
st.set_page_config(page_title="Intermediary Storage", page_icon="📂", layout="wide")
st.title("Intermediary Storage")
STORAGE_FILE = "storage.json"
def load_data():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as file:
            return json.load(file)
    return {}
def save_data(data):
    with open(STORAGE_FILE, "w") as file:
        json.dump(data, file, indent=4)
stored_data = load_data()
if "user_data" in st.session_state:
    st.write("✅ New user data received from DietRecommendation Page!")
    stored_data = st.session_state["user_data"]
    save_data(stored_data)
    st.success("Data successfully saved to storage.json!")
st.subheader("Stored User Data")
st.json(stored_data)