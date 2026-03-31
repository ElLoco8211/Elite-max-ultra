import requests

TOKEN = "TUO_TOKEN"
CHAT_ID = "TUO_CHAT_ID"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
