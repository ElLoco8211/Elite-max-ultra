# main.py
import sqlite3
from core.db import DB_PATH, init_db, save_match, save_bet
from core.value_multi import find_value_multi
from core.ai_training import train_model
from core.analytics import get_roi_stats, roi_by_type
from core.telegram import send

# Init DB prima!
init_db()

# Train AI
train_model()

# MOCK match (sostituirai con scraper)
matches = [
    {
        "home": "Juventus",
        "away": "Milan",
        "bookmakers": {
            "book1": {"home": 2.4, "draw": 3.2, "away": 2.8},
            "book2": {"home": 2.35, "draw": 3.1, "away": 2.9}
        }
    },
    {
        "home": "Inter",
        "away": "Napoli",
        "bookmakers": {
            "book1": {"home": 2.5, "draw": 3.0, "away": 2.9},
            "book2": {"home": 2.41, "draw": 3.05, "away": 2.95}
        }
    }
]

# LOOP MATCH
for m in matches:
    print(f"\n{m['home']} vs {m['away']}")

    values = find_value_multi(m)

    if not values:
        print("❌ Nessuna value")
    else:
        match_id = save_match(m)

        for v in values:
            save_bet(match_id, v)

            print(f"💰 {v['type']} @ {v['odd']} ({v['book']})")
            print(f"📊 EDGE: {v['edge']} | PROB: {v['prob']}")
            print(f"💵 STAKE (Kelly): {v['stake']}€")

            # 🚀 TELEGRAM ALERT
            msg = f"{m['home']} vs {m['away']}\n💰 {v['type']} @ {v['odd']} EDGE {v['edge']}"
            send(msg)

            print("------------------------------")

# ======================
# DASHBOARD PRO
# ======================

stats = get_roi_stats()

print("\n⚽ ELITE MAX PRO DASHBOARD")
print(f"💰 Profitto: {stats['profit']}€")
print(f"📊 ROI: {stats['roi']}%")
print(f"🎯 Bets: {stats['bets']}")

print("\n📈 Performance per tipo:")
for r in roi_by_type():
    print(f"{r['type']} → ROI {r['roi']}% | Profit {r['profit']}€")


