import sqlite3
from core.db import DB_PATH

def get_roi_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT stake, profit FROM bets WHERE result IS NOT NULL
    """)

    rows = c.fetchall()
    conn.close()

    total_stake = sum(r[0] for r in rows)
    total_profit = sum(r[1] for r in rows)

    roi = (total_profit / total_stake) * 100 if total_stake > 0 else 0

    return {
        "bets": len(rows),
        "stake": round(total_stake, 2),
        "profit": round(total_profit, 2),
        "roi": round(roi, 2)
    }

def roi_by_type():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT bet_type, SUM(stake), SUM(profit)
    FROM bets
    WHERE result IS NOT NULL
    GROUP BY bet_type
    """)

    data = c.fetchall()
    conn.close()

    result = []

    for t, stake, profit in data:
        roi = (profit / stake) * 100 if stake else 0
        result.append({
            "type": t,
            "roi": round(roi, 2),
            "profit": round(profit, 2)
        })

    return result
