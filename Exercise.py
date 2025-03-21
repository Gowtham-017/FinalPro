import streamlit as st
import json
import os

st.title("🏋️ Exercise Plans")
script_dir = os.path.dirname(os.path.abspath(__file__)) 
exercise_data_file = os.path.join(script_dir, "./pages/exercisedata.json")
if not os.path.exists(exercise_data_file):
    st.error(f"⚠️ Exercise data file `{exercise_data_file}` not found!")
    st.stop()
with open(exercise_data_file, "r") as f:
    exercise_data = json.load(f)
def filter_exercises(exercises, required_tags=None, max_intensity=None):
    filtered = []
    intensity_rank = {"light": 1, "moderate": 2, "hard": 3}
    for ex in exercises:
        if max_intensity and intensity_rank.get(ex["intensity"], 1) > intensity_rank[max_intensity]:
            continue
        if required_tags and not any(tag in ex.get("tags", []) for tag in required_tags):
            continue
        filtered.append(ex)
    return filtered

st.markdown("## 🏃 Warm-up & Cardio Exercises")
warmup_exercises = exercise_data["cardio"]
carousel_html = """
<style>
.carousel-wrapper { position: relative; width: 100%; overflow: hidden; padding: 10px; }
.carousel-container { display: flex; gap: 100px; overflow-x: auto; scroll-behavior: smooth; white-space: nowrap; padding: 10px; scrollbar-width: none; -ms-overflow-style: none; }
.carousel-container::-webkit-scrollbar { display: none; }
.carousel-item { display: inline-block; width: 220px; text-align: center; margin-right: 15px; color: white; } /* text-align & color applied here */
.carousel-item img { width: 300px; height: 400px; border-radius: 10px; }
.carousel-title { font-size: 16px; font-weight: bold; margin-top: 10px; color: white; } /* white text for title */
.carousel-arrow { position: absolute; top: 25%; transform: translateY(-25%); background-color: white; color: black; border: none; padding: 12px 16px; font-size: 22px; cursor: pointer; border-radius: 50%; z-index: 10; box-shadow: 2px 2px 5px rgba(255, 255, 255, 0.5); }
.carousel-arrow.left { left: 10px; }
.carousel-arrow.right { right: 10px; }
.carousel-arrow:hover { background-color: #ddd; }
</style>
<div class="carousel-wrapper">
<button class="carousel-arrow left" onclick="scrollCarousel(-250)">❮</button>
<div class="carousel-container" id="carousel">
"""
for exercise in warmup_exercises:
    carousel_html += f"""
    <div class="carousel-item">
        <img src="{exercise['img']}" alt="{exercise['title']}">
        <div class="carousel-title">{exercise['title']}</div>
    </div>
    """
carousel_html += """
</div>
<button class="carousel-arrow right" onclick="scrollCarousel(250)">❯</button>
</div>
<script>
function scrollCarousel(amount) {{
    document.getElementById('carousel').scrollBy({{ left: amount, behavior: 'smooth' }});
}}
</script>
"""
st.components.v1.html(carousel_html, height=500)
# ✅ Generalized Exercise Plan
st.markdown("---")
st.markdown("## 🏆 Generalized Exercise Plan")
general_exercises = exercise_data["general"]
cols = st.columns(3)
for i, exercise in enumerate(general_exercises):
    with cols[i % 3]:
        st.image(exercise["img"], caption=exercise["title"], width=200)
        st.write(exercise.get("text", ""))
# ✅ Personalized BMI-Based Exercise Plan
st.markdown("---")
st.markdown("## 🎯 Personalized BMI-Based Exercise Plan")
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
bmi = round(user_data["weight"] / ((user_data["height"] / 100) ** 2), 2)
if bmi < 18.5:
    bmi_category = "Underweight"
    bmi_exercises = exercise_data["bmi_based"]["underweight"]
elif 18.5 <= bmi < 24.9:
    bmi_category = "Normal Weight"
    bmi_exercises = exercise_data["bmi_based"]["normal"]
elif 25.0 <= bmi < 29.9:
    bmi_category = "Overweight"
    bmi_exercises = exercise_data["bmi_based"]["overweight"]
else:
    bmi_category = "Obese"
    bmi_exercises = exercise_data["bmi_based"]["obese"]
show_reminder = False
reasons = []
personalized_exercises = []
if feedback_list:
    latest_feedback = feedback_list[-1]
    ex_feedback = latest_feedback["exercise"]
    if ex_feedback.get("pain") and ex_feedback["pain"] != "None":
        pain_area = ex_feedback["pain"].lower()
        show_reminder = True
        reasons.append(f"{pain_area.title()} Pain")
        pain_exercises = filter_exercises(
            exercise_data["personalized"]["pain"],
            required_tags=[f"no {pain_area} pain"],
            max_intensity="light"
        )
        personalized_exercises.extend(pain_exercises)
    if ex_feedback.get("fatigue_level") == "Severe":
        show_reminder = True
        reasons.append("Severe Fatigue")
        personalized_exercises.extend(exercise_data["personalized"]["severe_fatigue"])
    if ex_feedback.get("motivation_level") == "Low":
        show_reminder = True
        reasons.append("Low Motivation")
        personalized_exercises.extend(exercise_data["personalized"]["motivation_low"])
    pref_type = ex_feedback.get("preferred_type", "").lower()
    pref_key = f"preferred_type_{pref_type}"
    if pref_key in exercise_data["personalized"]:
        show_reminder = True
        reasons.append(f"Preference for {pref_type.title()}")
        personalized_exercises.extend(exercise_data["personalized"][pref_key])
if personalized_exercises:
    unique_exercises = {ex["title"]: ex for ex in personalized_exercises}
    bmi_exercises = list(unique_exercises.values())
if show_reminder and reasons:
    reasons_text = ", ".join(reasons)
    st.warning(f"⚠️ Personalized Plan: You reported **{reasons_text}**. We've customized today's exercises accordingly.")
cols = st.columns(2)
for i, exercise in enumerate(bmi_exercises):
    with cols[i % 2]:
        st.image(exercise["img"], caption=exercise["title"], width=200)
        st.write(exercise.get("text", ""))
st.info("💡 Stay hydrated and listen to your body during exercise!")