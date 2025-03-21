import streamlit as st
import json
import os
from streamlit_option_menu import option_menu
import time 

st.set_page_config(page_title="Automatic Diet Recommendation", layout="wide")
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True
)
if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump({}, f)
with open("users.json", "r", encoding="utf-8") as f:
    users = json.load(f)

if "logged_in_user" not in st.session_state:
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Home", "Get Started"],
            default_index=0,
        )

    if selected == "Home":
        st.markdown("<h1 style='text-align: center; color: #2e7d32;'>Personalised Health Management</h1>", unsafe_allow_html=True)
        st.markdown("""
            <div style="display: flex; justify-content: center;">
                <img src="https://cdn.pixabay.com/photo/2016/03/05/19/02/salad-1238247_1280.jpg" 
                    style="width: 1200px; height: 300px; object-fit: cover; border-radius: 10px;">
            </div>
            <div style="text-align: center; font-size: 20px; line-height: 1.6; color: #555;">
                Your Personalized Nutrition & Health Companion. <br>
                Get AI-driven diet plans and fitness guidance tailored to your lifestyle and health needs.
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; color: #888; font-size: 14px;">
                © 2025 Automatic Diet Recommendation. All Rights Reserved.
                <br><br>
                <a href='https://www.facebook.com' target='_blank'>Facebook</a> |
                <a href='https://www.twitter.com' target='_blank'>Twitter</a> |
                <a href='https://www.instagram.com' target='_blank'>Instagram</a> |
                <a href='https://www.linkedin.com' target='_blank'>LinkedIn</a>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif selected == "Get Started":
        st.title("About This App")
        st.write("This app helps you with personalized meal plans.")
        st.subheader("Login / Sign Up")
        choice = st.radio("Select an option:", ["Sign Up", "Login"])
        if choice == "Sign Up":
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            if st.button("Sign Up"):
                if new_username in users:
                    st.warning("⚠️ Username already exists! Please log in.")
                else:
                    with st.spinner("Creating your account..."):
                        users[new_username] = {"email": new_email, "password": new_password}
                        with open("users.json", "w", encoding="utf-8") as f:
                            json.dump(users, f)
                        st.session_state["new_user_signup"] = new_username
                        time.sleep(3)
                        st.success("✅ Account created successfully!")
                        time.sleep(3)
                        st.switch_page("pages/HealthData.py")
        elif choice == "Login":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if username in users and users[username]["password"] == password:
                    with st.spinner("Logging you in..."):
                        st.session_state["logged_in_user"] = username
                        st.session_state["user_email"] = users[username]["email"]
                        time.sleep(1)
                        st.success(f"🎉 Welcome back, {username}! Redirecting...")
                        time.sleep(2)
                        st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
else:
    st.title(f"Welcome, {st.session_state['logged_in_user']}! 👋")
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Profile", "Dashboard", "Review", "Food Plan", "Exercise", "Feedback"],
            default_index=0,
        )
    if selected == "Profile":
        with open("pages/Profile.py", "r", encoding="utf-8") as f:
            exec(f.read())
        if st.button("Logout"):
            del st.session_state["logged_in_user"]
            st.success("Logged out successfully!")
            st.rerun()
    elif selected == "Dashboard":
        with open("pages/Dashboard.py", "r", encoding="utf-8") as f:
            exec(f.read())
    elif selected == "Review":
        with open("pages/Review.py", "r", encoding="utf-8") as f:
            exec(f.read())
    elif selected == "Food Plan":
        with open("pages/FoodPlan.py", "r", encoding="utf-8") as f:
            exec(f.read())
    elif selected == "Exercise":
        with open("pages/Exercise.py", "r", encoding="utf-8") as f:
            exec(f.read())
    elif selected == "Feedback":
        with open("pages/Feedback.py", "r", encoding="utf-8") as f:
            exec(f.read())