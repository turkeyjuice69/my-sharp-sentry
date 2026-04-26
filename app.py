import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Sharp Sentry: ULTIMATE", layout="wide")
st.title("🛡️ Sharp Sentry Elite: ULTIMATE MODE")

# --- COMMAND CENTER ---
st.sidebar.header("Command Center")
api_key = st.sidebar.text_input("Odds API Key", value="39744d8cdba2dcddd047b442d7488f8")
debug_mode = st.sidebar.toggle("🔍 Diagnostic Mode (See Raw Data)")
gap_trigger = st.sidebar.slider("Sharp Gap Trigger (%)", 5, 30, 12)

# --- THE REAL-TIME SCRAPER ---
def get_vsin_splits():
    try:
        url = "https://vsin.com/betting-splits/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        # We grab the tables from the live VSiN site
        tables = pd.read_html(res.text)
        
        all_splits = []
        for t in tables:
            # Look for MLB/NBA/NHL tables
            if any(col in str(t.columns) for col in ['ML Bets', 'Handle', '%']):
                for _, row in t.iterrows():
                    try:
                        all_splits.append({
                            "Team": str(row.iloc[0]).strip(),
                            "Bets": str(row.iloc[-2]).replace('%',''),
                            "Money": str(row.iloc[-1]).replace('%','')
                        })
                    except: continue
        return all_splits
    except:
        return []

# --- MATCHING LOGIC ---
def is_match(api_name, split_name):
    # This logic handles "L.A. Dodgers" vs "Dodgers"
    a = api_name.lower().split()[-1] # Grabs just "Dodgers"
    b = split_name.lower()
    return a in b

# --- MAIN RECON ---
if st.button("🚀 EXECUTE MARKET RECON"):
    with st.spinner("Syncing Vegas Matrix..."):
        # 1. Fetch Live Odds
        odds_url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=us&markets=h2h&oddsFormat=american&apiKey={api_key}"
        odds_data = requests.get(odds_url).json()
        
        # 2. Fetch Live Handles
        vsin_data = get_vsin_splits()
        
        if debug_mode:
            st.write("### 🔍 Diagnostic: Raw Vegas Data")
            st.write(vsin_data if vsin_data else "No data found on VSiN yet.")

        if isinstance(odds_data, list) and vsin_data:
            matches = []
            for game in odds_data:
                # We focus on the Big 3: MLB, NBA, NHL
                if any(x in game['sport_key'] for x in ['baseball', 'basketball', 'icehockey']):
                    for split in vsin_data:
                        if is_match(game['home_team'], split['Team']):
                            try:
                                m_pct = int(split['Money'])
                                b_pct = int(split['Bets'])
                                gap = m_pct - b_pct
                                
                                matches.append({
                                    "Sport": game['sport_title'],
                                    "Matchup": f"{game['away_team']} @ {game['home_team']}",
                                    "Bets %": f"{b_pct}%",
                                    "Money %": f"{m_pct}%",
                                    "Sharp Gap": gap,
                                    "Verdict": "🔥 WHALE" if gap >= 20 else "✅ SHARP" if gap >= gap_trigger else "Neutral"
                                })
                            except: continue
            
            if matches:
                df = pd.DataFrame(matches)
                def color_rows(row):
                    if "WHALE" in row['Verdict']: return ['background-color: #004d00; color: white'] * len(row)
                    if "SHARP" in row['Verdict']: return ['background-color: #1e4620; color: white'] * len(row)
                    return [''] * len(row)
                
                st.table(df.style.apply(color_rows, axis=1))
                st.success("Recon Complete. Follow the green.")
            else:
                st.warning("Found games, but Vegas hasn't released the money handles for them yet. Check back closer to tip-off.")
        else:
            st.error("Connection Error: Check API Key or try again in 5 minutes.")
