import streamlit as st
import plotly.graph_objects as go
from components.metrics import pixel_style_metric

def create_dashboard(iot_df):
    """Create the IoT monitoring dashboard with retro gaming aesthetic"""
    st.markdown("<h2>IoT CONTROL STATION</h2>", unsafe_allow_html=True)
    
    # Filter options that look like game controls
    col1, col2 = st.columns(2)
    
    with col1:
        sensor_type = st.selectbox(
            "SELECT SENSOR TYPE",
            options=sorted(iot_df["sensor_type"].unique())
        )
    
    with col2:
        location = st.selectbox(
            "SELECT ZONE",
            options=sorted(iot_df["location"].unique())
        )
    
    # Filter IoT data
    filtered_iot = iot_df[
        (iot_df["sensor_type"] == sensor_type) & 
        (iot_df["location"] == location)
    ]
    
    # Group by date and calculate average
    daily_avg = filtered_iot.groupby(filtered_iot["date"].dt.date)["value"].mean().reset_index()
    daily_avg["date_str"] = daily_avg["date"].astype(str)
    
    # Create pixel-style time series chart
    st.markdown("<h3>SENSOR READINGS OVER TIME</h3>", unsafe_allow_html=True)
    
    # Get unit for the selected sensor type
    unit = filtered_iot["unit"].iloc[0] if not filtered_iot.empty else ""
    
    # Determine color based on sensor type
    if sensor_type == "Temperature":
        color = "#FF6B6B"  # Red for temperature
    elif sensor_type == "Humidity":
        color = "#4ECDC4"  # Teal for humidity
    elif sensor_type == "Occupancy":
        color = "#FFE66D"  # Yellow for occupancy
    elif sensor_type == "Energy":
        color = "#9D65C9"  # Purple for energy
    else:  # Water
        color = "#556270"  # Gray for water
    
    # Create a pixel-like line chart
    fig = go.Figure()
    
    # Add line trace with square markers for pixel effect
    fig.add_trace(go.Scatter(
        x=daily_avg["date_str"],
        y=daily_avg["value"],
        mode="lines+markers",
        line=dict(color=color, width=3, shape="hv"),  # Step-like lines for pixel effect
        marker=dict(size=8, symbol="square"),
        name=sensor_type
    ))
    
    # Add a horizontal reference line
    fig.add_shape(
        type="line",
        x0=daily_avg["date_str"].iloc[0],
        y0=daily_avg["value"].mean(),
        x1=daily_avg["date_str"].iloc[-1],
        y1=daily_avg["value"].mean(),
        line=dict(color="white", width=2, dash="dot")
    )
    
    # Add annotation for the average
    fig.add_annotation(
        x=daily_avg["date_str"].iloc[-1],
        y=daily_avg["value"].mean(),
        text=f"AVG: {daily_avg['value'].mean():.1f} {unit}",
        showarrow=True,
        arrowhead=1,
        font=dict(family="VT323", size=14, color="white"),
        bgcolor="#2A2A72",
        bordercolor="white",
        borderwidth=2
    )
    
    # Update layout for retro gaming aesthetic
    fig.update_layout(
        title=f"{sensor_type.upper()} READINGS IN {location}",
        plot_bgcolor="#2A2A72",
        paper_bgcolor="#2A2A72",
        font=dict(family="VT323", size=14, color="white"),
        title_font=dict(family="VT323", size=24, color="white"),
        xaxis=dict(
            title="DATE",
            gridcolor="#556270",
            tickfont=dict(family="VT323"),
            tickangle=45
        ),
        yaxis=dict(
            title=f"{sensor_type.upper()} ({unit})",
            gridcolor="#556270",
            tickfont=dict(family="VT323")
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed sensor statistics in pixelated cards
    st.markdown("<h3>SENSOR STATS</h3>", unsafe_allow_html=True)
    
    stat_cols = st.columns(4)
    
    with stat_cols[0]:
        current_value = filtered_iot.iloc[-1]["value"] if not filtered_iot.empty else 0
        st.markdown(pixel_style_metric("CURRENT VALUE", f"{current_value:.1f} {unit}", None, color), unsafe_allow_html=True)
    
    with stat_cols[1]:
        avg_value = filtered_iot["value"].mean() if not filtered_iot.empty else 0
        st.markdown(pixel_style_metric("AVERAGE", f"{avg_value:.1f} {unit}", None, color), unsafe_allow_html=True)
    
    with stat_cols[2]:
        min_value = filtered_iot["value"].min() if not filtered_iot.empty else 0
        st.markdown(pixel_style_metric("MINIMUM", f"{min_value:.1f} {unit}", None, color), unsafe_allow_html=True)
    
    with stat_cols[3]:
        max_value = filtered_iot["value"].max() if not filtered_iot.empty else 0
        st.markdown(pixel_style_metric("MAXIMUM", f"{max_value:.1f} {unit}", None, color), unsafe_allow_html=True)
    
    # Anomaly detection section with pixel art style
    st.markdown("<h3>ANOMALY DETECTION</h3>", unsafe_allow_html=True)
    
    # Define anomalies (values that are significantly higher or lower than average)
    std_dev = filtered_iot["value"].std()
    mean_val = filtered_iot["value"].mean()
    threshold = 2  # Number of standard deviations to consider as anomaly
    
    anomalies = filtered_iot[
        (filtered_iot["value"] > mean_val + threshold * std_dev) | 
        (filtered_iot["value"] < mean_val - threshold * std_dev)
    ]
    
    if not anomalies.empty:
        # Create a table with retro gaming styling
        st.markdown("""
        <div style="
            background-color: #2A2A72;
            border: 3px solid white;
            box-shadow: 4px 4px 0px black;
            padding: 15px;
            margin-top: 10px;
            color: white;
        ">
            <h4 style="text-align: center; color: #FF6B6B; margin-top: 0;">ANOMALIES DETECTED</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #556270;">
                    <th style="padding: 8px; border: 2px solid white; text-align: center;">DATE</th>
                    <th style="padding: 8px; border: 2px solid white; text-align: center;">TIME</th>
                    <th style="padding: 8px; border: 2px solid white; text-align: center;">VALUE</th>
                    <th style="padding: 8px; border: 2px solid white; text-align: center;">DEVIATION</th>
                </tr>
        """, unsafe_allow_html=True)
        
        for _, row in anomalies.head(5).iterrows():
            date_str = row["date"].strftime("%Y-%m-%d")
            time_str = row["date"].strftime("%H:%M")
            value = row["value"]
            deviation = (value - mean_val) / std_dev
            deviation_str = f"{deviation:.2f}σ"
            
            # Determine row color based on deviation
            if deviation > 0:
                row_color = "#FF6B6B"  # Red for high values
            else:
                row_color = "#4ECDC4"  # Teal for low values
            
            st.markdown(f"""
            <tr style="background-color: {row_color}20;">
                <td style="padding: 8px; border: 2px solid white; text-align: center;">{date_str}</td>
                <td style="padding: 8px; border: 2px solid white; text-align: center;">{time_str}</td>
                <td style="padding: 8px; border: 2px solid white; text-align: center;">{value:.1f} {unit}</td>
                <td style="padding: 8px; border: 2px solid white; text-align: center; color: {row_color};">{deviation_str}</td>
            </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        # Add game-like button for anomaly investigation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("🔍 INVESTIGATE ANOMALIES 🔍", key="investigate_anomalies")
    else:
        st.markdown("""
        <div style="
            background-color: #4ECDC4;
            border: 3px solid black;
            box-shadow: 4px 4px 0px black;
            padding: 15px;
            margin-top: 10px;
            text-align: center;
            color: white;
        ">
            <h4 style="margin: 0;">ALL SYSTEMS NORMAL - NO ANOMALIES DETECTED</h4>
        </div>
        """, unsafe_allow_html=True)