import streamlit as st
import pandas as pd
import json

st.title("⚽ Scout App - Top Rated Players")

try:
    with open("data/players.json") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    if df.empty:
        st.warning("No data yet.")
    else:
        df = df.sort_values("Rating", ascending=False)
        st.dataframe(df.head(50), use_container_width=True)

except:
    st.error("Data file not found.")
