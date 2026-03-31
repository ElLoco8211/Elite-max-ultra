import sqlite3
from pathlib import Path

DB_PATH = "elite.db"
DB_PATH = Path("data/database.db")
DB_PATH.parent.mkdir(exist_ok=True)

def init_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        home TEXT,
        away TEXT,
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS bets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        bet_type TEXT,
        odd REAL,
        edge REAL,
        stake REAL,
        result TEXT,
        profit REAL
    )
    """)

    conn.commit()
    conn.close()


def save_match(match):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("INSERT INTO matches (home, away) VALUES (?, ?)",
              (match["home"], match["away"]))

    match_id = c.lastrowid
    conn.commit()
    conn.close()
    return match_id


def save_bet(match_id, bet):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT INTO bets (match_id, bet_type, odd, edge, stake)
    VALUES (?, ?, ?, ?, ?)
    """, (match_id, bet["type"], bet["odd"], bet["edge"], bet["stake"]))

    conn.commit()
    conn.close()

    
def update_result(match_id, result):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # salva risultato match
    c.execute("UPDATE matches SET result=? WHERE id=?", (result, match_id))

    # prendi bets
    c.execute("SELECT id, bet_type, odd, stake FROM bets WHERE match_id=?", (match_id,))
    bets = c.fetchall()

    for b in bets:
        bet_id, bet_type, odd, stake = b

        if bet_type == result:
            profit = stake * (odd - 1)
            res = "win"
        else:
            profit = -stake
            res = "lose"

        c.execute("UPDATE bets SET result=?, profit=? WHERE id=?", (res, profit, bet_id))

    conn.commit()
    conn.close()
