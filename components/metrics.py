import streamlit as st

def pixel_style_metric(label, value, delta=None, color="#4ECDC4"):
    """Display a metric in pixel art style"""
    delta_html = f"""<span style="color:{'green' if delta and delta > 0 else 'red' if delta and delta < 0 else 'gray'}; font-size: 1rem;">
        {"▲" if delta and delta > 0 else "▼" if delta and delta < 0 else "●"} {abs(delta) if delta else 0}%
    </span>""" if delta is not None else ""
    
    html = f"""
    <div style="
        background-color: {color};
        border: 3px solid #000000;
        box-shadow: 4px 4px 0px #000000;
        padding: 10px;
        margin: 5px;
        text-align: center;
        color: white;
    ">
        <div style="font-size: 1.2rem; margin-bottom: 5px; text-transform: uppercase;">{label}</div>
        <div style="font-size: 2rem; font-weight: bold;">{value}</div>
        {delta_html}
    </div>
    """
    return html