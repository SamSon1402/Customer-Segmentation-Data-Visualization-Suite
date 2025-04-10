import streamlit as st

def create_pixel_art_header():
    """Creates a pixel art header for the dashboard"""
    st.markdown("""
    <div style="text-align:center; padding: 10px; margin-bottom: 20px;">
        <h1>PROPTECH-8BIT ANALYTICS</h1>
        <div style="font-family: 'VT323', monospace; font-size: 20px; letter-spacing: 2px; color: #FFE66D;">
            STRATEGIC PROPTECH IMPLEMENTATION FOR OPERATIONAL EFFICIENCY
        </div>
    </div>
    """, unsafe_allow_html=True)