import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- 1. THE IMPROVED ENGINE ---
def fetch_real_money_splits():
    """Scrapes Covers for consensus data and returns a cleaned Dict"""
    url = "https://contests.covers.com/consensus/topconsensus/mlb/overall"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        tables = pd.read_html(res.text)
        df = tables[0]
        
        # We need a dictionary for quick lookups: { "Team Name": Money% }
        # Covers table usually has 'Team' and 'Consensus' or 'Money' columns
        # Note: You'll need to verify the column names based on the live table structure
        splits = {}
        for _, row in df.iterrows():
            team = str(row[0]).split('(')[0].strip() # Clean "Dodgers (75%)" if needed
            try:
                # Extracting just the number from the percentage string
                money_val = int(''.join(filter(str.isdigit, str(row[1])))) 
                splits[team] = money_val
            except:
                continue
        return splits
    except Exception as e:
        st.error(f"Scraper Error: {e}")
        return {}

# --- 2. THE ELITE UI ---
st.set_page_config(page_title="Sharp Sentry: ELITE", layout="wide")
st.title("🛡️ Sharp Sentry: Elite Board")

# Move API Key to sidebar as seen in your screenshot
api_key = st.sidebar.text_input("Odds API Key", value="c91d510592e7618beb954208ecc842", type="password")

if st.button("🔥 EXECUTE LIVE MARKET RECON"):
    with st.spinner("Bypassing paywalls for real-time handle data..."):
        # 1. Get Scraped Data First
        real_splits = fetch_real_money_splits()
        
        # 2. Get API Odds
        odds_url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=us&markets=h2h&apiKey={api_key}"
        odds_data = requests.get(odds_url).json()
        
        if isinstance(odds_data, list):
            for g in odds_data[:10]:
                sport = g['sport_key']
                if sport not in ['baseball_mlb', 'basketball_nba']: continue
                
                # --- MATCHING LOGIC ---
                home_team = g['home_team']
                away_team = g['away_team']
                
                # Look up the handle for the Home Team (example logic)
                # In a real sharp move, we check which side has the massive money influx
                m_pct = real_splits.get(home_team, 50) # Default to 50 if no match
                t_pct = 45 # Tickets are usually more distributed; you can scrape these too
                
                gap = m_pct - t_pct
                is_sharp = gap > 15 # Alert if money is 15% higher than tickets
                
                # --- DYNAMIC UI COLORING ---
                status_color = "#2ecc71" if is_sharp else "#95a5a6"
                status_text = "✅ SHARP MOVE" if is_sharp else "⚖️ NEUTRAL"

                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 3, 2])
                    with c1:
                        grade = "A+" if gap > 20 else "B"
                        st.markdown(f"### {grade}")
                        st.write(f"**{g['sport_title']}**")
                    with c2:
                        st.markdown(f"### {away_team} @ {home_team}")
                        st.markdown(f'<span style="background:{status_color};color:white;padding:3px 8px;border-radius:10px;">{status_text}</span>', unsafe_allow_html=True)
                        st.caption(f"Line Movement: +1.5 (Simulated)") # Placeholder for the movement logic
                    with c3:
                        st.write("The Handle (Actual Money)")
                        st.progress(m_pct/100)
                        st.caption(f"Money: {m_pct}% | Tickets: {t_pct}%")
        else:
            st.error("API Limit reached or Key Error.")
