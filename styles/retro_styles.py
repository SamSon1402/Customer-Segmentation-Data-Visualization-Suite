import streamlit as st

def apply_styles():
    """Apply retro gaming aesthetic styles to the application"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono&display=swap');
        
        /* Main Retro Gaming Styles */
        * {
            font-family: 'VT323', monospace;
        }
        
        code {
            font-family: 'Space Mono', monospace;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-family: 'VT323', monospace !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 3px 3px 0px #000000;
        }
        
        h1 {
            color: #FF6B6B !important;
            font-size: 3rem !important;
        }
        
        h2 {
            color: #4ECDC4 !important;
            font-size: 2rem !important;
        }
        
        h3 {
            color: #FFE66D !important;
            font-size: 1.5rem !important;
        }
        
        /* Card styling with pixel borders */
        .css-1r6slb0, .css-1wrcr25 {
            background-color: #2A2A72;
            border: 4px solid #ffffff;
            border-radius: 0px !important;
            box-shadow: 6px 6px 0px #000000;
            padding: 5px;
        }
        
        /* Button styling */
        .stButton > button {
            font-family: 'VT323', monospace !important;
            background-color: #FF6B6B;
            color: white;
            border: 3px solid #000000;
            border-radius: 0px;
            box-shadow: 3px 3px 0px #000000;
            transition: all 0.1s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stButton > button:hover {
            transform: translate(2px, 2px);
            box-shadow: 1px 1px 0px #000000;
        }
        
        /* Metric styling */
        .css-1xarl3l, .css-1offfwp {
            font-family: 'VT323', monospace !important;
            background-color: #4ECDC4;
            border: 3px solid #000000;
            border-radius: 0px;
            box-shadow: 3px 3px 0px #000000;
            padding: 10px;
        }
        
        /* Custom styling for sidebar */
        .css-1d391kg, .css-1lcbmhc {
            background-color: #2A2A72;
            background-image: linear-gradient(180deg, #2A2A72 0%, #009FFD 100%);
        }
        
        .css-1wrcr25 {
            background-color: transparent;
        }
        
        /* Make plots more pixel-like */
        .js-plotly-plot {
            border: 4px solid #ffffff;
            box-shadow: 6px 6px 0px #000000;
        }

        /* Custom progress bar */
        .stProgress > div > div {
            background-color: #FF6B6B;
            border-radius: 0px;
        }
        
        .stProgress {
            height: 20px;
        }
    </style>
    """, unsafe_allow_html=True)