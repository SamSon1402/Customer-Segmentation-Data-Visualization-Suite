import streamlit as st
from datetime import datetime, timedelta

def create_game_menu():
    """Creates a retro game-like menu in the sidebar"""
    st.sidebar.markdown("""
    <div style="text-align:center; margin-bottom: 20px;">
        <h2 style="color:#FF6B6B !important; text-shadow: 2px 2px 0px #000000;">GAME MENU</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create menu options that look like game menu items
    menu_selection = st.sidebar.radio("",
        options=[
            "🏢 Executive Dashboard",
            "🔍 Property Analytics",
            "🤖 IoT Systems",
            "👥 Tenant Insights",
            "📊 Predictive Models"
        ],
        index=0
    )
    
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div style="text-align:center; margin-top: 20px; margin-bottom: 10px;">
        <h3 style="color:#4ECDC4 !important; text-shadow: 2px 2px 0px #000000;">GAME CONTROLS</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Date range slider that looks like a game controller
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    
    date_range = st.sidebar.date_input(
        "SELECT TIMEFRAME",
        value=(start_date, end_date),
        max_value=datetime.now()
    )
    
    # Property filter as a game-like dropdown
    properties = [f"Property {chr(65 + i)}{i}" for i in range(10)]
    selected_properties = st.sidebar.multiselect(
        "SELECT PROPERTIES",
        options=properties,
        default=properties[:3]
    )
    
    # Add a power button style control
    st.sidebar.markdown("""
    <div style="text-align:center; margin-top: 30px;">
        <button style="
            font-family: 'VT323', monospace;
            background-color: #FF6B6B;
            color: white;
            border: 3px solid #000000;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            box-shadow: 3px 3px 0px #000000;
            cursor: pointer;
            font-size: 24px;
        ">
            ⏻
        </button>
        <p style="margin-top: 5px; color: #FFE66D;">REFRESH DATA</p>
    </div>
    """, unsafe_allow_html=True)
    
    return menu_selection, date_range, selected_properties