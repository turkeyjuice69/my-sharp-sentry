import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="SENTRY ELITE PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM PRO UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Card Styling */
    .stMetric {
        background: #1A1C24;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #2D3139;
    }
    
    /* Master Board Card */
    .bet-card {
        background: linear-gradient(145deg, #1e2129, #16181d);
        border-radius: 15px;
        padding: 18px;
        margin-bottom: 15px;
        border-left: 5px solid #3E63DD;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Badge Logic Colors */
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 900;
        font-size: 10px;
        text-transform: uppercase;
        margin-right: 5px;
    }
    .sharp { background-color: #00E676; color: #000; }
    .whale { background-color: #D500F9; color: #fff; }
    .trap { background-color: #FF1744; color: #fff; }
    
    /* Money Discrepancy Highlight */
    .money-flow {
        font-size: 18px;
        font-weight: 700;
        color: #00E676;
    }
    .market-price {
        color: #888DA8;
        font-size: 14px;
        text-decoration: line-through;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC: BADGE GENERATOR ---
def get_badges(row):
    badges = []
    # SHARP: High handle on low bet count
    if row['money_pct'] - row['bets_pct'] > 15:
        badges.append('<span class="badge sharp">SHARP</span>')
    # WHALE: massive individual tickets
    if row['avg_bet'] > 500:
        badges.append('<span class="badge whale">WHALE</span>')
    # TRAP: Public heavy one way, line moving the other
    if row['bets_pct'] > 70 and row['line_movement'] == "Reverse":
        badges.append('<span class="badge trap">TRAP</span>')
    return "".join(badges)

# --- MOCK DATA (Replace with your API/Scraper) ---
data = [
    {"team": "Lakers", "opp": "Nuggets", "spread": "+4.5", "money_pct": 78, "bets_pct": 45, "avg_bet": 850, "line_movement": "Stable", "icon": "🏀"},
    {"team": "Chiefs", "opp": "Bills", "spread": "-3.0", "money_pct": 30, "bets_pct": 82, "avg_bet": 45, "line_movement": "Reverse", "icon": "🏈"},
    {"team": "Rangers", "opp": "Devils", "spread": "ML", "money_pct": 55, "bets_pct": 52, "avg_bet": 120, "line_movement": "Stable", "icon": "🏒"},
]

# --- MAIN UI ---
st.markdown("<h1 style='text-align: center; color: #3E63DD;'>SENTRY ELITE <span style='color:white'>PRO UI</span></h1>", unsafe_allow_html=True)

for game in data:
    badges_html = get_badges(game)
    discrepancy = game['money_pct'] - game['bets_pct']
    
    with st.container():
        st.markdown(f"""
        <div class="bet-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 20px;">{game['icon']}</span>
                    <span style="font-weight: 700; font-size: 18px; margin-left: 8px;">{game['team']} vs {game['opp']}</span>
                </div>
                <div>
                    {badges_html}
                </div>
            </div>
            
            <hr style="border: 0.5px solid #2D3139; margin: 15px 0;">
            
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <p style="color: #888DA8; font-size: 12px; margin-bottom: 2px;">ACTUAL MONEY FLOW</p>
                    <span class="money-flow">{game['money_pct']}%</span> 
                    <span style="font-size: 12px; color: #444;">({game['bets_pct']}% Bets)</span>
                </div>
                <div style="text-align: right;">
                    <p style="color: #888DA8; font-size: 12px; margin-bottom: 2px;">PROJECTION</p>
                    <span style="font-weight: 700;">{game['spread']}</span>
                </div>
            </div>
            
            <div style="margin-top: 10px; background: #0E1117; border-radius: 8px; padding: 10px;">
                <span style="font-size: 12px; color: #00E676;">⚡ Discrepancy: +{discrepancy}% more money than public bets</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<p style='text-align: center; color: #444; font-size: 10px;'>SENTRY ELITE V3.0 | LIVE PRO DATA FEED</p>", unsafe_allow_html=True)
