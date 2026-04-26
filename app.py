import streamlit as st
import requests
import time

# --- 1. UI CONFIG ---
st.set_page_config(page_title="Sharp Sentry: ELITE", layout="wide")

st.markdown("""
    <style>
    .sharp-badge { background-color: #2ecc71; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .whale-badge { background-color: #f1c40f; color: black; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .trap-badge { background-color: #e74c3c; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sharp Sentry: Live Market Discrepancies")
st.sidebar.header("Command Center")
st.sidebar.write("Tracking Pinnacle (Sharp) vs. DraftKings (Public)")

# --- 2. MATH ENGINE ---
def get_implied_prob(odds):
    """Converts American odds to implied probability percentage."""
    if odds > 0:
        return 100 / (odds + 100) * 100
    else:
        return abs(odds) / (abs(odds) + 100) * 100

def get_pro_badge(edge):
    if edge > 4.0: return '<span class="whale-badge">⭐ MASSIVE EDGE</span>', "A+"
    if edge > 2.0: return '<span class="sharp-badge">✅ SHARP MOVE</span>', "A"
    if edge < -2.0: return '<span class="trap-badge">⚠️ PUBLIC TRAP</span>', "D"
    return "", "B"

# --- 3. LIVE DATA ENGINE ---
@st.cache_data(ttl=120) # Caches data for 2 minutes to save API requests
def fetch_live_odds():
    try:
        api_key = st.secrets["ODDS_API_KEY"]
        # Fetching odds specifically from Pinnacle (eu) and DraftKings (us)
        url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=us,eu&markets=h2h&bookmakers=pinnacle,draftkings&oddsFormat=american&apiKey={api_key}"
        return requests.get(url).json()
    except Exception as e:
        return {"error": str(e)}

# --- 4. EXECUTION ---
if st.button("🚀 EXECUTE LIVE RECON"):
    with st.spinner("Intercepting global sportsbook lines..."):
        data = fetch_live_odds()
        
    if isinstance(data, dict) and "error" in data:
        st.error(f"System Failure: Check API Key or limits. ({data['error']})")
    else:
        processed_games = []
        
        for game in data:
            pinny_odds = {}
            dk_odds = {}
            
            # Extract bookmaker data
            for book in game.get("bookmakers", []):
                if book["key"] == "pinnacle":
                    pinny_odds = {out["name"]: out["price"] for out in book["markets"][0]["outcomes"]}
                elif book["key"] == "draftkings":
                    dk_odds = {out["name"]: out["price"] for out in book["markets"][0]["outcomes"]}
            
            # If both books have a line on this game, compare them
            if pinny_odds and dk_odds:
                for team, p_line in pinny_odds.items():
                    if team in dk_odds:
                        dk_line = dk_odds[team]
                        p_prob = get_implied_prob(p_line)
                        dk_prob = get_implied_prob(dk_line)
                        
                        # Edge = What the sharp book says vs what the public book offers
                        edge = p_prob - dk_prob
                        badge_html, grade = get_pro_badge(edge)
                        
                        if abs(edge) >= 1.5: # Only show games with notable discrepancies
                            processed_games.append({
                                "sport": game["sport_title"],
                                "matchup": f"{game['away_team']} @ {game['home_team']}",
                                "target_team": team,
                                "p_line": p_line,
                                "dk_line": dk_line,
                                "edge": round(edge, 2),
                                "badge": badge_html,
                                "grade": grade
                            })
        
        # Sort by the biggest edge first
        processed_games.sort(key=lambda x: x['edge'], reverse=True)

        if not processed_games:
            st.info("Market is tight right now. No major sharp discrepancies detected.")
            
        for item in processed_games:
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 2])
                
                with col1:
                    st.markdown(f"### {item['grade']}")
                    st.write(f"**{item['sport']}**")
                
                with col2:
                    st.markdown(f"**{item['matchup']}**")
                    st.markdown(item['badge'], unsafe_allow_html=True)
                    st.write(f"Target: **{item['target_team']}**")
                
                with col3:
                    st.write("**The Line Discrepancy**")
                    st.write(f"Sharp (Pinnacle): `{item['p_line']}`")
                    st.write(f"Public (DraftKings): `{item['dk_line']}`")
                
                with st.expander("📝 View Sharp Analysis"):
                    st.write(f"""
                    **The Logic:** Pinnacle has priced {item['target_team']} at {item['p_line']}, implying a tighter probability than DraftKings' line of {item['dk_line']}. 
                    This creates a **{item['edge']}% mathematical edge**. The public money is likely holding the DraftKings line down, creating value.
                    """)
                st.divider()
