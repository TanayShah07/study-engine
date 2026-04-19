import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pickle
import os

FEATURES = ['hours_studied', 'sleep_hours', 'attendance_percent', 'previous_scores']
TARGET = 'performance_category'


def load_and_prepare(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.dropna()

    def categorise(score):
        if score >= 38:
            return 'Good'
        elif score >= 28:
            return 'Average'
        else:
            return 'At Risk'

    df[TARGET] = df['exam_score'].apply(categorise)
    return df


def train_models(csv_path: str, model_dir: str = '.'):
    df = load_and_prepare(csv_path)

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    os.makedirs(model_dir, exist_ok=True)

    with open(os.path.join(model_dir, 'best_model.pkl'), 'wb') as f:
        pickle.dump({
            'model': model,
            'scaler': scaler,
            'needs_scaling': False,
            'accuracy': acc
        }, f)

    return acc


def load_model(model_dir: str = '.'):
    with open(os.path.join(model_dir, 'best_model.pkl'), 'rb') as f:
        return pickle.load(f)


def predict_performance(hours_studied, sleep_hours, attendance_percent,
                         previous_scores, model_bundle):

    model = model_bundle['model']

    X = [[hours_studied, sleep_hours, attendance_percent, previous_scores]]

    prediction = model.predict(X)[0]

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[0]
        confidence = max(probs)
    else:
        confidence = None

    return {
        'category': prediction,
        'confidence': round(confidence * 100, 2) if confidence else None
    }