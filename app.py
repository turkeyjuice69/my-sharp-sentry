import streamlit as st
import pandas as pd
import requests
import random

st.set_page_config(page_title="Sharp Sentry: The Pro Board", layout="wide")
st.title("🛡️ Sharp Sentry: The Pro Board")

# --- 1. COMMAND CENTER ---
st.sidebar.header("Command Center")
odds_key = st.sidebar.text_input("Odds API Key", type="password", value="c91d510592e7618beb954208ecc842")
practice_mode = st.sidebar.toggle("Practice Mode (Simulated Splits)", value=True)

# --- 2. THE GRADING BRAIN ---
def get_pro_rating(gap, tickets, move):
    # A+ = Massive Money Gap + Reverse Line Movement
    if gap > 20 and move < 0:
        return "A+", "🏆 ELITE: Whales are move the line against the public."
    elif gap > 15:
        return "A", "🔥 SHARP: Strong pro-money confidence."
    elif gap > 8:
        return "B", "✅ VALUE: Smart money is leaning here."
    elif tickets > 70 and gap < -10:
        return "D", "⚠️ TRAP: The public is bait for the house."
    else:
        return "C", "Neutral: Market is currently efficient."

# --- 3. THE BOARD ENGINE ---
def load_board(api_key, is_practice):
    url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=us&markets=h2h&apiKey={api_key}"
    try:
        res = requests.get(url).json()
        if not isinstance(res, list): return None
        
        games = []
        for g in res:
            # We only want MLB, NBA, or NHL
            if g['sport_key'] not in ['baseball_mlb', 'basketball_nba', 'icehockey_nhl']:
                continue
            
            # THE DATA MATCH (Fixed the KeyError here)
            matchup_name = f"{g['away_team']} @ {g['home_team']}"
            
            # Splits & Movement Simulation (Until you connect the real VSiN scraper)
            t_pct = random.randint(30, 80)
            m_pct = random.randint(20, 95)
            gap = m_pct - t_pct
            move = random.choice([-10, -5, 0, 5, 10, 15]) # Price movement in cents
            
            grade, logic = get_pro_rating(gap, t_pct, move)
            
            games.append({
                "Grade": grade,
                "Matchup": matchup_name,
                "Public %": f"{t_pct}%",
                "Money %": f"{m_pct}%",
                "Move": f"{move}¢",
                "Logic": logic,
                "Sort": {"A+": 5, "A": 4, "B": 3, "C": 2, "D": 1}[grade]
            })
        return pd.DataFrame(games).sort_values("Sort", ascending=False)
    except:
        return None

# --- 4. THE UI ---
if st.button("🔄 REFRESH FULL BOARD"):
    df = load_board(odds_key, practice_mode)
    
    if df is not None and not df.empty:
        for _, row in df.iterrows():
            # Color coding for the grade
            g_color = "#2ecc71" if "A" in row['Grade'] else "#e74c3c" if "D" in row['Grade'] else "#f1c40f"
            
            with st.container(border=True):
                col1, col2, col3 = st.columns([1, 4, 3])
                with col1:
                    st.markdown(f"<h1 style='color: {g_color}; text-align: center;'>{row['Grade']}</h1>", unsafe_allow_html=True)
                with col2:
                    st.subheader(row['Matchup'])
                    st.write(f"**Public:** {row['Public %']} | **Money:** {row['Money %']} | **Move:** {row['Move']}")
                with col3:
                    st.info(row['Logic'])
    else:
        st.warning("No games found or API connection failed. Check your key!")
