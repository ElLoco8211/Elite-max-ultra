import sqlite3
from core.db import DB_PATH

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT SUM(profit) FROM bets")
    profit = c.fetchone()[0] or 0

    c.execute("SELECT COUNT(*) FROM bets")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM bets WHERE result='win'")
    wins = c.fetchone()[0]

    winrate = (wins / total * 100) if total > 0 else 0

    conn.close()

    return {
        "profit": round(profit, 2),
        "bets": total,
        "winrate": round(winrate, 2)
    }
