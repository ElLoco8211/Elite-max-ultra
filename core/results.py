import random
from core.db import update_result
import sqlite3
from core.db import DB_PATH

def update_all_results():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT id FROM matches WHERE result IS NULL")
    matches = c.fetchall()

    for m in matches:
        match_id = m[0]

        # simulazione risultato (per ora)
        result = random.choice(["home", "draw", "away"])

        update_result(match_id, result)
        print(f"Aggiornato match {match_id} → {result}")

    conn.close()

import sqlite3

def calculate_roi():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT stake, odd, result FROM bets WHERE result IS NOT NULL")
    rows = c.fetchall()

    conn.close()

    profit = 0
    total_stake = 0

    for stake, odd, result in rows:
        total_stake += stake

        if result == "win":
            profit += stake * (odd - 1)
        elif result == "lose":
            profit -= stake

    roi = (profit / total_stake) if total_stake > 0 else 0

    return round(roi, 3), round(profit, 2)
