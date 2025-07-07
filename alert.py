import requests
from geopy.distance import geodesic


BOT_TOKEN = ""
CHAT_ID = ""  

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    return response.json()

current_location = (26.9124, 75.7873)


security_team = [
    ("John", (29.9135, 75.7890)),
    ("Asha", (26.9200, 75.8000)),
    ("Raj", (26.9100, 75.7800))
]

def find_nearest_security(location, team):
    return min(team, key=lambda p: geodesic(location, p[1]).meters)


voice_triggered = True

if voice_triggered:
    name, sec_loc = find_nearest_security(current_location, security_team)
    message = (
        f"🚨 *Emergency Alert!*\n"
        f"Help needed at location: {current_location}\n"
        f"Nearest responder: {name}"
    )
    print(f"Sending alert to Telegram for {name}...")
    response = send_telegram_alert(message)
    print("Telegram Response:", response)
else:
    print("No alert triggered.")
