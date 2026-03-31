import os
import joblib

MODEL_PATH = "data/model.pkl"

def predict(odd):
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        prob = model.predict_proba([[odd]])[0][1]
        return prob

    return 0.5  # fallback
