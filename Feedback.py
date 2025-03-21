import streamlit as st
import json
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta, time

st.title("📝 Feedback & Progress Hub")
if "logged_in_user" not in st.session_state:
    st.error("🚨 Please log in first!")
    st.stop()
username = st.session_state["logged_in_user"]
if not os.path.exists("storage.json"):
    st.error("⚠️ No user data found! Please fill out your profile first.")
    st.stop()
with open("storage.json", "r") as f:
    storage = json.load(f)
user_data = storage.get(username, {})
feedback_list = user_data.get("feedback", [])
menu_options = [
    "Give Feedback",
    "View Feedback & Insights",
    "Modify/Delete Feedback",
    "Weekly Report",
    "Streak & Rewards"
]
selected_option = st.selectbox("Select an option", menu_options)

# ✅ GIVE FEEDBACK SECTION
if selected_option == "Give Feedback":
    st.header("✍️ Provide Today's Feedback")
    now = datetime.now()
    current_time = now.time()
    today_date_str = now.strftime("%Y-%m-%d")
    start_time = time(21, 0)  
    end_time = time(23, 59)   
    already_submitted_today = any(
        feedback["date"] == today_date_str for feedback in feedback_list
    )
    if current_time < start_time:
        remaining_time = datetime.combine(now.date(), start_time) - now
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        st.info(f"⏳ Feedback opens at 09:00 PM. Time remaining: **{hours}h {minutes}m {seconds}s**")
    reminder_time = time(21, 55)
    if reminder_time <= current_time < start_time:
        st.toast("🔔 Feedback submission opens soon! Get ready to log your day.", icon="⏰")
    if start_time <= current_time <= end_time:
        if already_submitted_today:
            st.success("✅ You've already submitted today's feedback. Come back tomorrow!")
        else:
            with st.form("feedback_form"):
                st.subheader("🌟 General Wellbeing")
                mood = st.selectbox("Mood", ["Happy", "Neutral", "Sad"])
                energy = st.slider("Energy Level (1-10)", 1, 10, 5)
                hydration = st.selectbox("Water Intake", ["<1L", "1-2L", ">2L"])
                hours_slept = st.slider("Hours Slept", 0, 12, 6)
                sleep_quality = st.slider("Sleep Quality (1-5)", 1, 5, 3)
                st.subheader("🏋️ Exercise Feedback")
                exercise_completed = st.selectbox("Exercise Completed?", ["Yes", "No"])
                exercise_effort = st.selectbox("Exercise Effort", ["Easy", "Moderate", "Hard"])
                exercise_pain = st.selectbox("Any Pain?", ["None", "Knees", "Back", "Shoulders", "Other"])
                fatigue_level = st.selectbox("Fatigue After Exercise", ["None", "Mild", "Severe"])
                energy_after = st.selectbox("How did you feel after exercising?", ["More energized", "Tired", "Drained"])
                preferred_type = st.selectbox("Preferred Type of Exercise", ["Yoga", "Cardio", "Strength", "Stretching"])
                motivation_level = st.selectbox("Motivation Level Today", ["Low", "Normal", "High"])
                time_preference = st.selectbox("Preferred Time for Exercise", ["Morning", "Evening", "Anytime"])
                st.subheader("🍽️ Meals Feedback")
                meals_feedback = {}
                for meal in ["Breakfast", "Lunch", "Dinner"]:
                    st.markdown(f"**{meal} Feedback**")
                    satisfaction = st.slider(f"{meal} Satisfaction (1-5)", 1, 5, 3, key=f"{meal}_satisfaction")
                    hunger_after = st.selectbox(f"Were you hungry after {meal}?", ["Yes", "No"], key=f"{meal}_hunger")
                    issues = st.selectbox(f"Any issues after {meal}?", ["None", "Bloating", "Acidity", "Other"], key=f"{meal}_issues")
                    meals_feedback[meal] = {
                        "satisfaction": satisfaction,
                        "hunger_after": hunger_after,
                        "issues": issues
                    }
                submitted = st.form_submit_button("Submit Feedback")
            if submitted:
                new_feedback = {
                    "date": today_date_str,
                    "mood": mood,
                    "energy_level": energy,
                    "hydration": hydration,
                    "hours_slept": hours_slept,
                    "sleep_quality": sleep_quality,
                    "exercise": {
                        "completed": exercise_completed,
                        "effort": exercise_effort,
                        "pain": exercise_pain,
                        "fatigue_level": fatigue_level,
                        "energy_after": energy_after,
                        "preferred_type": preferred_type,
                        "motivation_level": motivation_level,
                        "time_preference": time_preference
                    },
                    "meals": meals_feedback
                }
                feedback_list.append(new_feedback)
                user_data["feedback"] = feedback_list
                storage[username] = user_data
                with open("storage.json", "w") as f:
                    json.dump(storage, f, indent=4)
                st.success("✅ Feedback submitted successfully for today!")
    elif current_time > end_time:
        st.warning("⏰ The feedback window has closed. Please submit tomorrow between 10:00 PM and 12:00 AM.")

# ✅ VIEW FEEDBACK & INSIGHTS
elif selected_option == "View Feedback & Insights":
    st.header("📂 Your Feedback Entries & Insights")
    if not feedback_list:
        st.info("No feedback records yet. Start by submitting today's feedback.")
    else:
        df_feedback = pd.DataFrame(feedback_list)
        df_feedback["date"] = pd.to_datetime(df_feedback["date"])
        st.dataframe(df_feedback[["date", "mood", "energy_level", "hydration"]])
        avg_energy = df_feedback["energy_level"].mean()
        mood_mode = df_feedback["mood"].value_counts().idxmax()
        st.write(f"🔋 **Average Energy**: {avg_energy:.1f}/10")
        st.write(f"🙂 **Most Frequent Mood**: {mood_mode}")

# ✅ MODIFY / DELETE FEEDBACK
elif selected_option == "Modify/Delete Feedback":
    st.header("🛠️ Modify or Delete Feedback Entries")
    if not feedback_list:
        st.info("No feedback records to modify/delete.")
    else:
        df_feedback = pd.DataFrame(feedback_list)
        df_feedback["date"] = pd.to_datetime(df_feedback["date"])
        selected_date = st.selectbox("Select feedback date to modify/delete:", df_feedback["date"].dt.strftime("%Y-%m-%d"))
        selected_index = df_feedback[df_feedback["date"].dt.strftime("%Y-%m-%d") == selected_date].index[0]
        selected_feedback = feedback_list[selected_index]
        st.subheader(f"🗓️ Feedback Details for {selected_date}")
        st.markdown("### 🌟 General Wellbeing")
        st.write(f"**Mood:** {selected_feedback['mood']}")
        st.write(f"**Energy Level:** {selected_feedback['energy_level']}/10")
        st.write(f"**Hydration:** {selected_feedback['hydration']}")
        st.write(f"**Hours Slept:** {selected_feedback['hours_slept']}")
        st.write(f"**Sleep Quality:** {selected_feedback['sleep_quality']}/5")
        st.markdown("### 🏋️ Exercise Feedback")
        exercise = selected_feedback["exercise"]
        st.write(f"**Exercise Completed?:** {exercise['completed']}")
        st.write(f"**Effort:** {exercise['effort']}")
        st.write(f"**Pain Reported:** {exercise['pain']}")
        st.write(f"**Fatigue Level:** {exercise['fatigue_level']}")
        st.write(f"**Energy After Exercise:** {exercise['energy_after']}")
        st.write(f"**Preferred Exercise Type:** {exercise['preferred_type']}")
        st.write(f"**Motivation Level:** {exercise['motivation_level']}")
        st.write(f"**Time Preference:** {exercise['time_preference']}")
        st.markdown("### 🍽️ Meals Feedback")
        meals = selected_feedback["meals"]
        for meal_name, meal_data in meals.items():
            st.markdown(f"#### {meal_name}")
            st.write(f"- **Satisfaction:** {meal_data['satisfaction']}/5")
            st.write(f"- **Hungry After?:** {meal_data['hunger_after']}")
            st.write(f"- **Issues:** {meal_data['issues']}")
        if st.button("Delete This Feedback"):
            feedback_list.pop(selected_index)
            user_data["feedback"] = feedback_list
            storage[username] = user_data
            with open("storage.json", "w") as f:
                json.dump(storage, f, indent=4)
            st.success(f"✅ Feedback from {selected_date} deleted!")
# ✅ WEEKLY REPORT (with Short Date Labels)
elif selected_option == "Weekly Report":
    st.header("📊 Weekly Progress Report & Past Reports")
    if not feedback_list:
        st.info("No feedback records yet. Submit feedback to generate reports.")
    else:
        df_feedback = pd.DataFrame(feedback_list)
        df_feedback["date"] = pd.to_datetime(df_feedback["date"])
        df_feedback["week_start"] = df_feedback["date"].dt.to_period('W').apply(lambda r: r.start_time.date())
        df_feedback["week_end"] = df_feedback["week_start"] + timedelta(days=6)
        df_feedback["week_label"] = df_feedback.apply(
            lambda row: f"{row['week_start'].strftime('%b')} {row['week_start'].day} - {row['week_end'].strftime('%b')} {row['week_end'].day}",
            axis=1
        )   
        week_labels_sorted = sorted(df_feedback["week_label"].unique(), reverse=True)
        selected_week_label = st.selectbox("Select Week to View Report", week_labels_sorted)
        selected_week_df = df_feedback[df_feedback["week_label"] == selected_week_label]
        week_start_date = selected_week_df.iloc[0]["week_start"]
        week_end_date = selected_week_df.iloc[0]["week_end"]
        today = datetime.now().date()
        current_week_start = today - timedelta(days=today.weekday()) 
        if week_start_date == current_week_start and len(selected_week_df) < 7:
            st.warning(f"⏳ Weekly report for **{selected_week_label}** will be available after logging 7 days of feedback.")
        else:
            st.success(f"📅 Showing report for **{selected_week_label}** ({len(selected_week_df)} days logged)")
            feedback_days = len(selected_week_df)
            exercise_days = selected_week_df[selected_week_df["exercise"].apply(lambda x: x["completed"] == "Yes")].shape[0]
            st.subheader("🗓️ Overview")
            st.metric("Feedback Logged", f"{feedback_days}/7 days")
            st.metric("Workouts Completed", f"{exercise_days}/7 days")
            avg_mood = selected_week_df["mood"].value_counts().idxmax() if not selected_week_df["mood"].empty else "N/A"
            avg_energy = selected_week_df["energy_level"].mean() if not selected_week_df.empty else 0
            st.subheader("📈 Mood & Energy Trends")
            st.write(f"Average Mood: {avg_mood}")
            st.write(f"Average Energy Level: {avg_energy:.1f}/10")
            energy_fig = go.Figure(go.Scatter(
                x=selected_week_df["date"],
                y=selected_week_df["energy_level"],
                mode='lines+markers',
                name='Energy Level'
            ))
            st.plotly_chart(energy_fig)
            hydration_summary = selected_week_df["hydration"].value_counts()
            sleep_avg = selected_week_df["hours_slept"].mean()
            st.subheader("💧 Hydration & Sleep Insights")
            st.write(f"Most common hydration: {hydration_summary.idxmax() if not hydration_summary.empty else 'N/A'}")
            st.write(f"Average Sleep: {sleep_avg:.1f} hours")
            pain_reports = selected_week_df["exercise"].apply(lambda x: x["pain"]).value_counts()
            st.subheader("🩺 Pain / Symptoms")
            if not pain_reports.empty:
                st.write(f"Most reported pain: {pain_reports.idxmax()}")
            else:
                st.write("No pain reported!")
            st.subheader("🍽️ Suggested Meal Plan for Next Week")
            bloating_reports = any(
                fb["meals"]["Dinner"]["issues"] == "Bloating" for fb in selected_week_df.to_dict(orient="records")
            )
            if bloating_reports:
                st.info("⚠️ Bloating detected. Recommending light meals.")
                next_week_meals = pd.DataFrame({
                    "Day": ["Monday", "Tuesday", "Wednesday"],
                    "Breakfast": ["Smoothie", "Oatmeal", "Fruit Bowl"],
                    "Lunch": ["Steamed Veggies", "Grilled Fish", "Chicken Salad"],
                    "Dinner": ["Soup", "Light Khichdi", "Steamed Tofu"]
                })
            else:
                st.success("✅ Balanced meals recommended.")
                next_week_meals = pd.DataFrame({
                    "Day": ["Monday", "Tuesday", "Wednesday"],
                    "Breakfast": ["Eggs & Toast", "Porridge & Nuts", "Smoothie"],
                    "Lunch": ["Brown Rice & Chicken", "Quinoa Bowl", "Grilled Paneer"],
                    "Dinner": ["Salad & Soup", "Khichdi", "Light Grilled Fish"]
                })
            st.table(next_week_meals)
            st.subheader("🏋️ Exercise Plan for Next Week")
            streak_count = 0
            week_dates = sorted(selected_week_df["date"].dt.date.tolist(), reverse=True)
            for i, d in enumerate(week_dates):
                if (week_dates[0] - d).days == i:
                    streak_count += 1
                else:
                    break
            if streak_count >= 7:
                st.balloons()
                st.success("🎉 7-Day Streak! Unlocking advanced exercises.")
                next_week_exercises = pd.DataFrame({
                    "Day": ["Monday", "Tuesday", "Wednesday"],
                    "Exercise": ["Bodyweight Training", "HIIT Cardio", "Strength Training"]
                })
            else:
                st.info("🚶 Starting light for consistency.")
                next_week_exercises = pd.DataFrame({
                    "Day": ["Monday", "Tuesday", "Wednesday"],
                    "Exercise": ["Yoga", "Brisk Walking", "Stretching"]
                })
            st.table(next_week_exercises)
# ✅ STREAK & REWARDS (Using View Insights Data)
elif selected_option == "Streak & Rewards":
    st.header("🔥 Your Streaks & Rewards")
    if not feedback_list:
        st.info("No feedback entries yet. Submit feedback to start building streaks.")
    else:
        df_feedback = pd.DataFrame(feedback_list)
        df_feedback["date"] = pd.to_datetime(df_feedback["date"])
        feedback_dates = sorted(df_feedback["date"].dt.date.unique(), reverse=True)
        feedback_streak = 0
        if feedback_dates:
            feedback_streak = 1
            for i in range(1, len(feedback_dates)):
                expected_date = feedback_dates[i - 1] - timedelta(days=1)
                if feedback_dates[i] == expected_date:
                    feedback_streak += 1
                else:
                    break
        exercise_feedback = df_feedback[df_feedback["exercise"].apply(lambda x: x["completed"] == "Yes")]
        exercise_dates = sorted(exercise_feedback["date"].dt.date.unique(), reverse=True)
        exercise_streak = 0
        if exercise_dates:
            exercise_streak = 1
            for i in range(1, len(exercise_dates)):
                expected_date = exercise_dates[i - 1] - timedelta(days=1)
                if exercise_dates[i] == expected_date:
                    exercise_streak += 1
                else:
                    break
        st.metric("📝 Feedback Streak", f"{feedback_streak} days")
        st.metric("🏋️ Exercise Streak", f"{exercise_streak} days")
        st.subheader("🏅 Rewards Unlocked")
        if feedback_streak >= 7:
            st.success("🎉 You've unlocked: **7-Day Feedback Streak Badge!**")
            st.balloons()
        if exercise_streak >= 7:
            st.success("🎉 You've unlocked: **7-Day Exercise Streak Badge!**")
            st.balloons()
        if feedback_streak >= 30:
            st.success("🔥 Legendary Streak: **30-Day Consistency Champion!**")
            st.balloons()
        if feedback_streak < 3 and exercise_streak < 3:
            st.info("🔔 Keep going! You're close to unlocking new badges!")