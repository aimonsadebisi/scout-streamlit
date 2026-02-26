import requests
import json
import os

OUTPUT = "data/players.json"

EVENT_ID = 12437786  # GUARANTEED DATA MATCH

url = f"https://api.sofascore.com/api/v1/event/{EVENT_ID}/lineups"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

r = requests.get(url, headers=headers)

print("STATUS:", r.status_code)

data = r.json()

print("KEYS:", data.keys())

players = []

for side in ["home", "away"]:
    team = data.get(side)

    if not team:
        print("NO TEAM:", side)
        continue

    for p in team.get("players", []):
        stats = p.get("statistics")

        if not stats:
            continue

        rating = stats.get("rating")

        if rating:
            players.append({
                "Player": p["player"]["name"],
                "Rating": float(rating)
            })

os.makedirs("data", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(players, f, indent=2)

print("TOTAL PLAYERS:", len(players))
