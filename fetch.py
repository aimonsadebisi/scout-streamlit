from playwright.sync_api import sync_playwright
import json
import os

OUTPUT = "data/players.json"

URL = "https://www.sofascore.com/tr/futbol/mac/fenerbahce-nottingham-forest/osclb#id:15453093"

players = []
captured = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # API response yakala
    def handle_response(response):
        if "lineups" in response.url:
            try:
                captured.append(response.json())
            except:
                pass

    page.on("response", handle_response)

    page.goto(URL)

    # SAYFA TAM YÜKLENSİN
    page.wait_for_timeout(5000)

    # ✅ LINEUPS TABINA TIKLA
    try:
        page.get_by_text("Kadro").click(timeout=5000)
    except:
        try:
            page.get_by_text("Lineups").click(timeout=5000)
        except:
            pass

    # API çağrısı için bekle
    page.wait_for_timeout(8000)

    browser.close()

# ---- DATA PARSE ----
for data in captured:
    for side in ["home", "away"]:
        team = data.get(side)
        if not team:
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

print("Players:", len(players))
