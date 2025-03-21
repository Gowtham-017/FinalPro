import json
import os
import streamlit as st
import pandas as pd
import random
script_dir = os.path.dirname(os.path.abspath(__file__))
st.markdown("<h1 style='text-align: center;'>🍽️ Your Weekly Meal Plan</h1>", unsafe_allow_html=True)
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = "demo_user" 
username = st.session_state["logged_in_user"]
@st.cache_data
def load_food_data():
    df = pd.read_excel("pages/food_data.xlsx")
    required_columns = ["foodname", "classification", "type"]
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Missing column: {col}")
            st.stop()
    return df
food_data = load_food_data()
if "logged_in_user" not in st.session_state:
    st.error("🚨 Please log in first!")
    st.stop()
username = st.session_state["logged_in_user"]
storage_file = os.path.join(script_dir, "storage.json")
if not os.path.exists(storage_file):
    st.error("⚠️ No health data found! Please enter your details on the Diet Recommendation page.")
    st.stop()
with open(storage_file, "r") as f:
    storage = json.load(f)
if username not in storage:
    st.error("⚠️ No health data found! Please enter your details on the Diet Recommendation page.")
    st.stop()
user_data = storage[username]
feedback_list = user_data.get("feedback", [])
show_reminder = False
reminder_message = ""
personalized_data = food_data.copy()
if feedback_list:
    latest_feedback = feedback_list[-1]
    bloating_detected = any(
        meal_feedback["issues"] == "Bloating"
        for meal_feedback in latest_feedback["meals"].values()
    )
    low_energy_detected = latest_feedback["energy_level"] < 5
    hydration_low = latest_feedback["hydration"] == "<1L"
    low_satisfaction = any(meal["satisfaction"] < 3 for meal in latest_feedback["meals"].values())
    frequent_cravings = latest_feedback.get("cravings", "None") != "None"
    poor_sleep = latest_feedback.get("sleep_quality", "Good") in ["Poor", "Very Poor"]
    digestive_issues = any(
        meal_feedback["issues"] in ["Indigestion", "Acidity", "Stomach Pain"]
        for meal_feedback in latest_feedback["meals"].values()
    )
    if bloating_detected:
        show_reminder = True
        reminder_message += "⚠️ You reported bloating. Light, easy-to-digest meals recommended.\n\n"
        personalized_data = personalized_data[
            personalized_data["classification"].isin(["Liquid", "Fruit", "Salad"])
        ]
    if low_energy_detected:
        show_reminder = True
        reminder_message += "⚡ Low energy detected. High-protein and iron-rich meals suggested.\n\n"
        personalized_data = personalized_data[
            personalized_data["classification"].isin(["Protein", "Iron-rich"])
        ]
    if hydration_low:
        show_reminder = True
        reminder_message += "💧 Hydration was low. Recommended hydrating foods and liquids.\n\n"
        personalized_data = personalized_data[
            personalized_data["classification"].isin(["Liquid", "Fruit", "Salad"])
        ]
    if low_satisfaction:
        show_reminder = True
        reminder_message += "😞 You reported low meal satisfaction. Adjusting flavors and variety.\n\n"
    if frequent_cravings:
        show_reminder = True
        reminder_message += "🍫 You reported frequent cravings. Including more satiating foods.\n\n"
    if poor_sleep:
        show_reminder = True
        reminder_message += "🌙 Poor sleep detected. Suggesting relaxing, magnesium-rich foods.\n\n"
        personalized_data = personalized_data[
            personalized_data["classification"].isin(["Nuts", "Seeds", "Herbal Tea"])
        ]
    if digestive_issues:
        show_reminder = True
        reminder_message += "🤕 Digestive issues reported. Avoiding high-fiber/spicy foods.\n\n"
        personalized_data = personalized_data[
            ~personalized_data["classification"].isin(["Spicy", "High-Fiber"])
        ]
if show_reminder:
    st.warning(reminder_message)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
preference = st.selectbox(
    "Select Your Meal Preference",
    [
        "Default Plan (Mixed)",
        "Prefer Tiffin All Day",
        "Prefer Dishes All Day",
        "Tiffin Morning & Dinner, Dishes Lunch",
        "Veg Only",
        "Non-Veg Only",
        "Veg/Non-Veg Mix"
    ]
)
if preference == "Veg Only":
    filtered_data = food_data[food_data["type"] == "Veg"]
elif preference == "Non-Veg Only":
    filtered_data = food_data[food_data["type"] == "Non-Veg"]
else:
    filtered_data = food_data.copy()
def get_items(df, classification, meal_type):
    items = df[(df["classification"] == classification) & (df["type"] == meal_type)]["foodname"].tolist()
    return items if items else []
def assign_day_types(preference):
    day_types = {}
    if preference == "Veg Only":
        day_types = {day: "Veg" for day in days}
    elif preference == "Non-Veg Only":
        day_types = {day: "Non-Veg" for day in days}
    else:
        veg_days_count = random.randint(3, 5)  
        veg_days = random.sample(days, veg_days_count)
        for day in days:
            day_types[day] = "Veg" if day in veg_days else "Non-Veg"
    return day_types
day_types = assign_day_types(preference)
# --- Meal Plan Generation ---
meal_plan = []
for day in days:
    breakfast = []
    lunch = []
    dinner = []
    meal_type = day_types[day]
    tiffins = get_items(filtered_data, "Tiffin", meal_type)
    main_dishes = get_items(filtered_data, "Main Dish", meal_type)
    side_dishes = get_items(filtered_data, "Side Dish", meal_type)
    gravies = get_items(filtered_data, "Gravy", meal_type)
    snacks = get_items(filtered_data, "Snack", meal_type)
    liquids = get_items(filtered_data, "Liquid", meal_type)

    # --- Preferences ---
    if preference == "Prefer Tiffin All Day":
        breakfast = random.sample(tiffins, min(1, len(tiffins))) + random.sample(snacks + liquids, min(1, len(snacks + liquids)))
        lunch = random.sample(tiffins, min(1, len(tiffins))) + random.sample(snacks + liquids, min(1, len(snacks + liquids)))
        dinner = random.sample(tiffins, min(1, len(tiffins))) + random.sample(snacks + liquids, min(1, len(snacks + liquids)))
    elif preference == "Prefer Dishes All Day":
        breakfast = (
            random.sample(main_dishes, min(1, len(main_dishes))) +
            random.sample(side_dishes, min(1, len(side_dishes))) +
            random.sample(gravies, min(1, len(gravies))) +
            random.sample(snacks + liquids, min(1, len(snacks + liquids)))
        )
        lunch = (
            random.sample(main_dishes, min(1, len(main_dishes))) +
            random.sample(side_dishes, min(1, len(side_dishes))) +
            random.sample(gravies, min(1, len(gravies))) +
            random.sample(snacks + liquids, min(1, len(snacks + liquids)))
        )
        dinner = (
            random.sample(main_dishes, min(1, len(main_dishes))) +
            random.sample(side_dishes, min(1, len(side_dishes))) +
            random.sample(gravies, min(1, len(gravies))) +
            random.sample(snacks + liquids, min(1, len(snacks + liquids)))
        )
    elif preference == "Tiffin Morning & Dinner, Dishes Lunch":
        breakfast = random.sample(tiffins, min(1, len(tiffins))) + random.sample(snacks + liquids, min(1, len(snacks + liquids)))
        lunch = (
            random.sample(main_dishes, min(1, len(main_dishes))) +
            random.sample(side_dishes, min(1, len(side_dishes))) +
            random.sample(gravies, min(1, len(gravies))) +
            random.sample(snacks + liquids, min(1, len(snacks + liquids)))
        )
        dinner = random.sample(tiffins, min(1, len(tiffins))) + random.sample(snacks + liquids, min(1, len(snacks + liquids)))
    elif preference in ["Veg Only", "Non-Veg Only", "Veg/Non-Veg Mix", "Default Plan (Mixed)"]:
        breakfast = random.sample(tiffins, min(1, len(tiffins))) + random.sample(snacks + liquids, min(1, len(snacks + liquids)))
        lunch = (
            random.sample(main_dishes, min(1, len(main_dishes))) +
            random.sample(side_dishes, min(1, len(side_dishes))) +
            random.sample(gravies, min(1, len(gravies))) +
            random.sample(snacks + liquids, min(1, len(snacks + liquids)))
        )
        dinner = random.sample(tiffins, min(1, len(tiffins))) + random.sample(snacks + liquids, min(1, len(snacks + liquids)))
    else:
        st.warning("No valid preference selected.")
    meal_plan.append({
        "Day": f"{day} ({meal_type})",
        "Breakfast": ", ".join(breakfast) if breakfast else "No items",
        "Lunch": ", ".join(lunch) if lunch else "No items",
        "Dinner": ", ".join(dinner) if dinner else "No items"
    })
st.subheader("📋 Your Weekly Meal Plan")
st.table(meal_plan)
if st.button("🔄 Refresh Meal Plan"):
    st.rerun()
st.success("✅ Meal plan ready! 🍽️")