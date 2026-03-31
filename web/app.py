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

    return render_template("index.html", bets=bets, stats=stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
