import streamlit as st
import requests
import pandas as pd

st.title("⚽ Scout App - Top Rated Players")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# -----------------------------
# GET LEAGUE EVENTS (WORKING ENDPOINT)
# -----------------------------
def get_league_events(league_id):

    url = f"https://www.sofascore.com/api/v1/unique-tournament/{league_id}/events/last/50"

    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        st.write("League fetch failed:", r.status_code)
        return []

    return r.json().get("events", [])


# -----------------------------
# GET LINEUPS
# -----------------------------
def get_lineups(event_id):

    url = f"https://www.sofascore.com/api/v1/event/{event_id}/lineups"

    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        return []

    data = r.json()
    players = []

    for side in ["home", "away"]:
        for p in data.get(side, {}).get("players", []):

            rating = p.get("avgRating")

            if rating is None:
                continue

            players.append({
                "Player": p["player"]["name"],
                "Rating": rating
            })

    return players


# -----------------------------
# COLLECT PLAYERS
# -----------------------------
def collect_players(league_id):

    events = get_league_events(league_id)

    st.write("Matches found:", len(events))

    all_players = []

    for e in events:
        event_id = e["id"]
        players = get_lineups(event_id)
        all_players.extend(players)

    return pd.DataFrame(all_players)


# -----------------------------
# UI
# -----------------------------
league_id = st.number_input(
    "League ID (Premier League = 17)",
    value=17
)

if st.button("Analyze"):

    with st.spinner("Collecting players..."):

        df = collect_players(league_id)

        if df.empty:
            st.warning("No data found.")
        else:
            df = df.sort_values("Rating", ascending=False)

            st.success("Top players calculated!")

            st.dataframe(df.head(50), use_container_width=True)
