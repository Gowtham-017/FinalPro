import streamlit as st
import json
import os
st.title("User Profile")
if "logged_in_user" not in st.session_state:
    st.error("Please log in first!")
    st.stop()
username = st.session_state["logged_in_user"]
if not os.path.exists("storage.json"):
    st.error("No health data found! Please enter your details first.")
    st.stop()
with open("storage.json", "r") as f:
    storage = json.load(f)
if username not in storage:
    st.error("No health data found! Please enter your details first.")
    st.stop()
data = storage[username]
if st.button("Update Health Data"):
    st.session_state["updating_profile"] = True 
    st.switch_page("pages/HealthData.py")
st.subheader("Basic Information")
st.write(f"**Age:** {data['age']} years")
st.write(f"**Height:** {data['height']} cm")
st.write(f"**Weight:** {data['weight']} kg")
st.write(f"**Gender:** {data['gender']}")