# import streamlit as st
# from PIL import Image
# import requests
# from io import BytesIO

# # Function to fetch and resize images
# def fetch_resized_image(url, new_width=250, new_height=150):
#     response = requests.get(url)
#     if response.status_code == 200:
#         img = Image.open(BytesIO(response.content))
#         img = img.resize((new_width, new_height))
#         return img
#     else:
#         return None  # Return None if the image couldn't be fetched

# # Set page title
# st.title("🏋️‍♂️ Exercise Plan")

# # Generalized Exercise Plan (For All Users)
# st.header("💪 Generalized Exercise Plan (For Everyone)")
# st.write("These exercises are beneficial for overall fitness, irrespective of BMI.")

# general_exercises = {
#     "Squats": "https://upload.wikimedia.org/wikipedia/commons/d/d8/Man-Doing-Bodyweight-Air-Squats-Outdoors.jpg",
#     "Push-ups": "https://source.unsplash.com/300x200/?pushups",
#     "Planks": "https://source.unsplash.com/300x200/?plank",
#     "Running": "https://source.unsplash.com/300x200/?running"
# }

# # Display General Exercises with resized images
# for name, url in general_exercises.items():
#     img = fetch_resized_image(url)
#     if img:
#         st.image(img, caption=name)
# st.markdown("---")  # Divider for better separation

# # User Input for BMI-based Specialization
# st.header("🩺 Personalized Exercise Plan Based on BMI")
# st.write("Your BMI category determines the best exercise routine for you.")

# bmi_category = st.selectbox("Select Your BMI Category:", 
#                             ["Underweight", "Normal Weight", "Overweight", "Obese"])

# # BMI-based Exercise Plans
# exercise_plans = {
#     "Underweight": {
#         "description": "🏋️ Focus on **muscle gain** with strength training and a calorie surplus.",
#         "exercises": {
#             "Weight Lifting": "https://source.unsplash.com/300x200/?weight-lifting",
#             "Resistance Training": "https://source.unsplash.com/300x200/?resistance-training",
#             "Calisthenics": "https://source.unsplash.com/300x200/?calisthenics",
#             "Protein-Rich Diet": "https://source.unsplash.com/300x200/?protein-food"
#         }
#     },
#     "Normal Weight": {
#         "description": "⚖️ Maintain fitness with **balanced workouts** and moderate intensity.",
#         "exercises": {
#             "Jogging": "https://source.unsplash.com/300x200/?jogging",
#             "Bodyweight Training": "https://source.unsplash.com/300x200/?bodyweight-training",
#             "Yoga": "https://source.unsplash.com/300x200/?yoga",
#             "Cycling": "https://source.unsplash.com/300x200/?cycling"
#         }
#     },
#     "Overweight": {
#         "description": "🔥 Burn fat with **cardio and moderate strength training**.",
#         "exercises": {
#             "Brisk Walking": "https://source.unsplash.com/300x200/?brisk-walk",
#             "Jump Rope": "https://source.unsplash.com/300x200/?jump-rope",
#             "Low-Impact HIIT": "https://source.unsplash.com/300x200/?hiit",
#             "Swimming": "https://source.unsplash.com/300x200/?swimming"
#         }
#     },
#     "Obese": {
#         "description": "🦵 **Low-impact workouts** to reduce joint stress and improve mobility.",
#         "exercises": {
#             "Seated Leg Lifts": "https://source.unsplash.com/300x200/?seated-exercise",
#             "Water Aerobics": "https://source.unsplash.com/300x200/?water-exercise",
#             "Slow Walking": "https://source.unsplash.com/300x200/?walking",
#             "Stretching": "https://source.unsplash.com/300x200/?stretching"
#         }
#     }
# }

# # Display Selected Exercise Plan with resized images
# st.subheader(f"📌 {bmi_category} Exercise Plan")
# st.write(exercise_plans[bmi_category]["description"])

# for name, url in exercise_plans[bmi_category]["exercises"].items():
#     img = fetch_resized_image(url)
#     if img:
#         st.image(img, caption=name)








# import streamlit as st
# from PIL import Image
# import requests
# from io import BytesIO
# import time

# # Function to fetch images or GIFs
# def fetch_resized_image(url, new_width=250, new_height=150):
#     response = requests.get(url)
#     if response.status_code == 200:
#         img = Image.open(BytesIO(response.content))
#         img = img.resize((new_width, new_height))
#         return img
#     else:
#         return None  

# # Function to start a countdown timer
# def workout_timer(duration):
#     with st.empty():
#         for seconds in range(duration, 0, -1):
#             st.metric(label="⏳ Workout Timer", value=f"{seconds} sec")
#             time.sleep(1)
#         st.success("🏁 Time's Up! Great Job!")

# # Set Page Title
# st.title("🏋️‍♂️ Personalized Exercise Plan")

# # **Generalized Exercise Plan for Everyone**
# st.header("💪 Generalized Exercise Plan")
# st.write("These exercises improve overall fitness and are recommended for everyone.")

# general_exercises = {
#     "Squats": "https://media.giphy.com/media/l3vR1lgaJR4RaAq0A/giphy.gif",
#     "Push-ups": "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif",
#     "Planks": "https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif",
#     "Running": "https://media.giphy.com/media/jt5gLm9U0oQh6/giphy.gif"
# }

# # **Display General Exercises in a Grid Layout**
# col1, col2 = st.columns(2)
# for index, (name, url) in enumerate(general_exercises.items()):
#     img = fetch_resized_image(url)
#     if img:
#         if index % 2 == 0:
#             with col1:
#                 st.image(img, caption=name)
#         else:
#             with col2:
#                 st.image(img, caption=name)

# st.markdown("---")  # Divider

# # **BMI-Based Personalized Exercise Plan**
# st.header("🩺 Personalized Exercise Plan")
# bmi_category = st.radio("Select Your BMI Category:", 
#                         ["Underweight", "Normal Weight", "Overweight", "Obese"], horizontal=True)

# # **Exercise Plans per BMI Category**
# exercise_plans = {
#     "Underweight": {
#         "description": "🏋️ Focus on **muscle gain** with strength training and a calorie surplus.",
#         "exercises": {
#             "Weight Lifting": "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
#             "Resistance Training": "https://media.giphy.com/media/l41YtZOb9EUABnuqA/giphy.gif",
#             "Calisthenics": "https://media.giphy.com/media/26n6xXg2qXB6Jmuuk/giphy.gif",
#             "Protein-Rich Diet": "https://media.giphy.com/media/JqfLfqfA6mxtvd0oGr/giphy.gif"
#         }
#     },
#     "Normal Weight": {
#         "description": "⚖️ Maintain fitness with **balanced workouts** and moderate intensity.",
#         "exercises": {
#             "Jogging": "https://media.giphy.com/media/3ov9k9AyzTiHf6Vq6k/giphy.gif",
#             "Bodyweight Training": "https://media.giphy.com/media/5xtDarzR0VPLVSoyWVa/giphy.gif",
#             "Yoga": "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif",
#             "Cycling": "https://media.giphy.com/media/l41lI4bYmcsPJX9Go/giphy.gif"
#         }
#     },
#     "Overweight": {
#         "description": "🔥 Burn fat with **cardio and moderate strength training**.",
#         "exercises": {
#             "Brisk Walking": "https://media.giphy.com/media/l0HlPjezGY9grdhVC/giphy.gif",
#             "Jump Rope": "https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif",
#             "Low-Impact HIIT": "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
#             "Swimming": "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif"
#         }
#     },
#     "Obese": {
#         "description": "🦵 **Low-impact workouts** to reduce joint stress and improve mobility.",
#         "exercises": {
#             "Seated Leg Lifts": "https://media.giphy.com/media/xT8qBepJQzUjXpeWuI/giphy.gif",
#             "Water Aerobics": "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
#             "Slow Walking": "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
#             "Stretching": "https://media.giphy.com/media/l41YtZOb9EUABnuqA/giphy.gif"
#         }
#     }
# }

# # **Display Personalized Exercise Plan**
# st.subheader(f"📌 {bmi_category} Exercise Plan")
# st.write(exercise_plans[bmi_category]["description"])

# # Grid Layout for Exercises
# col1, col2 = st.columns(2)
# for index, (name, url) in enumerate(exercise_plans[bmi_category]["exercises"].items()):
#     img = fetch_resized_image(url)
#     if img:
#         if index % 2 == 0:
#             with col1:
#                 st.image(img, caption=name)
#         else:
#             with col2:
#                 st.image(img, caption=name)

# st.markdown("---")  # Divider

# # **Workout Timer**
# st.header("⏳ Workout Timer")
# workout_time = st.slider("Set Timer (minutes)", min_value=1, max_value=30, value=5)
# if st.button("Start Workout Timer"):
#     workout_timer(workout_time * 60)

# # **Progress Tracker**
# st.header("📅 Exercise Progress Tracker")
# st.write("Check off the exercises you’ve completed today.")

# # Store progress in session state
# if "progress" not in st.session_state:
#     st.session_state.progress = {key: False for key in exercise_plans[bmi_category]["exercises"].keys()}

# # Checkboxes to mark progress
# for exercise in exercise_plans[bmi_category]["exercises"].keys():
#     st.session_state.progress[exercise] = st.checkbox(exercise, value=st.session_state.progress[exercise])

# st.success("Keep it up! You're making progress! 💪")







import streamlit as st
import time
import json

# Function to load user BMI from storage.json
def load_user_bmi():
    try:
        with open("storage.json", "r") as f:
            data = json.load(f)
        username = st.session_state.get("logged_in_user")  # Correct session key

        if username and username in data:
            user_data = data[username]
            return user_data.get("bmi", None)
    except Exception as e:
        return None

# Function to format time in HH:MM:SS format
def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d}"

# Function to create a stopwatch for each exercise
def create_stopwatch(exercise):
    if f"{exercise}_time" not in st.session_state:
        st.session_state[f"{exercise}_time"] = 0
        st.session_state[f"{exercise}_running"] = False
        st.session_state[f"{exercise}_start_time"] = None

    col1, col2, col3 = st.columns([1, 1, 1])

    # Start Stopwatch
    with col1:
        if st.button(f"▶ Start {exercise}", key=f"start_{exercise}"):
            if not st.session_state[f"{exercise}_running"]:
                st.session_state[f"{exercise}_running"] = True
                st.session_state[f"{exercise}_start_time"] = time.time() - st.session_state[f"{exercise}_time"]

    # Stop Stopwatch
    with col2:
        if st.button(f"⏸ Stop {exercise}", key=f"stop_{exercise}"):
            if st.session_state[f"{exercise}_running"]:
                st.session_state[f"{exercise}_running"] = False
                st.session_state[f"{exercise}_time"] = time.time() - st.session_state[f"{exercise}_start_time"]

    # Reset Stopwatch
    with col3:
        if st.button(f"🔄 Reset {exercise}", key=f"reset_{exercise}"):
            st.session_state[f"{exercise}_running"] = False
            st.session_state[f"{exercise}_time"] = 0
            st.session_state[f"{exercise}_start_time"] = None

    # Timer Display (updates live)
    timer_placeholder = st.empty()

    if st.session_state[f"{exercise}_running"]:
        while st.session_state[f"{exercise}_running"]:
            st.session_state[f"{exercise}_time"] = time.time() - st.session_state[f"{exercise}_start_time"]
            timer_placeholder.write(f"⏳ Stopwatch: {format_time(int(st.session_state[f'{exercise}_time']))}")
            time.sleep(1)
            st.rerun()
    else:
        timer_placeholder.write(f"⏳ Stopwatch: {format_time(int(st.session_state[f'{exercise}_time']))}")

# Get user's BMI category automatically
bmi = load_user_bmi()
if bmi is not None:
    if bmi < 18.5:
        bmi_category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        bmi_category = "Normal Weight"
    elif 25 <= bmi < 29.9:
        bmi_category = "Overweight"
    else:
        bmi_category = "Obese"
else:
    st.warning("⚠ Unable to detect BMI. Please update your health data.")
    st.stop()

# Exercise plans
exercise_plans = {
    "Underweight": {
        "description": "🏋️ Focus on **muscle gain** with strength training and a calorie surplus.",
        "exercises": ["Weight Lifting", "Resistance Training", "Calisthenics"]
    },
    "Normal Weight": {
        "description": "⚖️ Maintain fitness with **balanced workouts** and moderate intensity.",
        "exercises": ["Jogging", "Bodyweight Training", "Yoga"]
    },
    "Overweight": {
        "description": "🔥 Burn fat with **cardio and moderate strength training**.",
        "exercises": ["Brisk Walking", "Jump Rope", "Low-Impact HIIT"]
    },
    "Obese": {
        "description": "🦵 **Low-impact workouts** to reduce joint stress and improve mobility.",
        "exercises": ["Seated Leg Lifts", "Water Aerobics", "Slow Walking"]
    }
}

# Display auto-selected category
st.title("🏋️‍♂️ Personalized Exercise Plan")
st.subheader(f"📌 {bmi_category} Category")
st.write(exercise_plans[bmi_category]["description"])
st.markdown("---")

# Display exercises
for exercise in exercise_plans[bmi_category]["exercises"]:
    with st.expander(f"▶ {exercise} (Click to expand)"):
        st.write(f"### Steps for {exercise}:")
        st.write("- Step 1: Warm up for 5 minutes")
        st.write("- Step 2: Perform exercise for 30-60 seconds")
        st.write("- Step 3: Rest for 10 seconds")
        st.write("- Step 4: Repeat for 3 sets")

        # Stopwatch for each exercise
        create_stopwatch(exercise)

st.success("🔥 Stay Consistent & Keep Moving!")
