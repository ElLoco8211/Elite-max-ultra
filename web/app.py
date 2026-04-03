import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from flask import Flask, render_template
import sqlite3
import os
from core.db import DB_PATH, init_db
from core.analytics import get_roi_stats

init_db()

app = Flask(__name__)

# 🔥 METTI QUI LA FUNZIONE
def get_profit_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT profit FROM bets WHERE result IS NOT NULL")
    rows = c.fetchall()
    conn.close()

    profits = []
    total = 0

    for r in rows:
        total += r[0] or 0
        profits.append(total)

    return profits


@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT m.home, m.away, b.bet_type, b.odd, b.stake, b.result, b.profit
    FROM bets b
    JOIN matches m ON b.match_id = m.id
    ORDER BY b.id DESC
    LIMIT 50
    """)

    bets = c.fetchall()
    conn.close()

    stats = get_roi_stats()
    profits = get_profit_history()

    return render_template("index.html", bets=bets, stats=stats, profits=profits)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
