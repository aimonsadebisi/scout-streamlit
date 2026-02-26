import requests, json

HEADERS={"User-Agent":"Mozilla/5.0"}

url="https://www.sofascore.com/api/v1/event/15453093/lineups"

r=requests.get(url,headers=HEADERS)

players=[]

data=r.json()

for side in ["home","away"]:
    for p in data[side]["players"]:
        if "avgRating" in p:
            players.append({
                "Player":p["player"]["name"],
                "Rating":p["avgRating"]
            })

with open("data/players.json","w") as f:
    json.dump(players,f)
