import streamlit as st
import json
import datetime
import os
import time
st.title("Health Data Form")
if "new_user_signup" in st.session_state:
    username = st.session_state["new_user_signup"]
    new_user = True
elif "logged_in_user" in st.session_state:
    username = st.session_state["logged_in_user"]
    new_user = False
else:
    st.error("Unauthorized access. Please sign up or log in first.")
    st.stop()
if not os.path.exists("storage.json"):
    with open("storage.json", "w") as f:
        json.dump({}, f)
with open("storage.json", "r", encoding="utf-8") as f:
    storage = json.load(f)
user_data = storage.get(username, {})
age = st.number_input("Age", min_value=2, max_value=120, step=1, value=user_data.get("age", 25))
height = st.number_input("Height (cm)", min_value=50, max_value=300, step=1, value=user_data.get("height", 170))
weight = st.number_input("Weight (kg)", min_value=10, max_value=300, step=1, value=user_data.get("weight", 70))
gender = st.radio("Gender", ("Male", "Female"), index=0 if user_data.get("gender", "Male") == "Male" else 1)
activity = st.select_slider(
    "Activity Level",
    options=["Little/no exercise", "Light exercise", "Moderate", "Very active", "Extra active"],
    value=user_data.get("activity", "Moderate"),
)
bmi = round(weight / ((height / 100) ** 2), 2)
# Medical History
st.subheader("Medical History")
common_conditions = [
    "Diabetes", "Hypertension", "Heart Disease", "Asthma", 
    "Kidney Disease", "Liver Disease", "Thyroid Disorder", 
    "High Cholesterol", "Obesity", "Anemia"
]
medical_history = {
    condition: st.checkbox(condition, value=user_data.get("medical_history", {}).get(condition, False)) 
    for condition in common_conditions
}
# Lifestyle Factors
st.subheader("Lifestyle Factors")
lifestyle_factors = {
    "sleep": st.slider("Average Sleep Hours per Night", 0, 12, value=user_data.get("lifestyle", {}).get("sleep", 7)),
    "stress": st.selectbox("Stress Level", ["Low", "Moderate", "High"], 
                            index=["Low", "Moderate", "High"].index(user_data.get("lifestyle", {}).get("stress", "Moderate"))),
    "smoking": st.checkbox("Do you smoke?", value=user_data.get("lifestyle", {}).get("smoking", False)),
    "alcohol": st.checkbox("Do you consume alcohol?", value=user_data.get("lifestyle", {}).get("alcohol", False)),
    "hydration": st.checkbox("Do you drink less than 2 liters of water daily?", value=user_data.get("lifestyle", {}).get("hydration", False)),
    "junk_food": st.checkbox("Do you frequently consume junk/processed food?", value=user_data.get("lifestyle", {}).get("junk_food", False)),
    "meal_skipping": st.checkbox("Do you frequently skip meals?", value=user_data.get("lifestyle", {}).get("meal_skipping", False)),
    "exercise": st.selectbox("Exercise Level", ["None", "Light", "Moderate", "Intense"], 
                            index=["None", "Light", "Moderate", "Intense"].index(user_data.get("lifestyle", {}).get("exercise", "Moderate"))),
}
# Medical Symptoms & Tests
st.subheader("Medical History & Current Health Status")
common_symptoms = [
    "Fatigue", "Headache", "Dizziness", "Nausea", "Shortness of breath",
    "Joint Pain", "Chest Pain", "Indigestion", "Skin Rash", "Blurred Vision"
]
st.markdown("#### Current Symptoms with Severity")
current_symptoms = {}
previous_symptoms = user_data.get("current_symptoms", {})
for symptom in common_symptoms:
    previously_selected = symptom in previous_symptoms
    selected = st.checkbox(symptom, value=previously_selected)
    if selected:
        previous_level = previous_symptoms.get(symptom, "Mild")
        level = st.selectbox(
            f"{symptom} Severity Level", 
            ["Mild", "Moderate", "Severe"], 
            index=["Mild", "Moderate", "Severe"].index(previous_level)
        )
        current_symptoms[symptom] = level
# Lab Tests
common_lab_tests = [
    "Blood Sugar Test", "Cholesterol Test", "Thyroid Test", 
    "Hemoglobin (Hb) Test", "Liver Function Test", "Kidney Function Test"
]
selected_lab_tests = st.multiselect(
    "Recent Lab Tests Done (if any)", 
    options=common_lab_tests, 
    default=user_data.get("recent_lab_tests", [])
)
lab_results = {}
if selected_lab_tests:
    st.subheader("Enter Lab Test Results")
    for test in selected_lab_tests:
        lab_results[test] = st.text_input(
            f"{test} Result", 
            value=user_data.get("lab_results", {}).get(test, "")
        )
# Food Allergies & Dietary Preferences
common_allergies = ["Dairy", "Meat", "Nuts", "Seafood", "Eggs", "Spices"]
selected_allergies = st.multiselect(
    "Known Food Allergies (if any)", 
    options=common_allergies, 
    default=user_data.get("food_allergies", [])
)
custom_allergy = st.text_input("Other Allergy (if not listed)", "")
if custom_allergy:
    selected_allergies.append(custom_allergy)
# Doctor’s Recommendations
st.subheader("📋 Doctor’s Recommendations")
recommendation_options = [
    "Increase Physical Activity",
    "Follow a balanced, nutritious diet",
    "Exercise regularly, at least 30 minutes a day",
    "Reduce salt and sugar intake",
    "Monitor blood pressure regularly",
    "Take prescribed medications on time",
    "Quit smoking and avoid tobacco products",
    "Limit alcohol consumption",
    "Practice stress management techniques",
    "Stay hydrated with adequate water intake",
    "Get 7-8 hours of quality sleep each night",
    "Maintain a healthy weight",
    "Schedule regular health check-ups",
    "Follow a heart-healthy diet",
    "Include more fiber in daily meals",
    "Avoid processed and junk foods"
]
saved_recommendations = user_data.get("doctor_recommendations", [])
valid_defaults = [rec for rec in saved_recommendations if rec in recommendation_options]
doctor_recommendations = st.multiselect(
    "Did your doctor recommend any lifestyle changes or treatments?", 
    recommendation_options,
    default=valid_defaults
)
if st.button("Submit"):
    storage[username] = {
        "age": age,
        "height": height,
        "weight": weight,
        "gender": gender,
        "bmi": bmi,
        "activity": activity,
        "medical_history": medical_history,
        "lifestyle": lifestyle_factors,
        "current_symptoms": current_symptoms, 
        "recent_lab_tests": selected_lab_tests,
        "lab_results": lab_results,
        "food_allergies": selected_allergies,
        "doctor_recommendations": doctor_recommendations
    }
    with open("storage.json", "w") as f:
        json.dump(storage, f, indent=4)
    with st.spinner("Uploading your health data..."):
        progress_bar = st.progress(0)
        for percent_complete in range(101):
            time.sleep(0.01) 
            progress_bar.progress(percent_complete)
        time.sleep(1)
    st.success("✅ Health data submitted successfully!")
    if new_user:
        st.success("Data saved successfully! Redirecting to Login...")
        time.sleep(1.5)
        st.switch_page("App.py")  
    else:
        st.success("Health data updated successfully! Returning to previous page...")
        time.sleep(1.5)
        st.switch_page("App.py")  