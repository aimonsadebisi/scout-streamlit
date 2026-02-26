import requests
import json
import os

OUTPUT = "data/players.json"

# TEST MATCH (public working match id)
EVENT_ID = 15453093

url = f"https://api.sofascore.com/api/v1/event/{EVENT_ID}/lineups"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

r = requests.get(url, headers=headers)

if r.status_code != 200:
    print("Request failed:", r.status_code)
    exit()

data = r.json()

players = []

# ---- SAFE PARSE ----
for side in ["home", "away"]:
    if side not in data:
        continue

    for player in data[side]["players"]:
        rating = player.get("statistics", {}).get("rating")

        if rating:
            players.append({
                "Player": player["player"]["name"],
                "Rating": float(rating)
            })

# save
os.makedirs("data", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(players, f, indent=2)

print("Players saved:", len(players))
