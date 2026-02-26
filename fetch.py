import requests
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

URL = "https://www.sofascore.com/api/v1/event/15453093/lineups"

print("Fetching data...")

players = []

try:
    r = requests.get(URL, headers=HEADERS, timeout=15)

    print("Status code:", r.status_code)

    if r.status_code != 200:
        raise Exception("Request blocked")

    data = r.json()

    # Güvenli erişim (KeyError YOK)
    for side in ["home", "away"]:
        side_data = data.get(side)

        if not side_data:
            print(f"{side} data missing")
            continue

        for p in side_data.get("players", []):
            rating = p.get("avgRating")

            if rating is None:
                continue

            players.append({
                "Player": p["player"]["name"],
                "Rating": rating
            })

except Exception as e:
    print("ERROR:", e)

# HER DURUMDA DOSYA YAZ
print("Players collected:", len(players))

with open("data/players.json", "w") as f:
    json.dump(players, f)

print("players.json updated.")
