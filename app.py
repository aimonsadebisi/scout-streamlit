import streamlit as st
import requests
import pandas as pd
from datetime import timedelta

st.title("⚽ Scout App - Top Rated Players")

# -----------------------------
# API FUNCTIONS
# -----------------------------

def get_matches(date):
    url = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{date}"
    r = requests.get(url)

    if r.status_code != 200:
        return []

    return r.json()["events"]


def get_lineups(event_id):
    url = f"https://www.sofascore.com/api/v1/event/{event_id}/lineups"
    r = requests.get(url)

    if r.status_code != 200:
        return []

    data = r.json()

    players = []

    for side in ["home", "away"]:
        for p in data[side]["players"]:

            rating = p.get("avgRating")

            if rating is None:
                continue

            players.append({
                "Player": p["player"]["name"],
                "Rating": rating,
                "TeamId": p["teamId"],
                "EventId": event_id
            })

    return players


def collect_players(start_date, end_date, league_id):

    all_players = []

    current = start_date

    progress = st.progress(0)
    total_days = (end_date - start_date).days + 1
    step = 0

    while current <= end_date:

        matches = get_matches(current.strftime("%Y-%m-%d"))

        for m in matches:

            try:
                league = m["tournament"]["uniqueTournament"]["id"]
            except:
                continue

            if league != league_id:
                continue

            event_id = m["id"]

            players = get_lineups(event_id)
            all_players.extend(players)

        current += timedelta(days=1)

        step += 1
        progress.progress(step / total_days)

    return pd.DataFrame(all_players)


# -----------------------------
# UI
# -----------------------------

start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

league_id = st.number_input(
    "League ID (Example: Premier League = 17)",
    value=17
)

if st.button("Analyze"):

    with st.spinner("Collecting players..."):

        df = collect_players(start_date, end_date, league_id)

        if df.empty:
            st.warning("No data found.")
        else:
            df = df.sort_values("Rating", ascending=False)

            top50 = df.head(50)

            st.success("Top 50 players found!")

            st.dataframe(top50, use_container_width=True)
