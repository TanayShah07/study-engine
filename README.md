# Study Engine

*A machine learning system for predicting performance and planning studies.*

---

## Overview

This project is an intelligent academic assistance system that analyzes student performance and generates a structured study plan. It uses machine learning techniques to predict performance and combines it with a rule-based scheduling approach to allocate study time efficiently.

---

## Features

- Academic performance prediction using machine learning  
- Subject-wise analysis based on marks and difficulty  
- Personalized study time allocation  
- Automated timetable generation  
- Data visualization (charts and insights)  

---

## Technologies Used

- Python  
- Streamlit  
- Scikit-learn  
- Pandas  
- Matplotlib  

---

## Project Structure
```bash
study-engine/
│── app.py # Main Streamlit application
│── model.py # Machine learning model training and prediction
│── utils.py # Analysis, scheduling, and recommendation logic
│── student_exam_scores.csv # Dataset
│── best_model.pkl # Trained model
│── requirements.txt # Project dependencies
```

---

## How to Run

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```
### 2. Run the application:
```bash
streamlit run app.py
```
---

## Machine Learning Approach

The system uses supervised learning (Random Forest) to predict student performance based on:

- Study hours  
- Sleep hours  
- Attendance  
- Previous scores  

The prediction is then used to guide study planning and time allocation.

---

## Output

- Predicted performance category  
- Subject-level analysis  
- Personalized study timetable  
- Visual insights (charts)  

---

## Authors

- Neerav Reddy  
- Sonia Mascarenhas  
- Sukhada Gulhane  
- Tanay Shah  

---

## Note

This project focuses on combining machine learning with practical scheduling logic to create a simple and interpretable academic planning system.
