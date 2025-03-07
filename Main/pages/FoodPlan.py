import streamlit as st
import pandas as pd
import json
import os
import random

st.markdown("<h1 style='text-align: center;'>Your Weekly Meal Plan 🍽️</h1>", unsafe_allow_html=True)

# Ensure storage.json exists
if not os.path.exists("storage.json"):
    with open("storage.json", "w") as f:
        json.dump({}, f)

# Check if a user is logged in
if "logged_in_user" not in st.session_state:
    st.error("Unauthorized access! Please log in first.")
    st.stop()

username = st.session_state["logged_in_user"]

# Load user data from storage.json
with open("storage.json", "r") as f:
    storage_data = json.load(f)

# Ensure user data exists
if username not in storage_data:
    st.error("No user data found! Please enter your details on the main page first.")
    st.stop()

# Retrieve the user's stored health data
user_data = storage_data[username]

# Load food data from an Excel file
@st.cache_data
def load_food_data():
    return pd.read_excel("pages/food_data.xlsx")

food_data = load_food_data()

# Function to classify meals based on user's health condition and food suitability
def classify_meals(meal_type):
    meal_options = food_data.copy()

    # Meal type-based classification
    if meal_type == "Breakfast":
        meal_options = meal_options[(meal_options['calories'] >= 200) & (meal_options['protein'] >= 8)]  # Heavy foods
    elif meal_type == "Lunch":
        meal_options = meal_options[(meal_options['calories'] >= 250) & (meal_options['protein'] >= 10) & (meal_options['fat'] >= 5)]
    elif meal_type == "Dinner":
        meal_options = meal_options[(meal_options['calories'] <= 200) & (meal_options['fat'] <= 8)]  # Light foods

    # Filter based on dietary preferences
    if "lifestyle" in user_data and "diet" in user_data["lifestyle"]:
        if user_data["lifestyle"]["diet"] == "Vegetarian":
            meal_options = meal_options[meal_options['foodname'].isin(['Lentils', 'Quinoa', 'Tofu', 'Chickpeas'])]
        elif user_data["lifestyle"]["diet"] == "Keto":
            meal_options = meal_options[(meal_options['fat'] >= 10) & (meal_options['carbs'] <= 10)]

    # Filter based on health conditions
    if "medical_history" in user_data:
        if user_data["medical_history"].get("Diabetes", False):
            meal_options = meal_options[meal_options['glycemic_index'] <= 55]  # Low GI foods
        if user_data["medical_history"].get("Hypertension", False):
            meal_options = meal_options[meal_options['fat'] <= 140]  # Low sodium foods

    # Select random meals to add variety
    meal_list = list(meal_options['foodname'])
    
    if not meal_list:  # If the filtered list is empty, provide default options
        meal_list = ["Default Meal 1", "Default Meal 2", "Default Meal 3"]

    return random.sample(meal_list, min(3, len(meal_list)))

# Days of the week
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Function to generate the meal plan
def generate_meal_plan():
    return pd.DataFrame({
        "Day": days,
        "Breakfast (Heavy)": [", ".join(classify_meals("Breakfast")) for _ in days],
        "Lunch (Balanced)": [", ".join(classify_meals("Lunch")) for _ in days],
        "Dinner (Light)": [", ".join(classify_meals("Dinner")) for _ in days],
    })

# Check if a meal plan exists in session state, otherwise generate one
if "meal_plan" not in st.session_state:
    st.session_state["meal_plan"] = generate_meal_plan()

# Display the meal plan
st.subheader("Your Personalized Weekly Meal Plan")
st.dataframe(st.session_state["meal_plan"], width=1000)

# Refresh Button
if st.button("Refresh Meal Plan 🔄"):
    st.session_state["meal_plan"] = generate_meal_plan()
    st.rerun()

st.success("Your personalized weekly meal plan is ready! Enjoy your healthy meals! 🍽️")
