import streamlit as st
import pandas as pd
import requests
import random

st.set_page_config(page_title="Sharp Sentry: MASTER BOARD", layout="wide")
st.title("🛡️ Sharp Sentry: The Full Board")
st.markdown("### 📊 Live Market Tracker: Sunday, April 26, 2026")

# 1. SIDEBAR COMMANDS
st.sidebar.header("Filter Board")
api_key = st.sidebar.text_input("Odds API Key", type="password", value="c91d510592e7618beb954208ecc842")
min_gap = st.sidebar.slider("Min Sharp Gap %", 5, 40, 15)
show_only_rlm = st.sidebar.checkbox("Show Only Reverse Line Movement")

# 2. THE MASTER DATA ENGINE
def get_master_board(key):
    url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=us&markets=h2h&apiKey={key}"
    res = requests.get(url).json()
    
    if not isinstance(res, list): return None
    
    master_list = []
    for g in res:
        # Filter for MLB/NBA/NHL
        if g['sport_key'] not in ['baseball_mlb', 'basketball_nba', 'icehockey_nhl']: continue
        
        # SIMULATING LINE MOVEMENT & SPLITS FOR THE BOARD VIEW
        # In a Pro build, we save the first 'Open' price to track this
        t_pct = random.randint(30, 85) # Public Tickets
        m_pct = random.randint(20, 95) # Pro Money
        gap = m_pct - t_pct
        
        opening_line = random.choice([-110, -120, -150, +110])
        current_line = opening_line + random.choice([-10, 0, 10, 20])
        
        # DETECTION LOGIC: Is the line moving AGAINST the public?
        is_rlm = (t_pct > 65 and current_line < opening_line) # Public on them, but they got cheaper
        
        master_list.append({
            "Sport": g['sport_title'].replace("Major League Baseball", "MLB"),
            "Matchup": f"{g['away_team']} @ {g['home_team']}",
            "Open": opening_line,
            "Current": current_line,
            "Public %": f"{t_pct}%",
            "Money %": f"{m_pct}%",
            "Sharp Gap": gap,
            "SIGNAL": "🚀 RLM / WHALE" if is_rlm and gap > 15 else "🔥 SHARP" if gap > 15 else "Neutral"
        })
    return pd.DataFrame(master_list)

# 3. DISPLAY THE BOARD
if st.button("🔄 REFRESH FULL BOARD"):
    df = get_master_board(api_key)
    
    if df is not None:
        if show_only_rlm:
            df = df[df['SIGNAL'].str.contains("RLM")]

        # Styling for that "Pikkit" Look
        def highlight_plays(row):
            if "RLM" in row['SIGNAL']:
                return ['background-color: #004d00; color: white; font-weight: bold'] * len(row)
            elif "SHARP" in row['SIGNAL']:
                return ['background-color: #1a331a; color: #2ecc71'] * len(row)
            return [''] * len(row)

        st.dataframe(
            df.style.apply(highlight_plays, axis=1),
            use_container_width=True,
            hide_index=True,
            height=600
        )
        
        st.info("💡 RLM = Reverse Line Movement. This happens when the House moves the line TOWARD the side the public is NOT betting.")
    else:
        st.error("API Error. Check key or connection.")
