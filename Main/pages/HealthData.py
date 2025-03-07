import streamlit as st
import json
import os

st.title("Health Data Form")

# Determine if user is signing up or updating data
if "new_user_signup" in st.session_state:
    username = st.session_state["new_user_signup"]
    new_user = True
elif "logged_in_user" in st.session_state:
    username = st.session_state["logged_in_user"]
    new_user = False
else:
    st.error("Unauthorized access. Please sign up or log in first.")
    st.stop()

# Load or create storage.json
if not os.path.exists("storage.json"):
    with open("storage.json", "w") as f:
        json.dump({}, f)

with open("storage.json", "r", encoding="utf-8") as f:
    storage = json.load(f)

# Prefill form if user already exists
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

# Medical History
st.subheader("Medical History")
medical_history = {
    "Diabetes": st.checkbox("Diabetes", value=user_data.get("medical_history", {}).get("Diabetes", False)),
    "Hypertension": st.checkbox("Hypertension", value=user_data.get("medical_history", {}).get("Hypertension", False)),
    "Heart Disease": st.checkbox("Heart Disease", value=user_data.get("medical_history", {}).get("Heart Disease", False)),
}

# Lifestyle Factors
st.subheader("Lifestyle Factors")
smoking = st.checkbox("Do you smoke?", value=user_data.get("lifestyle", {}).get("smoking", False))
alcohol = st.checkbox("Do you consume alcohol?", value=user_data.get("lifestyle", {}).get("alcohol", False))
exercise = st.selectbox(
    "Exercise Level", ["None", "Light", "Moderate", "Intense"], 
    index=["None", "Light", "Moderate", "Intense"].index(user_data.get("lifestyle", {}).get("exercise", "Moderate"))
)
sleep = st.slider("Average Sleep Hours per Night", 0, 12, value=user_data.get("lifestyle", {}).get("sleep", 7))
stress = st.selectbox("Stress Level", ["Low", "Moderate", "High"], 
                    index=["Low", "Moderate", "High"].index(user_data.get("lifestyle", {}).get("stress", "Moderate")))

# Prescribed Medications
st.subheader("Prescribed Medications")
medications = st.text_area("Enter medications (comma-separated, if any)", value=", ".join(user_data.get("medications", [])))

# Doctor's Notes
st.subheader("Doctor's Notes & Appointments")
doctors_notes = st.text_area("Enter doctor's notes (if any)", value=user_data.get("doctors_notes", ""))

# Store Data and Redirect
if st.button("Submit"):
    storage[username] = {
        "age": age,
        "height": height,
        "weight": weight,
        "gender": gender,
        "activity": activity,
        "medical_history": medical_history,
        "lifestyle": {
            "smoking": smoking,
            "alcohol": alcohol,
            "exercise": exercise,
            "sleep": sleep,
            "stress": stress,
        },
        "medications": [med.strip() for med in medications.split(",")] if medications else [],
        "doctors_notes": doctors_notes,
    }

    with open("storage.json", "w") as f:
        json.dump(storage, f)

    # Redirect logic
    if new_user:
        del st.session_state["new_user_signup"]
        st.success("Data saved successfully! Redirecting to Login...")
        st.switch_page("App.py")  # Redirect to login (new user flow)
    else:
        st.success("Health data updated successfully! Returning to previous page...")

        # Redirect back to App.py (where the sidebar and everything is present)
        st.switch_page("App.py")
