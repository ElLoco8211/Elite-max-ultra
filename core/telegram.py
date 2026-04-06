import requests

TOKEN = "8775591684:AAGnS_KoD1y482if4NUdPWWXe8uzFQZ0zgo"
CHAT_ID = "8775591684"


def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        })
    except Exception as e:
        print("Errore Telegram:", e)


def send_value_alert(match, bet):
    # filtro edge (solo value forti)
    if bet["edge"] < 0.05:
        return

    msg = f"""
🔥 *VALUE BET*

⚽ {match['home']} vs {match['away']}

💰 *{bet['type'].upper()}* @ {bet['odd']}
📊 Edge: {bet['edge']}
💵 Stake: {bet['stake']}€
"""

    send(msg)
