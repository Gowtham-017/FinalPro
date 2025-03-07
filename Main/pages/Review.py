import streamlit as st
import json
import os
import pandas as pd

st.markdown("<h1 style='text-align: center;'>🥗 Personalized Meal Planner Report 🍽️</h1>", unsafe_allow_html=True)

# Ensure storage.json exists
if not os.path.exists("storage.json"):
    with open("storage.json", "w") as f:
        json.dump({}, f)

# Check if a user is logged in
if "logged_in_user" not in st.session_state:
    st.error("❌ Unauthorized access! Please log in first.")
    st.stop()

username = st.session_state["logged_in_user"]

# Load user data from storage.json
with open("storage.json", "r") as f:
    storage_data = json.load(f)

# Ensure user data exists
if username not in storage_data:
    st.error("⚠ No user data found! Please enter your details on the main page first.")
    st.stop()

# Retrieve the user's stored health data
user_data = storage_data[username]

# Load food data from an Excel file
@st.cache_data
def load_food_data():
    return pd.read_excel("pages/food_data.xlsx")

food_data = load_food_data()

# Function to generate a personalized meal plan with insights
def generate_meal_plan(data):
    meal_plan = {}

    # ✅ Calculate BMI and categorize
    height_m = data["height"] / 100
    bmi = round(data["weight"] / (height_m ** 2), 2)

    if bmi < 18.5:
        bmi_category = "Underweight"
        meal_plan["calories"] = "Increase calorie intake (High protein, healthy fats)"
        dietary_advice = "Increase your calorie intake by consuming nutrient-dense foods like nuts, seeds, whole grains, and lean proteins."
    elif 18.5 <= bmi < 24.9:
        bmi_category = "Normal"
        meal_plan["calories"] = "Maintain balanced calorie intake"
        dietary_advice = "Maintain a balanced diet with a mix of proteins, healthy fats, and carbohydrates. Stay hydrated and exercise regularly."
    else:
        bmi_category = "Overweight"
        meal_plan["calories"] = "Lower calorie intake (High fiber, low-fat options)"
        dietary_advice = "Focus on high-fiber foods, lean proteins, and healthy fats. Reduce processed foods and refined sugars."

    meal_plan["bmi"] = bmi
    meal_plan["bmi_category"] = bmi_category
    meal_plan["dietary_advice"] = dietary_advice

    # ✅ Lifestyle-based dietary recommendations
    meal_plan["diet"] = "Balanced Diet"
    if "lifestyle" in data and "diet" in data["lifestyle"]:
        if data["lifestyle"]["diet"] == "Vegetarian":
            meal_plan["diet"] = "Vegetarian Diet"
            dietary_advice += " Include a variety of plant-based proteins like lentils, tofu, and quinoa."
        elif data["lifestyle"]["diet"] == "Keto":
            meal_plan["diet"] = "Keto Diet"
            dietary_advice += " Stick to high-fat, low-carb foods like avocados, nuts, and fatty fish."

    # ✅ Medical history-based adjustments
    medical_advice = []
    if "medical_history" in data:
        if data["medical_history"].get("Diabetes", False):
            meal_plan["diabetes"] = "Monitor carbohydrate intake. Choose whole grains and avoid refined sugar."
            medical_advice.append("For diabetes, opt for foods with a low glycemic index such as whole grains, legumes, and non-starchy vegetables.")

        if data["medical_history"].get("Hypertension", False):
            meal_plan["hypertension"] = "Limit sodium intake. Opt for lean meats, fruits, and vegetables."
            medical_advice.append("For hypertension, reduce salt intake and focus on potassium-rich foods like bananas, spinach, and beans.")

    # ✅ Suggested food selections
    suggested_foods = []
    if meal_plan["calories"] == "Increase calorie intake (High protein, healthy fats)":
        suggested_foods = ['Chicken Breast', 'Salmon', 'Avocado', 'Greek Yogurt', 'Brown Rice']
    elif meal_plan["calories"] == "Lower calorie intake (High fiber, low-fat options)":
        suggested_foods = ['Broccoli', 'Greek Yogurt', 'Spinach', 'Oatmeal', 'Lentils']
    else:
        suggested_foods = ['Chicken Breast', 'Quinoa', 'Greek Yogurt', 'Broccoli', 'Sweet Potatoes']

    # Check if 'foodname' column exists in the food data
    if 'foodname' in food_data.columns:
        selected_foods = food_data[food_data['foodname'].isin(suggested_foods)]
    else:
        st.error("⚠ Column 'foodname' not found in the food data!")
        st.stop()

    meal_plan["selected_foods"] = selected_foods
    meal_plan["medical_advice"] = medical_advice

    return meal_plan

# ✅ Generate meal plan based on user data
meal_plan = generate_meal_plan(user_data)

# ✅ Display Personalized Report
st.subheader("📊 Your Personalized Nutrition Report")

st.write(f"**🔹 BMI:** {meal_plan['bmi']} ({meal_plan['bmi_category']})")
st.write(f"**🔹 Caloric Recommendation:** {meal_plan['calories']}")
st.write(f"**🔹 Diet Type:** {meal_plan['diet']}")

st.markdown(
    f"""
    <div style="padding:10px; border-radius:5px; background-color:#555;">
        <b>🍽 Dietary Advice:</b> {meal_plan['dietary_advice']}
    </div>
    """, unsafe_allow_html=True
)

# ✅ Display Medical Considerations
if meal_plan["medical_advice"]:
    st.subheader("⚕ Medical Considerations")
    for advice in meal_plan["medical_advice"]:
        st.write(f"- {advice}")

# ✅ Suggested Foods Table
st.subheader("🍏 Recommended Foods & Nutritional Breakdown")
st.dataframe(meal_plan["selected_foods"])

# ✅ Meal Plan Summary
st.subheader("📌 Key Takeaways for a Healthy Diet")
st.markdown(
    """
    - 🥗 **Eat a variety of foods** to ensure you get all essential nutrients.
    - 💧 **Stay hydrated** by drinking at least 8 glasses of water daily.
    - 🚶 **Exercise regularly** to complement your nutrition plan.
    - 🛑 **Avoid processed foods** high in added sugars and unhealthy fats.
    - 🍎 **Include fresh fruits and vegetables** in your daily diet.
    """
)

# ✅ Save the generated meal plan to session state
st.session_state['meal_plan'] = meal_plan

st.success("✅ Meal plan report generated successfully! Check your 'View Meal Plan' page for details.")
