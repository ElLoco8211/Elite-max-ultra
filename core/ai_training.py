# core/ai_training.py
import sqlite3
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from core.db import DB_PATH
from pathlib import Path

MODEL_PATH = Path("data/model.pkl")
MODEL_PATH.parent.mkdir(exist_ok=True)

def train_model():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT odd, edge, result
    FROM bets
    WHERE result IS NOT NULL
    """)

    data = c.fetchall()
    conn.close()

    if len(data) < 20:
        print("❌ Troppi pochi dati")
        return None

    X = []
    y = []

    for odd, edge, result in data:
        X.append([odd, edge])
        y.append(1 if result == "win" else 0)

    model = LogisticRegression()
    model.fit(np.array(X), np.array(y))

    joblib.dump(model, MODEL_PATH)
    print("✅ AI allenata (multi-feature)")
    return model

def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None

def predict_prob(odd, edge):
    model = load_model()
    if model:
        return model.predict_proba([[odd, edge]])[0][1]
    return 0.5
