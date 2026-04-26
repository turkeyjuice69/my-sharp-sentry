import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Sharp Sentry: ULTIMATE", layout="wide", page_icon="🏦")
st.title("🏦 Sharp Sentry Elite: ULTIMATE MODE")
st.write("Current Status: **Live Vegas Feed + Real Handle Matching**")

# Sidebar
api_key = st.sidebar.text_input("Odds API Key", value="5d4cf99b3f6534bb71758274380ba7f") # Your key from the photo
threshold = st.sidebar.slider("Sharp Gap Trigger (%)", 10, 30, 15)

# --- THE REAL DATA SCRAPER ---
def get_vsin_splits():
    try:
        url = "https://vsin.com/betting-splits/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        tables = pd.read_html(res.text)
        
        splits = {}
        for t in tables:
            # Look for the Moneyline splits table
            if 'ML Bets %' in str(t.columns):
                for _, row in t.iterrows():
                    team = str(row.iloc[0]).lower()
                    # Clean up the team name for matching
                    team = re.sub(r'[^a-z]', '', team)
                    splits[team] = {
                        "bets": int(str(row.iloc[-2]).replace('%','')),
                        "money": int(str(row.iloc[-1]).replace('%',''))
                    }
        return splits
    except:
        return None

# --- THE MATCHING ENGINE ---
if st.button("🔥 EXECUTE MARKET RECON"):
    with st.spinner("Analyzing Vegas handles..."):
        # 1. Fetch Odds
        odds_url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=us&markets=h2h&oddsFormat=american&apiKey={api_key}"
        odds_data = requests.get(odds_url).json()
        
        # 2. Fetch Real Splits
        real_splits = get_vsin_splits()
        
        if isinstance(odds_data, list):
            final_view = []
            for game in odds_data:
                home = game['home_team']
                # Try to find a match in the real splits
                clean_home = re.sub(r'[^a-z]', '', home.lower())
                
                # Match logic
                match = None
                for team_key in real_splits.keys() if real_splits else []:
                    if team_key in clean_home or clean_home in team_key:
                        match = real_splits[team_key]
                        break
                
                if match:
                    gap = match['money'] - match['bets']
                    verdict = "Neutral"
                    if gap >= threshold: verdict = "🔥 SHARP PLAY"
                    if gap >= 25: verdict = "🐳 WHALE ALERT"
                    if match['bets'] > 70 and gap < -10: verdict = "⚠️ PUBLIC TRAP"
                    
                    final_view.append({
                        "Matchup": f"{game['away_team']} @ {game['home_team']}",
                        "Public %": match['bets'],
                        "Pro %": match['money'],
                        "Gap": gap,
                        "VERDICT": verdict
                    })
            
            if final_view:
                df = pd.DataFrame(final_view)
                def color_rows(row):
                    if "SHARP" in row['VERDICT'] or "WHALE" in row['VERDICT']:
                        return ['background-color: #004d00; color: white'] * len(row)
                    if "TRAP" in row['VERDICT']:
                        return ['background-color: #4d0000; color: white'] * len(row)
                    return [''] * len(row)
                
                st.table(df.style.apply(color_rows, axis=1))
            else:
                st.warning("Found games, but Vegas hasn't released the money handles for them yet. Check back closer to tip-off/first pitch.")
        else:
            st.error("API Connection Error. Verify your key.")