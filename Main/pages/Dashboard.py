# import streamlit as st
# import json
# import os
# import pandas as pd
# import plotly.express as px
# import plotly.figure_factory as ff
# import plotly.graph_objects as go

# # Check if user is logged in
# if "logged_in_user" not in st.session_state:
#     st.error("Please log in first!")
#     st.stop()

# username = st.session_state["logged_in_user"]

# # Load storage.json
# if not os.path.exists("storage.json"):
#     st.error("No health data found! Please enter your details on the Diet Recommendation page.")
#     st.stop()

# with open("storage.json", "r") as f:
#     storage = json.load(f)

# if username not in storage:
#     st.error("No health data found! Please enter your details on the Diet Recommendation page.")
#     st.stop()

# data = storage[username]

# # **BMI Calculation**
# bmi = round(data["weight"] / ((data["height"] / 100) ** 2), 2)
# bmi_category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"

# # **BMI Category Text with Color**
# bmi_category_text = f"You are, <p style='font-size: 30px; font-weight: bold; color: {'green' if bmi_category == 'Normal' else 'red'};'> {bmi_category} </p>"
# st.markdown(bmi_category_text, unsafe_allow_html=True)

# # **BMI Ranges & Colors**
# bmi_ranges = {
#     "Underweight": (0, 18.5, "blue"),
#     "Normal": (18.5, 24.9, "green"),
#     "Overweight": (25, 29.9, "orange"),
#     "Obese": (30, 40, "red"),
# }

# # **Create a Continuous Bar Chart**
# fig = go.Figure()

# for category, (min_val, max_val, color) in bmi_ranges.items():
#     fig.add_trace(go.Bar(
#         x=[max_val - min_val],
#         y=["BMI Range"],
#         orientation='h',
#         name=category,
#         marker=dict(color=color),
#         hoverinfo="x+name"
#     ))

# # **Add User's BMI as a Marker**
# fig.add_trace(go.Scatter(
#     x=[bmi],
#     y=["BMI Range"],
#     mode="markers+text",
#     marker=dict(size=15, color="black", symbol="diamond"),
#     name=f"Your BMI: {bmi}",
#     text=[f"⬆ {bmi} ({bmi_category})"],
#     textposition="top center"
# ))

# # **Customize Layout**
# fig.update_layout(
#     title="BMI Analysis",
#     xaxis_title="BMI (kg/m²)",
#     yaxis_title="",
#     xaxis=dict(range=[10, 40]),  # Ensures full visibility of BMI range
#     height=300,
#     showlegend=True,
#     barmode="stack"  # Stacks bars together for a continuous range
# )

# # **Display Graph**
# st.plotly_chart(fig, use_container_width=True)

# # **Medical History**
# st.subheader("Medical History")
# history_df = pd.DataFrame(data["medical_history"].items(), columns=["Condition", "Present"])
# history_df["Present"] = history_df["Present"].apply(lambda x: "✅ Yes" if x else "❌ No")
# st.dataframe(history_df, height=200, width=500)

# # **Lifestyle Breakdown - Donut Chart**
# st.subheader("Lifestyle Breakdown")
# lifestyle_labels = ["Smoking", "Alcohol", "Exercise", "Sleep", "Stress"]
# lifestyle_values = [
#     1 if data["lifestyle"]["smoking"] else 0,
#     1 if data["lifestyle"]["alcohol"] else 0,
#     {"None": 0, "Light": 1, "Moderate": 2, "Intense": 3}[data["lifestyle"]["exercise"]],
#     data["lifestyle"]["sleep"],
#     {"Low": 1, "Moderate": 2, "High": 3}[data["lifestyle"]["stress"]],
# ]

# fig_lifestyle = px.pie(
#     names=lifestyle_labels,
#     values=lifestyle_values,
#     hole=0.4,
#     title="Lifestyle Factors",
#     color_discrete_sequence=px.colors.qualitative.Set3,
# )

# st.plotly_chart(fig_lifestyle, use_container_width=True)

# # **Medications**
# st.subheader("Prescribed Medications")
# if data["medications"]:
#     st.write(", ".join(data["medications"]))
# else:
#     st.write("No medications prescribed.")

# # **Doctor’s Notes & Appointments**
# st.subheader("Doctor's Notes & Appointments")
# st.info(data["doctors_notes"] if data["doctors_notes"] else "No notes available.")



# import streamlit as st
# import json
# import os
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# # **Check if user is logged in**
# if "logged_in_user" not in st.session_state:
#     st.error("🚨 Please log in first!")
#     st.stop()

# username = st.session_state["logged_in_user"]

# # **Load storage.json**
# if not os.path.exists("storage.json"):
#     st.error("⚠️ No health data found! Please enter your details on the Diet Recommendation page.")
#     st.stop()

# with open("storage.json", "r") as f:
#     storage = json.load(f)

# if username not in storage:
#     st.error("⚠️ No health data found! Please enter your details on the Diet Recommendation page.")
#     st.stop()

# data = storage[username]

# # **BMI Calculation**
# bmi = round(data["weight"] / ((data["height"] / 100) ** 2), 2)
# bmi_category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
# bmi_color = {"Underweight": "blue", "Normal": "green", "Overweight": "orange", "Obese": "red"}[bmi_category]

# # **Page Title**
# st.markdown(f"<h1 style='text-align:center;'>👤 {username}'s Health Profile</h1>", unsafe_allow_html=True)

# # **BMI Display - Gauge Chart**
# st.subheader("📊 BMI Analysis")
# # **BMI Category with Stylish Text**
# st.markdown(f"<h3 style='text-align:left; color:{bmi_color};'>✅ You are {bmi_category}</h3>", unsafe_allow_html=True)
# fig_bmi_gauge = go.Figure(go.Indicator(
#     mode="gauge+number",
#     value=bmi,
#     title={"text": "Your BMI"},
#     gauge={
#         "axis": {"range": [10, 40]},
#         "steps": [
#             {"range": [10, 18.5], "color": "blue"},
#             {"range": [18.5, 24.9], "color": "green"},
#             {"range": [25, 29.9], "color": "orange"},
#             {"range": [30, 40], "color": "red"}
#         ],
#         "bar": {"color": "black"},
#     }
# ))
# st.plotly_chart(fig_bmi_gauge, use_container_width=True)


# # **Columns Layout for Medical & Lifestyle Data**
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("🩺 Medical History")
#     medical_conditions = [f"✅ {cond}" if present else f"❌ {cond}" for cond, present in data["medical_history"].items()]
#     st.markdown("\n".join(medical_conditions) if medical_conditions else "No medical history recorded.")

#     st.subheader("🧪 Lab Tests & Results")
#     if data.get("recent_lab_tests"):
#         lab_results = [f"🧪 **{test}**: {data['lab_results'].get(test, 'Not Provided')}" for test in data["recent_lab_tests"]]
#         st.markdown("\n".join(lab_results))
#     else:
#         st.write("No lab tests recorded.")

#     st.subheader("🍎 Food Allergies")
#     st.write(", ".join(data["food_allergies"]) if data.get("food_allergies") else "No known food allergies.")

# with col2:
#     st.subheader("🏃 Lifestyle Factors")
#     lifestyle_icons = {
#         "Smoking": "🚬", "Alcohol": "🍷", "Exercise": "🏋️‍♂️", "Sleep": "😴", "Stress": "😟"
#     }
#     lifestyle_values = [
#         1 if data["lifestyle"]["smoking"] else 0,
#         1 if data["lifestyle"]["alcohol"] else 0,
#         {"None": 0, "Light": 1, "Moderate": 2, "Intense": 3}[data["lifestyle"]["exercise"]],
#         data["lifestyle"]["sleep"],
#         {"Low": 1, "Moderate": 2, "High": 3}[data["lifestyle"]["stress"]],
#     ]
    
#     fig_lifestyle = px.pie(
#         names=list(lifestyle_icons.keys()),
#         values=lifestyle_values,
#         hole=0.4,
#         title="Lifestyle Breakdown",
#         color_discrete_sequence=px.colors.qualitative.Set3,
#     )
#     st.plotly_chart(fig_lifestyle, use_container_width=True)

# # **Current Symptoms - Bullet List**
# st.subheader("🤒 Current Symptoms")
# if data.get("current_symptoms"):
#     st.markdown("\n".join([f"- {symptom}" for symptom in data["current_symptoms"]]))
# else:
#     st.write("No symptoms reported.")

# # **Dietary Preferences & Doctor’s Recommendations**
# col3, col4 = st.columns(2)

# with col3:
#     st.subheader("🥗 Dietary Preferences")
#     st.markdown(f"🍽️ **Preference:** {data.get('dietary_preferences', 'No Preference')}")

# with col4:
#     st.subheader("💊 Medications")
#     st.write(", ".join(data["medications"]) if data["medications"] else "No medications prescribed.")

# # **Doctor’s Notes & Appointments**
# st.subheader("📋 Doctor's Notes & Appointments")
# st.info(data["doctors_notes"] if data["doctors_notes"] else "No notes available.")




import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# **Check if user is logged in**
if "logged_in_user" not in st.session_state:
    st.error("🚨 Please log in first!")
    st.stop()

username = st.session_state["logged_in_user"]

# **Load storage.json**
if not os.path.exists("storage.json"):
    st.error("⚠️ No health data found! Please enter your details on the Diet Recommendation page.")
    st.stop()

with open("storage.json", "r") as f:
    storage = json.load(f)

if username not in storage:
    st.error("⚠️ No health data found! Please enter your details on the Diet Recommendation page.")
    st.stop()

data = storage[username]

# **BMI Calculation**
bmi = round(data["weight"] / ((data["height"] / 100) ** 2), 2)
bmi_category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
bmi_color = {"Underweight": "blue", "Normal": "green", "Overweight": "orange", "Obese": "red"}[bmi_category]

# **Page Title**
st.markdown(f"<h1 style='text-align:center;'>👤 {username}'s Health Profile</h1>", unsafe_allow_html=True)
st.markdown("---")  # Divider

# **BMI Display - Gauge Chart**
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

# **BMI Category with Stylish Text**
st.markdown(f"<h3 style='text-align:center; color:{bmi_color};'>✅ You are {bmi_category}</h3>", unsafe_allow_html=True)
st.markdown("---")  # Divider

# **Medical History (Table)**
st.subheader("🩺 Medical History")
medical_df = pd.DataFrame(data["medical_history"].items(), columns=["Condition", "Present"])
medical_df["Present"] = medical_df["Present"].apply(lambda x: "✅ Yes" if x else "❌ No")
st.table(medical_df)

st.markdown("---")  # Divider

# **Lab Tests & Results**
st.subheader("🧪 Lab Tests & Results")
if data.get("recent_lab_tests"):
    for test in data["recent_lab_tests"]:
        result = data["lab_results"].get(test, "Not Provided")
        st.markdown(f"- **{test}:** {result}")
else:
    st.write("No lab tests recorded.")

st.markdown("---")  # Divider

# **Food Allergies**
st.subheader("🍎 Food Allergies")
if data.get("food_allergies"):
    st.markdown(", ".join(data["food_allergies"]))
else:
    st.write("No known food allergies.")

st.markdown("---")  # Divider

# **Lifestyle Factors - Pie Chart**
st.subheader("🏃 Lifestyle Factors")
lifestyle_icons = {
    "Smoking": "🚬", "Alcohol": "🍷", "Exercise": "🏋️‍♂️", "Sleep": "😴", "Stress": "😟"
}
lifestyle_values = [
    1 if data["lifestyle"]["smoking"] else 0,
    1 if data["lifestyle"]["alcohol"] else 0,
    {"None": 0, "Light": 1, "Moderate": 2, "Intense": 3}[data["lifestyle"]["exercise"]],
    data["lifestyle"]["sleep"],
    {"Low": 1, "Moderate": 2, "High": 3}[data["lifestyle"]["stress"]],
]

fig_lifestyle = px.pie(
    names=list(lifestyle_icons.keys()),
    values=lifestyle_values,
    hole=0.4,
    title="Lifestyle Breakdown",
    color_discrete_sequence=px.colors.qualitative.Set3,
)
st.plotly_chart(fig_lifestyle, use_container_width=True)

st.markdown("---")  # Divider

# **Current Symptoms - Bullet List**
st.subheader("🤒 Current Symptoms")
if data.get("current_symptoms"):
    for symptom in data["current_symptoms"]:
        st.markdown(f"- {symptom}")
else:
    st.write("No symptoms reported.")

st.markdown("---")  # Divider

# **Dietary Preferences**
st.subheader("🥗 Dietary Preferences")
st.markdown(f"🍽️ **Preference:** {data.get('dietary_preferences', 'No Preference')}")

st.markdown("---")  # Divider


# **Doctor’s Notes & Appointments**
st.subheader("📋 Doctor's Notes & Appointments")
st.write(data.get("doctor_recommendations", "No recommendations provided."))  # Uses default text if key is missing

