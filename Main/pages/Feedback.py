import streamlit as st
import json
import os
from datetime import datetime

# Ensure storage file exists
if not os.path.exists("storage.json"):
    with open("storage.json", "w") as f:
        json.dump({}, f)

# Load storage data
with open("storage.json", "r", encoding="utf-8") as f:
    storage = json.load(f)

# Ensure user is logged in
if "logged_in_user" not in st.session_state:
    st.error("Please log in to access feedback!")
    st.stop()

username = st.session_state["logged_in_user"]

st.title("📋 Daily Feedback")

# -------------------
# 🕒 Display Live Clock
# -------------------
current_time = datetime.now().strftime("%H:%M:%S")
st.subheader(f"⏳ Current Time: {current_time}")

# Auto-refresh every 60 seconds
st.rerun() if st.button("Refresh Time") else None

# -------------------
# 🔽 Feedback Selection
# -------------------
st.subheader("📌 Select an Option:")
feedback_choice = st.selectbox(
    "Choose an action:",
    ["-- Select --", "Give Feedback", "View Past Feedback"],
)

# -------------------
# 🚫 Restrict Feedback Submission Before 10 PM
# -------------------
current_hour = datetime.now().hour
feedback_enabled = 21 <= current_hour <= 23

if feedback_choice == "Give Feedback" and not feedback_enabled:
    st.warning("⚠️ Feedback submission is only allowed between 10 PM - 12 AM.")
    st.stop()

# -------------------
# ✅ Option 1: Give Feedback
# -------------------
if feedback_choice == "Give Feedback":
    st.subheader("📝 Meal Plan Feedback")
    followed_plan = st.radio("Did you follow today's food plan?", ["Yes", "No"])
    rating = st.slider("How satisfied are you with the plan?", 1, 5, 3)
    meal_issues = st.text_area("Any issues with today's meals? (Optional)")

    st.subheader("🏋️ Exercise Feedback")
    exercise_completed = st.radio("Did you complete today's exercise?", ["Yes", "No"])
    additional_comments = st.text_area("Any other comments? (Optional)")

    if st.button("Submit Feedback"):
        feedback_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "followed_plan": followed_plan,
            "rating": rating,
            "meal_issues": meal_issues,
            "exercise_completed": exercise_completed,
            "additional_comments": additional_comments,
        }

        # Store feedback in user's profile
        if username not in storage:
            storage[username] = {}

        if "feedback" not in storage[username]:
            storage[username]["feedback"] = []

        storage[username]["feedback"].append(feedback_entry)

        with open("storage.json", "w", encoding="utf-8") as f:
            json.dump(storage, f)

        st.success("✅ Feedback submitted successfully!")

# -------------------
# 📅 Option 2: View & Delete Past Feedback
# -------------------
elif feedback_choice == "View Past Feedback":
    if "feedback" in storage.get(username, {}):
        st.subheader("📅 Past Feedback Entries")

        # Create a list of feedbacks with dates
        feedback_list = [
            f"{entry['date']} - Rating: {entry['rating']}/5"
            for entry in storage[username]["feedback"]
        ]

        if feedback_list:
            selected_feedback = st.selectbox("Select feedback to view or delete:", feedback_list)

            # Find the corresponding entry
            selected_index = feedback_list.index(selected_feedback)
            selected_entry = storage[username]["feedback"][selected_index]

            # Display feedback details
            st.markdown(f"**📆 Date:** {selected_entry['date']}")
            st.markdown(f"✔️ Followed Plan: {selected_entry['followed_plan']}")
            st.markdown(f"⭐ Satisfaction Rating: {selected_entry['rating']}/5")
            st.markdown(f"❗ Meal Issues: {selected_entry['meal_issues'] if selected_entry['meal_issues'] else 'None'}")
            st.markdown(f"🏋️ Exercise Completed: {selected_entry['exercise_completed']}")
            st.markdown(f"💬 Additional Comments: {selected_entry['additional_comments'] if selected_entry['additional_comments'] else 'None'}")
            st.markdown("---")

            # Delete feedback option
            if st.button("🗑️ Delete This Feedback"):
                del storage[username]["feedback"][selected_index]

                # Save updated feedback data
                with open("storage.json", "w", encoding="utf-8") as f:
                    json.dump(storage, f)

                st.success("✅ Feedback deleted successfully!")
                st.rerun()

    else:
        st.info("No past feedback found.")
