import streamlit as st
import requests
import pandas as pd
from datetime import timedelta

st.title("⚽ Scout App - Top Rated Players")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# -----------------------------
# MATCH FETCH
# -----------------------------
def get_matches(date):

    urls = [
        f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{date}",
        f"https://www.sofascore.com/api/v1/sport/football/events/{date}"
    ]

    events = []

    for url in urls:
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            data = r.json()
            events.extend(data.get("events", []))

    return events


# -----------------------------
# LINEUPS
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
                "Rating": rating,
                "EventId": event_id
            })

    return players


# -----------------------------
# COLLECT
# -----------------------------
def collect_players(start_date, end_date, league_id):

    all_players = []
    current = start_date

    progress = st.progress(0)
    total_days = (end_date - start_date).days + 1
    step = 0

    while current <= end_date:

        date_str = current.strftime("%Y-%m-%d")
        matches = get_matches(date_str)

        st.write(f"{date_str} → matches found:", len(matches))

        for m in matches:

            league = (
                m.get("tournament", {})
                 .get("uniqueTournament", {})
                 .get("id")
            )

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
    "League ID (Premier League = 17)",
    value=17
)

if st.button("Analyze"):

    with st.spinner("Collecting players..."):

        df = collect_players(start_date, end_date, league_id)

        if df.empty:
            st.warning("No data found.")
        else:
            df = df.sort_values("Rating", ascending=False)

            st.success("Top players calculated!")

            st.dataframe(df.head(50), use_container_width=True)
