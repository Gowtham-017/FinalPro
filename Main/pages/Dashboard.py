import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Check if user is logged in
if "logged_in_user" not in st.session_state:
    st.error("Please log in first!")
    st.stop()

username = st.session_state["logged_in_user"]

# Load storage.json
if not os.path.exists("storage.json"):
    st.error("No health data found! Please enter your details on the Diet Recommendation page.")
    st.stop()

with open("storage.json", "r") as f:
    storage = json.load(f)

if username not in storage:
    st.error("No health data found! Please enter your details on the Diet Recommendation page.")
    st.stop()

data = storage[username]

# **BMI Calculation**
bmi = round(data["weight"] / ((data["height"] / 100) ** 2), 2)
bmi_category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"

st.subheader("BMI Analysis")
bmi_category_text = f"<p style='font-size: 30px; font-weight: bold; color: {'green' if bmi_category == 'Normal' else 'red'};'> {bmi_category} </p>"
st.markdown(bmi_category_text, unsafe_allow_html=True)

# **BMI Analysis - Horizontal Bar Chart**
bmi_data = pd.DataFrame({
    "Category": ["Underweight", "Normal", "Overweight", "Obese"],
    "Threshold": [18.5, 25, 30, 40],
    "BMI Value": [bmi, bmi, bmi, bmi],
})

fig_bmi_bar = px.bar(
    bmi_data,
    x="BMI Value",
    y="Category",
    orientation="h",
    color="Category",
    title="BMI Analysis",
    labels={"BMI Value": "BMI (kg/m²)", "Category": "BMI Category"},
    color_discrete_sequence=px.colors.qualitative.Set2,
)

fig_bmi_bar.add_vline(
    x=bmi,
    line=dict(color="black", width=2, dash="dash"),
    annotation_text=f"BMI: {bmi} ({bmi_category})",
    annotation_position="top right",
)

st.plotly_chart(fig_bmi_bar, use_container_width=True)

# **Medical History**
st.subheader("Medical History")
history_df = pd.DataFrame(data["medical_history"].items(), columns=["Condition", "Present"])
history_df["Present"] = history_df["Present"].apply(lambda x: "✅ Yes" if x else "❌ No")
st.dataframe(history_df, height=200, width=500)

# **Lifestyle Breakdown - Donut Chart**
st.subheader("Lifestyle Breakdown")
lifestyle_labels = ["Smoking", "Alcohol", "Exercise", "Sleep", "Stress"]
lifestyle_values = [
    1 if data["lifestyle"]["smoking"] else 0,
    1 if data["lifestyle"]["alcohol"] else 0,
    {"None": 0, "Light": 1, "Moderate": 2, "Intense": 3}[data["lifestyle"]["exercise"]],
    data["lifestyle"]["sleep"],
    {"Low": 1, "Moderate": 2, "High": 3}[data["lifestyle"]["stress"]],
]

fig_lifestyle = px.pie(
    names=lifestyle_labels,
    values=lifestyle_values,
    hole=0.4,
    title="Lifestyle Factors",
    color_discrete_sequence=px.colors.qualitative.Set3,
)

st.plotly_chart(fig_lifestyle, use_container_width=True)

# **Medications**
st.subheader("Prescribed Medications")
if data["medications"]:
    st.write(", ".join(data["medications"]))
else:
    st.write("No medications prescribed.")

# **Doctor’s Notes & Appointments**
st.subheader("Doctor's Notes & Appointments")
st.info(data["doctors_notes"] if data["doctors_notes"] else "No notes available.")