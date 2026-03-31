# core/ai_training.py
import sqlite3
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from core.db import DB_PATH
from pathlib import Path
from core.filter import is_good_bet

MODEL_PATH = Path("data/model.pkl")
MODEL_PATH.parent.mkdir(exist_ok=True)

def train_model():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Prendi bets con risultato
    c.execute("""
    SELECT b.odd, CASE WHEN b.result='win' THEN 1 ELSE 0 END
    FROM bets b
    WHERE b.result IS NOT NULL
    """)
    data = c.fetchall()
    conn.close()

    if len(data) < 20:
        print("❌ Troppi pochi dati per training")
        return None

    X = np.array([[row[0]] for row in data])
    y = np.array([row[1] for row in data])

    model = LogisticRegression()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print("✅ Modello AI allenato!")
    return model

def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None

def predict_prob(odd):
    model = load_model()
    if model:
        return model.predict_proba([[odd]])[0][1]  # probabilità di vincita
    else:
        return 0.5  # fallback neutro

from core.ai_training import predict_prob
from core.kelly import kelly_stake

BANKROLL = 100  # capitale iniziale

def find_value_multi(match):
    values = []
    books = match.get("bookmakers", {})

    for outcome in ["home", "draw", "away"]:
        best_odd = 0
        best_book = None

        for b in books:
            try:
                odd = books[b][outcome]
            except:
                continue

            if odd > best_odd:
                best_odd = odd
                best_book = b

        if best_odd == 0:
            continue

        # prima edge grezzo
        base_prob = 1 / best_odd
        base_edge = (base_prob * best_odd) - 1

        # AI migliorata
        prob = predict_prob(best_odd, base_edge)
        edge = (prob * best_odd) - 1

        if is_good_bet(edge, prob, best_odd):
            stake = kelly_stake(prob, best_odd, BANKROLL)

            values.append({
                "type": outcome,
                "odd": best_odd,
                "book": best_book,
                "edge": round(edge, 3),
                "prob": round(prob, 3),
                "stake": stake
            })

    return values
