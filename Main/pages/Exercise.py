import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Function to fetch and resize images
def fetch_resized_image(url, new_width=250, new_height=150):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.resize((new_width, new_height))
        return img
    else:
        return None  # Return None if the image couldn't be fetched

# Set page title
st.title("🏋️‍♂️ Exercise Plan")

# Generalized Exercise Plan (For All Users)
st.header("💪 Generalized Exercise Plan (For Everyone)")
st.write("These exercises are beneficial for overall fitness, irrespective of BMI.")

general_exercises = {
    "Squats": "https://upload.wikimedia.org/wikipedia/commons/d/d8/Man-Doing-Bodyweight-Air-Squats-Outdoors.jpg",
    "Push-ups": "https://source.unsplash.com/300x200/?pushups",
    "Planks": "https://source.unsplash.com/300x200/?plank",
    "Running": "https://source.unsplash.com/300x200/?running"
}

# Display General Exercises with resized images
for name, url in general_exercises.items():
    img = fetch_resized_image(url)
    if img:
        st.image(img, caption=name)
st.markdown("---")  # Divider for better separation

# User Input for BMI-based Specialization
st.header("🩺 Personalized Exercise Plan Based on BMI")
st.write("Your BMI category determines the best exercise routine for you.")

bmi_category = st.selectbox("Select Your BMI Category:", 
                            ["Underweight", "Normal Weight", "Overweight", "Obese"])

# BMI-based Exercise Plans
exercise_plans = {
    "Underweight": {
        "description": "🏋️ Focus on **muscle gain** with strength training and a calorie surplus.",
        "exercises": {
            "Weight Lifting": "https://source.unsplash.com/300x200/?weight-lifting",
            "Resistance Training": "https://source.unsplash.com/300x200/?resistance-training",
            "Calisthenics": "https://source.unsplash.com/300x200/?calisthenics",
            "Protein-Rich Diet": "https://source.unsplash.com/300x200/?protein-food"
        }
    },
    "Normal Weight": {
        "description": "⚖️ Maintain fitness with **balanced workouts** and moderate intensity.",
        "exercises": {
            "Jogging": "https://source.unsplash.com/300x200/?jogging",
            "Bodyweight Training": "https://source.unsplash.com/300x200/?bodyweight-training",
            "Yoga": "https://source.unsplash.com/300x200/?yoga",
            "Cycling": "https://source.unsplash.com/300x200/?cycling"
        }
    },
    "Overweight": {
        "description": "🔥 Burn fat with **cardio and moderate strength training**.",
        "exercises": {
            "Brisk Walking": "https://source.unsplash.com/300x200/?brisk-walk",
            "Jump Rope": "https://source.unsplash.com/300x200/?jump-rope",
            "Low-Impact HIIT": "https://source.unsplash.com/300x200/?hiit",
            "Swimming": "https://source.unsplash.com/300x200/?swimming"
        }
    },
    "Obese": {
        "description": "🦵 **Low-impact workouts** to reduce joint stress and improve mobility.",
        "exercises": {
            "Seated Leg Lifts": "https://source.unsplash.com/300x200/?seated-exercise",
            "Water Aerobics": "https://source.unsplash.com/300x200/?water-exercise",
            "Slow Walking": "https://source.unsplash.com/300x200/?walking",
            "Stretching": "https://source.unsplash.com/300x200/?stretching"
        }
    }
}

# Display Selected Exercise Plan with resized images
st.subheader(f"📌 {bmi_category} Exercise Plan")
st.write(exercise_plans[bmi_category]["description"])

for name, url in exercise_plans[bmi_category]["exercises"].items():
    img = fetch_resized_image(url)
    if img:
        st.image(img, caption=name)
