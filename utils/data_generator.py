import plotly.graph_objects as go

def apply_retro_style_to_figure(fig, title=None):
    """Apply retro gaming styling to a plotly figure"""
    fig.update_layout(
        title=title,
        plot_bgcolor="#2A2A72",
        paper_bgcolor="#2A2A72",
        font=dict(family="VT323", size=14, color="white"),
        title_font=dict(family="VT323", size=24, color="white"),
        legend_title_font=dict(family="VT323", size=12),
        legend_font=dict(family="VT323", size=12),
        xaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323")),
        yaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323"))
    )
    return fig

def create_pixel_gauge(value, title, min_val=0, max_val=100, color="#4ECDC4", suffix=""):
    """Create a gauge chart with retro pixel styling"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": title, "font": {"family": "VT323", "size": 24}},
        gauge={
            "axis": {"range": [min_val, max_val], "tickfont": {"family": "VT323"}},
            "bar": {"color": color},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "black",
            "steps": [
                {"range": [min_val, min_val + (max_val-min_val)*0.5], "color": "lightgray"},
                {"range": [min_val + (max_val-min_val)*0.5, value], "color": color}
            ],
        },
        number={"font": {"family": "VT323", "size": 40}, "suffix": suffix}
    ))
    
    fig.update_layout(
        height=200,
        plot_bgcolor="#2A2A72",
        paper_bgcolor="#2A2A72",
        font={"family": "VT323", "color": "white"},
        margin=dict(l=30, r=30, t=50, b=30)
    )
    
    return fig