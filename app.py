import streamlit as st
import pandas as pd
import requests
import random

# --- 1. THE WINNER'S SETTINGS ---
st.set_page_config(page_title="Sharp Sentry: PRO BOARD", layout="wide")
st.title("🛡️ Sharp Sentry: The Pro Board")

st.sidebar.header("💰 Bankroll Management")
total_bankroll = st.sidebar.number_input("Your Total Bankroll ($)", value=1000, step=100)
unit_size = st.sidebar.slider("Standard Unit Size (%)", 1.0, 5.0, 2.0)
st.sidebar.divider()

odds_key = st.sidebar.text_input("Odds API Key", type="password", value="c91d510592e7618beb954208ecc842")
practice_mode = st.sidebar.toggle("🛠️ Practice Mode", value=True)

# --- 2. THE UNIT SIZER ---
def get_bet_recommendation(grade, bankroll, base_unit_pct):
    # Professional sizing: More confidence = more units
    multiplier = {"A+": 2.5, "A": 1.5, "B": 1.0, "C": 0.5, "D": 0.0}
    recom_pct = (base_unit_pct / 100) * multiplier.get(grade, 0)
    return f"${bankroll * recom_pct:,.2f} ({multiplier.get(grade)} Units)"

# --- 3. THE MASTER DATA ENGINE ---
def load_board(key, is_practice):
    if is_practice:
        # REAL matchups for Sunday, April 26, 2026
        data = [
            {"Matchup": "Lakers @ Rockets (Game 4)", "Sport": "NBA"},
            {"# Matchup": "Phillies @ Braves", "Sport": "MLB"},
            {"Matchup": "Yankees @ Astros", "Sport": "MLB"},
            {"Matchup": "Cubs @ Dodgers", "Sport": "MLB"},
            {"Matchup": "Celtics @ 76ers (Game 4)", "Sport": "NBA"}
        ]
        games = []
        for d in data:
            t_pct = random.randint(30, 85)
            m_pct = random.randint(20, 95)
            gap = m_pct - t_pct
            move = random.choice([-15, -10, 0, 10, 20])
            
            # THE GRADING BRAIN
            if gap > 20 and move < 0: grade, logic = "A+", "ELITE: Massive RLM detected. Pros vs Joes."
            elif gap > 12: grade, logic = "A", "SHARP: Pros are unloading. Strong +EV signal."
            elif gap > 5: grade, logic = "B", "VALUE: Professional lean. Solid for parlay legs."
            elif t_pct > 75 and gap < -10: grade, logic = "D", "TRAP: Public is blind-betting. FADE THIS."
            else: grade, logic = "C", "NEUTRAL: Market is efficient. No clear edge."
            
            games.append({"Grade": grade, "Matchup": d['Matchup'], "Public": t_pct, "Money": m_pct, "Move": move, "Logic": logic})
        return pd.DataFrame(games)
    
    # Real data fetch (same as before)
    return None # Will populate Sunday Morning!

# --- 4. DISPLAY THE BOARD ---
if st.button("🔄 REFRESH FULL BOARD"):
    df = load_board(odds_key, practice_mode)
    if df is not None:
        df['sort'] = df['Grade'].map({"A+": 5, "A": 4, "B": 3, "C": 2, "D": 1})
        df = df.sort_values("sort", ascending=False)
        
        for _, row in df.iterrows():
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([1, 2, 2, 3])
                with c1:
                    st.markdown(f"<h1 style='text-align: center; color: #2ecc71;'>{row['Grade']}</h1>", unsafe_allow_html=True)
                with c2:
                    st.subheader(row['Matchup'])
                    st.write(f"Public: {row['Public']}% | Move: {row['Move']}¢")
                with c3:
                    # THE MONEY MAKER: UNIT SIZING
                    bet_amt = get_bet_recommendation(row['Grade'], total_bankroll, unit_size)
                    st.metric("Suggested Bet", bet_amt)
                with c4:
                    st.info(row['Logic'])
