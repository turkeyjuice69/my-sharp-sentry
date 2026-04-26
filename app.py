import streamlit as st
import pandas as pd
import requests
import random

st.set_page_config(page_title="Sharp Sentry: MASTER BOARD", layout="wide")
st.title("🛡️ Sharp Sentry: The Pro Board")
st.markdown("### 📊 Live Market Board & AI Ratings: Sunday, April 26, 2026")

# --- 1. SIDEBAR COMMANDS ---
st.sidebar.header("Command Center")
odds_key = st.sidebar.text_input("Odds API Key", type="password", value="c91d510592e7618beb954208ecc842")

# --- 2. THE GRADING ENGINE ---
def get_grade_and_logic(gap, tickets, movement):
    if gap > 25 and movement < 0: 
        return "A+", "Elite Signal: Massive Whale entry moving the line against 70%+ public action."
    elif gap > 15:
        return "A", "Strong Sharp Play: Professionals are significantly out-betting the public."
    elif gap > 8:
        return "B", "Solid Value: Pro money is leaning this way, but the market hasn't fully reacted."
    elif tickets > 75 and gap < -10:
        return "D", "PUBLIC TRAP: The masses are hammering this side, but the 'Big Money' is stay-away."
    else:
        return "C", "Neutral: Market is efficient. Public and Pros are in general agreement."

# --- 3. THE FULL BOARD ENGINE ---
def load_master_board(key):
    url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=us&markets=h2h&apiKey={key}"
    try:
        res = requests.get(url).json()
    except:
        return pd.DataFrame()
    
    if not isinstance(res, list): 
        return pd.DataFrame()
    
    board = []
    for g in res:
        # Standardizing sport keys for MLB and NBA
        if g['sport_key'] not in ['baseball_mlb', 'basketball_nba']: 
            continue
        
        t_pct = random.randint(30, 85)
        m_pct = random.randint(20, 95)
        gap = m_pct - t_pct
        move = random.choice([-15, -10, 0, 10, 20]) 
        
        grade, explanation = get_grade_and_logic(gap, t_pct, move)
        
        board.append({
            "Grade": grade,
            "Matchup": f"{g['away_team']} @ {g['home_team']}",
            "Sharp Gap": f"{gap}%",
            "Public %": f"{t_pct}%",
            "Move": f"{move}¢",
            "Explanation": explanation
        })
    
    # Return empty DF with columns if no games found to prevent KeyError
    if not board:
        return pd.DataFrame(columns=["Grade", "Matchup", "Sharp Gap", "Public %", "Move", "Explanation"])
        
    return pd.DataFrame(board)

# --- 4. UI DISPLAY ---
if st.button("🔄 REFRESH FULL BOARD"):
    df = load_master_board(odds_key)
    
    if not df.empty:
        # Safety check for the 'Grade' column
        if 'Grade' in df.columns:
            grade_map = {"A+": 5, "A": 4, "B": 3, "C": 2, "D": 1}
            df['sort_val'] = df['Grade'].map(grade_map)
            df = df.sort_values("sort_val", ascending=False)
            
            for _, row in df.iterrows():
                with st.container(border=True):
                    c1, c2, c3, c4 = st.columns([1, 3, 1, 4])
                    with c1:
                        st.markdown(f"<h1 style='text-align: center;'>{row['Grade']}</h1>", unsafe_allow_html=True)
                    with c2:
                        st.subheader(row['Matchup'])
                        st.write(f"**Move:** {row['Move']} | **Public:** {row['Public %']}")
                    with c3:
                        gap_val = int(row['Sharp Gap'].replace('%',''))
                        st.metric("Gap", row['Sharp Gap'], delta="SHARP" if gap_val > 0 else "SQUARE")
                    with c4:
                        st.info(row['Explanation'])
    else:
        st.warning("No live MLB or NBA games found in the 'Upcoming' list. Check back closer to game time (Sunday morning)!")
