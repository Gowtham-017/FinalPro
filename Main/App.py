import streamlit as st
import json
import os
from streamlit_option_menu import option_menu
from pages import Profile,Review,Feedback,Exercise,FoodPlan,Dashboard
# Configure page layout
st.set_page_config(page_title="Automatic Diet Recommendation", layout="wide")

# Hide Streamlit’s default sidebar navigation
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# Ensure users.json exists
if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump({}, f)

# Load users data
with open("users.json", "r", encoding="utf-8") as f:
    users = json.load(f)

# 🔹 Sidebar: Different options for logged-in vs. non-logged-in users
if "logged_in_user" not in st.session_state:
    # BEFORE LOGIN (Home, About)
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Home", "Get Started"],
            default_index=0,
        )

    if selected == "Home":
        st.title("🍽️ Personalised Health Management")
        st.subheader("Your Personalized Nutrition Assistant")

        st.write("""
        Welcome to the **Personalised Nutrition Management** system, an AI-driven health assistant designed to create 
        personalized diet plans based on your health profile, medical history, and lifestyle habits.
        Whether you're looking to **lose weight, gain muscle, manage diabetes**, or just eat healthier, our app 
        helps you make the best dietary choices tailored to your needs. 🚀
        """)

        # Application Features
        st.header("🌟 Features")
        features = [
            "📊 **Personalized Diet Plans** based on BMI, lifestyle, and medical history",
            "🩺 **Integrates Health Metrics** such as vitals, lab test results, and medications",
            "📅 **Appointment & Medication Reminders** to keep you on track",
            "📈 **Visual Reports** with charts and tables for better analysis",
            "🥗 **Smart Meal Recommendations** based on your food preferences",
            "⚡ **User-friendly Interface** with easy navigation and profile management"
        ]
        for feature in features:
            st.markdown(f"- {feature}")

        # How It Works Section
        st.header("⚙️ How It Works")
        st.write("""
        1️⃣ **Sign Up / Log In** to create your profile.  
        2️⃣ **Enter Your Health Data** including BMI, vital signs, and lifestyle factors.  
        3️⃣ **Get AI-Based Recommendations** tailored to your needs.  
        4️⃣ **View Graphs & Reports** to track your progress.  
        5️⃣ **Stay On Track** with reminders and alerts.  
        """)

        # Image Section (You can replace with actual image URLs)
        # st.image("https://unsplash.com/photos/a-mixture-of-dried-fruits-and-nuts-PksCMkeiVYI", caption="Eat Healthy, Stay Fit!")

        # External Useful Links
        st.header("🔗 Useful Resources")
        st.markdown("""
        - 🏥 **[World Health Organization - Nutrition Advice](https://www.who.int/nutrition/en/)**  
        - 🍎 **[Harvard Healthy Eating Guide](https://www.hsph.harvard.edu/nutritionsource/healthy-eating-plate/)**  
        - 📉 **[BMI Calculator](https://www.calculator.net/bmi-calculator.html)**  
        """)

        # Call to Action
        st.info("Ready to improve your health? [Sign Up](/) now and start your journey towards better nutrition! 🚀")

        # Footer Section
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center;">
                <p>© 2025 Automatic Diet Recommendation. All Rights Reserved.</p>
                <p>Follow us on: 
                    <a href="https://www.facebook.com" target="_blank">Facebook</a> | 
                    <a href="https://www.twitter.com" target="_blank">Twitter</a> | 
                    <a href="https://www.instagram.com" target="_blank">Instagram</a> | 
                    <a href="https://www.linkedin.com" target="_blank">LinkedIn</a>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif selected == "Get Started":
        st.title("About This App")
        st.write("This app helps you with personalized meal plans.")

        # 🔹 Login & Sign-up Section
        st.subheader("Login / Sign Up")
        choice = st.radio("Select an option:", ["Sign Up", "Login"])

        if choice == "Sign Up":
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")

            if st.button("Sign Up"):
                if new_username in users:
                    st.warning("Username already exists! Please log in.")
                else:
                    users[new_username] = {"email": new_email, "password": new_password}
                    with open("users.json", "w", encoding="utf-8") as f:
                        json.dump(users, f)

                    # Store session & redirect to Diet Recommendation
                    st.session_state["new_user_signup"] = new_username
                    st.success("Account created successfully! Redirecting to Diet Recommendation...")
                    st.switch_page("pages/HealthData.py")

        elif choice == "Login":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if username in users and users[username]["password"] == password:
                    st.session_state["logged_in_user"] = username
                    st.success(f"Welcome, {username}! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid username or password!")

else:
    # AFTER LOGIN (Profile, Dashboard, Meal, View Data)
    st.title(f"Welcome, {st.session_state['logged_in_user']}! 👋")

    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Profile", "Dashboard", "Review", "Food Plan","Exercise","Feedback"],
            default_index=0,
        )

    # ✅ Display selected page content dynamically
    if selected == "Profile":
        Profile.show()

        # Logout button
        if st.button("Logout"):
            del st.session_state["logged_in_user"]
            st.success("Logged out successfully!")
            st.rerun()

    elif selected == "Dashboard":
        Dashboard.show()

    elif selected == "Review":
        Review.show()

    elif selected == "Food Plan":
        FoodPlan.show()
            
    elif selected == "Exercise":
        Exercise.show()
            
    elif selected == "Feedback":
        Feedback.show()
