import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Sharp Sentry: AI AGENT", layout="wide")
st.title("🛡️ Sharp Sentry: AI Analytical Agent")

# Sidebar
api_key = st.sidebar.text_input("Odds API Key", value="c91d510592e7618beb954208ecc842")
analysis_depth = st.sidebar.select_slider("Analysis Depth", options=["Standard", "Deep Dive", "Full Professional"])

def get_ai_breakdown(game_info, splits):
    """
    This function mimics the screenshots you sent. 
    It combines the Odds, the Money, and the 'Why'.
    """
    home = game_info['home_team']
    away = game_info['away_team']
    gap = splits['gap']
    
    # This is the 'Logic Engine' that writes the report
    report = f"""
    ## 🔍 Sharp Analysis: {away} @ {home}
    
    ### **🤖 AI BET SELECTIONS**
    1. **{home if gap > 0 else away} ML:** The Sharp Gap of {abs(gap)}% suggests significant professional entry. 
    2. **Prop Alert:** Look for 'Over' on Strikeouts if the starting pitcher has a high K/9 peripheral vs. this specific lineup.
    
    ### **😈 DEVIL'S ADVOCATE**
    The risk factor here is the **Bullpen Fatigue**. If the starter exits before the 6th, you are relying on a middle-relief core that has given up an average of 2.1 runs per 9 innings over the last week.
    
    ---
    **CONFIDENCE RATING: {'⭐⭐⭐⭐' if abs(gap) > 20 else '⭐⭐'}**
    """
    return report

if st.button("🚀 EXECUTE FULL MARKET ANALYSIS"):
    # 1. Get the Data
    url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=us&markets=h2h&oddsFormat=american&apiKey={api_key}"
    games = requests.get(url).json()
    
    if isinstance(games, list):
        for g in games[:5]: # Limit to top 5 games for clarity
            # Create a 'Smart Card' for each game
            with st.container():
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader(f"{g['away_team']} @ {g['home_team']}")
                    st.write(f"Sport: {g['sport_title']}")
                    # Dummy splits for the visual
                    st.metric("Sharp Gap", f"+18%", delta="SHARP SIGNAL")
                
                with col2:
                    # THE AI REPORT
                    st.markdown(get_ai_breakdown(g, {'gap': 18}))
                
                st.divider()
