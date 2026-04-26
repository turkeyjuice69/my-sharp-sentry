import streamlit as st

# 1. FORCE THE LAYOUT TO MOBILE-PRO
st.set_page_config(page_title="SENTRY ELITE PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. THE SECRET SAUCE: CSS INJECTION
# This makes it look like an app, not a website.
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0E1117; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        color: #3E63DD;
        text-align: center;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 20px;
    }

    .bet-card {
        background: #1A1C24;
        border: 1px solid #2D3139;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    .team-name { font-size: 18px; font-weight: 700; color: white; }
    .badge {
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 900;
        margin-left: 5px;
    }
    .sharp { background: #00E676; color: black; }
    .whale { background: #D500F9; color: white; }
    .trap { background: #FF1744; color: white; }
    
    .money-flow { color: #00E676; font-size: 22px; font-weight: 800; }
    .label { color: #888DA8; font-size: 11px; text-transform: uppercase; }
    .discrepancy-box {
        background: #252833;
        padding: 8px;
        border-radius: 6px;
        margin-top: 10px;
        border-left: 3px solid #00E676;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MOCK DATA (This is where your scraper/API feed goes)
games = [
    {"icon": "🏀", "team": "Lakers", "opp": "Nuggets", "spread": "+4.5", "money": 78, "bets": 45, "avg": 850, "type": "SHARP"},
    {"icon": "🏈", "team": "Chiefs", "opp": "Bills", "spread": "-3.0", "money": 30, "bets": 82, "avg": 45, "type": "TRAP"},
    {"icon": "🏒", "team": "Rangers", "opp": "Devils", "spread": "ML", "money": 55, "bets": 52, "avg": 120, "type": "NONE"}
]

# 4. HEADER
st.markdown('<h1 class="main-title">SENTRY ELITE <span style="color:white">PRO UI</span></h1>', unsafe_allow_html=True)

# 5. THE RENDER LOOP
# We bundle the entire card into ONE st.markdown call to ensure it renders correctly.
for g in games:
    # Logic for badges
    badge_html = ""
    if g['type'] == "SHARP":
        badge_html = '<span class="badge sharp">SHARP</span>'
    elif g['type'] == "TRAP":
        badge_html = '<span class="badge trap">TRAP</span>'
    
    diff = g['money'] - g['bets']
    
    # THE BIG RENDER
    st.markdown(f"""
        <div class="bet-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 20px;">{g['icon']}</span>
                    <span class="team-name">{g['team']} <span style="color:#444; font-weight:400;">vs</span> {g['opp']}</span>
                </div>
                <div>{badge_html}</div>
            </div>
            
            <hr style="border: 0; border-top: 1px solid #2D3139; margin: 12px 0;">
            
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <div class="label">Actual Money Flow</div>
                    <div class="money-flow">{g['money']}%</div>
                    <div style="color:#555; font-size:12px;">from {g['bets']}% of bets</div>
                </div>
                <div style="text-align: right;">
                    <div class="label">Current Line</div>
                    <div style="font-size: 18px; font-weight: 700;">{g['spread']}</div>
                </div>
            </div>
            
            <div class="discrepancy-box">
                <span style="color: #00E676; font-size: 12px; font-weight: 600;">
                    ⚡ +{diff}% Money Discrepancy detected
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #444; font-size: 10px; margin-top: 20px;'>V3.2 | MASTER BOARD LIVE</p>", unsafe_allow_html=True)
