import streamlit as st
import json
import os
import pandas as pd
import plotly.graph_objects as go

if "logged_in_user" not in st.session_state:
    st.error("🚨 Please log in first!")
    st.stop()

username = st.session_state["logged_in_user"]

if not os.path.exists("storage.json"):
    st.error("⚠️ No health data found! Please enter your details on the Diet Recommendation page.")
    st.stop()
with open("storage.json", "r") as f:
    storage = json.load(f)
if username not in storage:
    st.error("⚠️ No health data found! Please enter your details on the Diet Recommendation page.")
    st.stop()
data = storage[username]
# --- BMI Calculation ---
bmi = round(data["weight"] / ((data["height"] / 100) ** 2), 2)
bmi_category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
bmi_color = {"Underweight": "blue", "Normal": "green", "Overweight": "orange", "Obese": "red"}[bmi_category]

st.markdown("""
    <style>
    /* Increase the font size of the tab labels */
    button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
        font-size: 20px; /* Change this value to make it bigger/smaller */
        font-weight: bold;
    }

    /* Optional: Make selected tab more visible */
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #e0f7fa;
        color: black;
        width:25%;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align:center;'>👤 {username}'s  Health Summary at a Glance ✅</h1>", unsafe_allow_html=True)
st.markdown("---")

lifestyle_data = data.get("lifestyle", {})

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 BMI Analysis",
    "🩺 Medical History",
    "🏃 Lifestyle Factors",
    "📋 Doctor's Recommendations"
])
# --- TAB 1: BMI Analysis ---
with tab1:
    st.subheader("📊 BMI Analysis")
    fig_bmi_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        title={"text": "Your BMI"},
        gauge={
            "axis": {"range": [10, 40]},
            "steps": [
                {"range": [10, 18.5], "color": "blue"},
                {"range": [18.5, 24.9], "color": "green"},
                {"range": [25, 29.9], "color": "orange"},
                {"range": [30, 40], "color": "red"}
            ],
            "bar": {"color": "black"},
        }
    ))
    st.plotly_chart(fig_bmi_gauge, use_container_width=True)
    st.markdown(f"<h4 style='text-align:center; color:{bmi_color};'>✅ You are {bmi_category}</h4>", unsafe_allow_html=True)
    with st.expander("💡 BMI Insights & Tips"):
        if bmi_category == "Underweight":
            st.info("Consider increasing calorie intake with nutritious food. Consult your doctor for personalized advice.")
        elif bmi_category == "Normal":
            st.success("Great! Your BMI is in the healthy range. Keep maintaining your balanced lifestyle!")
        elif bmi_category == "Overweight":
            st.warning("You are overweight. Consider a balanced diet and regular physical activity.")
        else:
            st.error("Your BMI is in the obese range. Medical consultation is strongly advised!")
# --- TAB 2: Medical History ---
with tab2:
    st.subheader("🩺 Medical History")
    medical_df = pd.DataFrame(data["medical_history"].items(), columns=["Condition", "Present"])
    medical_df["Present"] = medical_df["Present"].apply(lambda x: "✅ Yes" if x else "❌ No")
    active_conditions = [cond for cond, present in data["medical_history"].items() if present]
    if not active_conditions:
        st.success("🎉 You have no recorded medical conditions! Keep maintaining a healthy lifestyle.")
    elif any(cond.lower() in [c.lower() for c in active_conditions] for cond in ["Diabetes", "Heart Disease", "Chronic Kidney Disease"]):
        st.error("🚨 Some critical medical conditions detected. Please ensure regular medical check-ups and follow your doctor's advice carefully.")
    elif any(cond.lower() in [c.lower() for c in active_conditions] for cond in ["Hypertension", "Asthma", "High Cholesterol", "Arthritis"]):
        st.warning("⚠️ Some ongoing health conditions detected. Please stay on track with your medication and lifestyle adjustments.")
    else:
        st.info("💡 Don't forget regular health check-ups and maintain your preventive care routines!")
    st.markdown("### 📝 Your Medical History")
    st.table(medical_df)
    with st.expander("💡 Tips for Managing Health Conditions"):
        if not active_conditions:
            st.write("✅ You have no health conditions. Continue eating well, exercising regularly, and having routine check-ups.")
        else:
            st.write("Here are a few general tips for managing chronic health conditions:")
            st.markdown("""
                - 🥗 **Healthy Diet**: Choose nutrient-dense foods and avoid excess salt, sugar, and trans fats.
                - 🏃 **Regular Exercise**: Aim for at least 30 minutes of moderate activity on most days.
                - 💊 **Medication Adherence**: Take your prescribed medications regularly and as directed.
                - 🧘 **Stress Management**: Practice relaxation techniques such as meditation, deep breathing, or yoga.
                - 🩺 **Regular Check-ups**: Monitor your health regularly and consult your doctor when necessary.
            """)
# --- TAB 3: Lifestyle Factors ---
with tab3:
    st.subheader("🏃 Lifestyle Factors")
    def lifestyle_card(title, value, emoji, color):
        return f"""
            <div style="
                background-color:{color};
                color:white;
                padding:20px;
                border-radius:15px;
                width: 180px;
                text-align:center;
                display:inline-block;
                margin:10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            ">
                <div style="font-size:30px;">{emoji}</div>
                <h4 style="margin-top:10px;">{title}</h4>
                <p style="font-size:18px; margin: 0;">{value}</p>
            </div>
        """
    cards_html = (
        lifestyle_card("Smoking", "Yes" if lifestyle_data.get("smoking") else "No", "🚬", "#d32f2f") +
        lifestyle_card("Alcohol", "Yes" if lifestyle_data.get("alcohol") else "No", "🍷", "#7b1fa2") +
        lifestyle_card("Exercise", lifestyle_data.get("exercise", "N/A"), "🏋️‍♂️", "#388e3c") +
        lifestyle_card("Sleep (hrs)", lifestyle_data.get("sleep", "N/A"), "😴", "#0288d1") +
        lifestyle_card("Stress", lifestyle_data.get("stress", "N/A"), "😟", "#fbc02d")
    )
    st.markdown(cards_html, unsafe_allow_html=True)
    with st.expander("💡 Lifestyle Suggestions"):
        if lifestyle_data.get("smoking"):
            st.warning("Smoking is harmful to your health. Quitting can improve lung and heart health.")
        else:
            st.success("Great! You're smoke-free. Keep it up!")
        if lifestyle_data.get("alcohol"):
            st.warning("Try to limit alcohol consumption for better liver health and overall wellbeing.")
        else:
            st.success("You're maintaining healthy alcohol habits!")
        exercise = lifestyle_data.get("exercise", "N/A")
        if exercise == "None":
            st.warning("Regular exercise is important. Aim for at least 30 mins a day.")
        else:
            st.success("Great! Keep up your exercise routine!")
# --- TAB 4: Doctor's Recommendations ---
with tab4:
    recommendations = data.get("doctor_recommendations", [])
    if recommendations:
        st.markdown("#### 📝 Your Personalized Health Advice")
        for idx, rec in enumerate(recommendations, start=1):
            st.markdown(f"""
                <div style="
                    background-color: #f1f8e1;
                    color:#111;
                    padding: 15px;
                    margin-bottom: 10px;
                    border-left: 6px solid #558b2f;
                    border-radius: 8px;
                ">
                    <b>✅ </b> {rec}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No doctor recommendations recorded.")
st.markdown("---")
st.markdown("<p style='text-align:center;'>🔒 Your data is secure and private.</p>", unsafe_allow_html=True)