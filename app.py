import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.markdown("""
    <style>
    header {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

from model import train_models, load_model, predict_performance
from utils import (
    analyse_subjects,
    allocate_study_time,
    generate_timetable,
    generate_recommendations,
    validate_inputs,
    compute_average_previous_score
)

st.set_page_config(
    page_title="Study Buddy Bot",
    layout="centered"
)

MODEL_DIR = "."
CSV_PATH = "student_exam_scores.csv"
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")


@st.cache_resource
def get_model():
    if not os.path.exists(MODEL_PATH):
        train_models(CSV_PATH, MODEL_DIR)
    return load_model(MODEL_DIR)


st.title("Study Engine")
st.write("ML-based academic performance analyzer and timetable generator")


attendance = st.number_input("Attendance (%)", 0.0, 100.0, step=0.5)
hours = st.number_input("Study hours per day", 0.5, 16.0, step=0.5)
sleep = st.number_input("Sleep hours per night", 3.0, 12.0, step=0.5)

num_subjects = st.number_input("Number of subjects", 1, 8, step=1)

subjects = []

st.subheader("Enter Subject Details")

for i in range(int(num_subjects)):
    st.markdown(f"### Subject {i+1}")
    name = st.text_input(f"Name {i+1}", key=f"name{i}")
    mark = st.number_input(f"Marks {i+1}", 0.0, 100.0, key=f"mark{i}")
    difficulty = st.selectbox(
        f"Difficulty {i+1}",
        ["Easy", "Medium", "Hard"],
        key=f"diff{i}"
    )

    if name:
        subjects.append({
            "name": name,
            "mark": mark,
            "difficulty": difficulty
        })


if st.button("Run Analysis"):

    valid, err = validate_inputs(attendance, hours, sleep, subjects)

    if not valid:
        st.error(err)

    else:
        model_bundle = get_model()

        avg_score = compute_average_previous_score(subjects)

        prediction = predict_performance(
            hours,
            sleep,
            attendance,
            avg_score,
            model_bundle
        )

        analysed = analyse_subjects(subjects)
        allocated = allocate_study_time(analysed, hours)
        timetable = generate_timetable(allocated)

        recs = generate_recommendations(
            prediction['category'],
            allocated,
            hours,
            sleep,
            attendance
        )

        st.subheader("Performance Prediction")
        st.success(f"Predicted Category: {prediction['category']}")

        if prediction.get('confidence'):
            st.write(f"Confidence: {prediction['confidence']}%")

        st.write("Model Used: Random Forest Classifier")

        st.subheader("Insights")
        st.write("Study hours, attendance, and previous performance are key factors influencing prediction.")

        st.subheader("Subject Analysis")

        df = pd.DataFrame([{
            "Subject": s['name'],
            "Marks": s['mark'],
            "Difficulty": s['difficulty'],
            "Level": s['classification'],
            "Study Time": s['time_display']
        } for s in allocated])

        st.dataframe(df, use_container_width=True)

        st.subheader("Marks Overview")

        fig, ax = plt.subplots()
        ax.bar(df["Subject"], df["Marks"])
        ax.set_ylabel("Marks")
        ax.set_title("Subject Marks")

        st.pyplot(fig)

        st.subheader("Study Timetable")

        for t in timetable:
            st.write(
                f"{t['subject']} | {t['start']} - {t['end']} | {t['duration']}"
            )

        st.subheader("Time Distribution")

        fig2, ax2 = plt.subplots()
        ax2.pie(
            [s['allocated_hours'] for s in allocated],
            labels=[s['name'] for s in allocated],
            autopct='%1.1f%%'
        )

        st.pyplot(fig2)

        st.subheader("Recommendations")

        for r in recs:
            st.write(f"- {r}")