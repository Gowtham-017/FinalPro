# import streamlit as st
# import json
# import os

# st.title("Health Data Form")
# # Determine if user is signing up or updating data
# if "new_user_signup" in st.session_state:
#     username = st.session_state["new_user_signup"]
#     new_user = True
# elif "logged_in_user" in st.session_state:
#     username = st.session_state["logged_in_user"]
#     new_user = False
# else:
#     st.error("Unauthorized access. Please sign up or log in first.")
#     st.stop()

# # Load or create storage.json
# if not os.path.exists("storage.json"):
#     with open("storage.json", "w") as f:
#         json.dump({}, f)

# with open("storage.json", "r", encoding="utf-8") as f:
#     storage = json.load(f)

# # Prefill form if user already exists
# user_data = storage.get(username, {})

# age = st.number_input("Age", min_value=2, max_value=120, step=1, value=user_data.get("age", 25))
# height = st.number_input("Height (cm)", min_value=50, max_value=300, step=1, value=user_data.get("height", 170))
# weight = st.number_input("Weight (kg)", min_value=10, max_value=300, step=1, value=user_data.get("weight", 70))
# gender = st.radio("Gender", ("Male", "Female"), index=0 if user_data.get("gender", "Male") == "Male" else 1)
# activity = st.select_slider(
#     "Activity Level",
#     options=["Little/no exercise", "Light exercise", "Moderate", "Very active", "Extra active"],
#     value=user_data.get("activity", "Moderate"),
# )

# # Medical History
# st.subheader("Medical History")

# # Most Common Medical Conditions
# common_conditions = [
#     "Diabetes", "Hypertension", "Heart Disease", "Asthma", 
#     "Kidney Disease", "Liver Disease", "Thyroid Disorder", 
#     "High Cholesterol", "Obesity", "Anemia"
# ]

# # Store user's medical history
# medical_history = {}

# # Create checkboxes dynamically
# for condition in common_conditions:
#     medical_history[condition] = st.checkbox(
#         condition, value=user_data.get("medical_history", {}).get(condition, False)
#     )

# # Lifestyle Factors
# st.subheader("Lifestyle Factors")

# # Lifestyle checkboxes
# lifestyle_factors = {
#     "smoking": st.checkbox("Do you smoke?", value=user_data.get("lifestyle", {}).get("smoking", False)),
#     "alcohol": st.checkbox("Do you consume alcohol?", value=user_data.get("lifestyle", {}).get("alcohol", False)),
#     "exercise": st.checkbox("Do you exercise regularly?", value=user_data.get("lifestyle", {}).get("exercise", False)),
#     "sleep_quality": st.checkbox("Do you have poor sleep quality?", value=user_data.get("lifestyle", {}).get("sleep_quality", False)),
#     "stress": st.checkbox("Do you experience high stress levels?", value=user_data.get("lifestyle", {}).get("stress", False)),
#     "hydration": st.checkbox("Do you drink less than 2 liters of water daily?", value=user_data.get("lifestyle", {}).get("hydration", False)),
#     "junk_food": st.checkbox("Do you frequently consume junk/processed food?", value=user_data.get("lifestyle", {}).get("junk_food", False)),
#     "meal_skipping": st.checkbox("Do you frequently skip meals?", value=user_data.get("lifestyle", {}).get("meal_skipping", False))
# }



# exercise = st.selectbox(
#     "Exercise Level", ["None", "Light", "Moderate", "Intense"], 
#     index=["None", "Light", "Moderate", "Intense"].index(user_data.get("lifestyle", {}).get("exercise", "Moderate"))
# )
# sleep = st.slider("Average Sleep Hours per Night", 0, 12, value=user_data.get("lifestyle", {}).get("sleep", 7))
# stress = st.selectbox("Stress Level", ["Low", "Moderate", "High"], 
#                     index=["Low", "Moderate", "High"].index(user_data.get("lifestyle", {}).get("stress", "Moderate")))




# st.subheader("Medical History & Current Health Status")

# # Current Symptoms (Multi-select instead of typing)
# common_symptoms = [
#     "Fatigue", "Headache", "Dizziness", "Nausea", "Shortness of breath",
#     "Joint Pain", "Chest Pain", "Indigestion", "Skin Rash", "Blurred Vision"
# ]
# selected_symptoms = st.multiselect(
#     "Are you experiencing any symptoms currently?", 
#     options=common_symptoms, 
#     default=user_data.get("current_symptoms", [])
# )

# # Recent Lab Tests (Dropdown instead of free text)
# common_lab_tests = [
#     "Blood Sugar Test", "Cholesterol Test", "Thyroid Test", 
#     "Hemoglobin (Hb) Test", "Liver Function Test", "Kidney Function Test"
# ]
# selected_lab_tests = st.multiselect(
#     "Recent Lab Tests Done (if any)", 
#     options=common_lab_tests, 
#     default=user_data.get("recent_lab_tests", [])
# )

# # Conditional input: If user selects lab tests, ask for results
# lab_results = {}
# if selected_lab_tests:
#     st.subheader("Enter Lab Test Results")
#     for test in selected_lab_tests:
#         lab_results[test] = st.text_input(f"{test} Result", value=user_data.get("lab_results", {}).get(test, ""))

# # Food Allergies (Multi-Select + Manual Input)
# common_allergies = ["Dairy", "Gluten", "Nuts", "Seafood", "Eggs", "Soy"]
# selected_allergies = st.multiselect(
#     "Known Food Allergies (if any)", 
#     options=common_allergies, 
#     default=user_data.get("food_allergies", [])
# )
# custom_allergy = st.text_input("Other Allergy (if not listed)", "")
# if custom_allergy:
#     selected_allergies.append(custom_allergy)

# # Dietary Preferences (Dropdown)
# dietary_preferences = st.selectbox(
#     "Select Your Dietary Preference", 
#     ["No Preference", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb", "Other"],
#     index=0 if "dietary_preferences" not in user_data else 
#         ["No Preference", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb", "Other"].index(user_data["dietary_preferences"])
# )

# # Doctor’s Recommendations (Radio Button instead of free text)
# st.subheader("Doctor’s Recommendations")
# doctor_recommendations = st.radio(
#     "Did your doctor recommend any lifestyle changes?", 
#     ["None", "Increase Physical Activity", "Reduce Salt Intake", "Follow a Specific Diet", "Manage Stress"], 
#     index=0
# )

# # Appointment Date
# appointment_date = st.date_input(
#     "Next Appointment Date", 
#     value=user_data.get("appointment_date", None)
# )


# # Store Data and Redirect
# if st.button("Submit"):
#     storage[username] = {
#         "age": age,
#         "height": height,
#         "weight": weight,
#         "gender": gender,
#         "activity": activity,
#         "medical_history": medical_history,
#         "lifestyle": {
#             "smoking": smoking,
#             "alcohol": alcohol,
#             "exercise": exercise,
#             "sleep": sleep,
#             "stress": stress,
#         },
#         "medications": [med.strip() for med in medications.split(",")] if medications else [],
#         "doctors_notes": doctors_notes,
#     }

#     with open("storage.json", "w") as f:
#         json.dump(storage, f)

#     # Redirect logic
#     if new_user:
#         del st.session_state["new_user_signup"]
#         st.success("Data saved successfully! Redirecting to Login...")
#         st.switch_page("App.py")  # Redirect to login (new user flow)
#     else:
#         st.success("Health data updated successfully! Returning to previous page...")

#         # Redirect back to App.py (where the sidebar and everything is present)
#         st.switch_page("App.py")


import streamlit as st
import json
import datetime
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

# Basic Details
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
medical_history = {condition: st.checkbox(condition, value=user_data.get("medical_history", {}).get(condition, False)) for condition in common_conditions}

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

common_symptoms = ["Fatigue", "Headache", "Dizziness", "Nausea", "Shortness of breath",
                    "Joint Pain", "Chest Pain", "Indigestion", "Skin Rash", "Blurred Vision"]
selected_symptoms = st.multiselect("Are you experiencing any symptoms currently?", options=common_symptoms, default=user_data.get("current_symptoms", []))

common_lab_tests = ["Blood Sugar Test", "Cholesterol Test", "Thyroid Test", "Hemoglobin (Hb) Test", 
                    "Liver Function Test", "Kidney Function Test"]
selected_lab_tests = st.multiselect("Recent Lab Tests Done (if any)", options=common_lab_tests, default=user_data.get("recent_lab_tests", []))

# Conditional input: If user selects lab tests, ask for results
lab_results = {}
if selected_lab_tests:
    st.subheader("Enter Lab Test Results")
    for test in selected_lab_tests:
        lab_results[test] = st.text_input(f"{test} Result", value=user_data.get("lab_results", {}).get(test, ""))

# Food Allergies & Dietary Preferences
common_allergies = ["Dairy", "Gluten", "Nuts", "Seafood", "Eggs", "Soy"]
selected_allergies = st.multiselect("Known Food Allergies (if any)", options=common_allergies, default=user_data.get("food_allergies", []))
custom_allergy = st.text_input("Other Allergy (if not listed)", "")
if custom_allergy:
    selected_allergies.append(custom_allergy)

dietary_preferences = st.selectbox("Select Your Dietary Preference", 
                                ["No Preference", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb", "Other"],
                                index=0 if "dietary_preferences" not in user_data else 
                                ["No Preference", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb", "Other"].index(user_data["dietary_preferences"]))

# Doctor’s Recommendations & Appointment Date
st.subheader("Doctor’s Recommendations")
doctor_recommendations = st.radio("Did your doctor recommend any lifestyle changes?", 
                                ["None", "Increase Physical Activity", "Reduce Salt Intake", "Follow a Specific Diet", "Manage Stress"], 
                                index=0)

# Convert stored date string to datetime.date before using it in st.date_input
stored_date = user_data.get("appointment_date", None)
if isinstance(stored_date, str):
    stored_date = datetime.datetime.strptime(stored_date, "%Y-%m-%d").date()  # Convert string to date object

# Display date input field with corrected value
appointment_date = st.date_input("Next Appointment Date", value=stored_date)

# Store Data
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
        "current_symptoms": selected_symptoms,
        "recent_lab_tests": selected_lab_tests,
        "lab_results": lab_results,
        "food_allergies": selected_allergies,
        "dietary_preferences": dietary_preferences,
        "doctor_recommendations": doctor_recommendations,
        "appointment_date": str(appointment_date)  # Convert to string to avoid JSON serialization issues
    }

    with open("storage.json", "w") as f:
        json.dump(storage, f, indent=4)

    # Redirect Logic
    if new_user:
        del st.session_state["new_user_signup"]
        st.success("Data saved successfully! Redirecting to Login...")
        st.switch_page("App.py")  # Redirect to login (new user flow)
    else:
        st.success("Health data updated successfully! Returning to previous page...")
        st.switch_page("App.py")  # Redirect back to main app
