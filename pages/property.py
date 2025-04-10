import streamlit as st
import random
from components.metrics import pixel_style_metric

def create_dashboard(properties_df):
    """Create the property analytics page with retro gaming aesthetic"""
    st.markdown("<h2>PROPERTY ANALYTICS POWER-UP</h2>", unsafe_allow_html=True)
    
    # Property selector as a game control
    selected_property = st.selectbox(
        "SELECT PROPERTY TO ANALYZE",
        options=properties_df["name"].tolist()
    )
    
    # Get property data
    prop_data = properties_df[properties_df["name"] == selected_property].iloc[0]
    
    # Display property stats in a game-like stats box
    st.markdown(f"""
    <div style="
        background-color: #2A2A72;
        border: 4px solid white;
        box-shadow: 6px 6px 0px black;
        padding: 15px;
        margin: 20px 0;
        color: white;
    ">
        <h3 style="text-align: center; color: #FF6B6B !important; margin-top: 0;">{prop_data['name']} STATS</h3>
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
            <div style="flex: 1; min-width: 120px; padding: 5px; text-align: center;">
                <div style="font-size: 14px; color: #4ECDC4;">TYPE</div>
                <div style="font-size: 20px;">{prop_data['type']}</div>
            </div>
            <div style="flex: 1; min-width: 120px; padding: 5px; text-align: center;">
                <div style="font-size: 14px; color: #4ECDC4;">LOCATION</div>
                <div style="font-size: 20px;">{prop_data['location']}</div>
            </div>
            <div style="flex: 1; min-width: 120px; padding: 5px; text-align: center;">
                <div style="font-size: 14px; color: #4ECDC4;">SIZE</div>
                <div style="font-size: 20px;">{prop_data['size_sqft']:,} SQFT</div>
            </div>
            <div style="flex: 1; min-width: 120px; padding: 5px; text-align: center;">
                <div style="font-size: 14px; color: #4ECDC4;">OCCUPANCY</div>
                <div style="font-size: 20px;">{int(prop_data['occupancy_rate']*100)}%</div>
            </div>
            <div style="flex: 1; min-width: 120px; padding: 5px; text-align: center;">
                <div style="font-size: 14px; color: #4ECDC4;">REVENUE/SQFT</div>
                <div style="font-size: 20px;">${prop_data['revenue_per_sqft']:.2f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create game-like progress bars for property metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3>PROPERTY PERFORMANCE LEVELS</h3>", unsafe_allow_html=True)
        
        # Energy Rating Bar
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between;">
                <span style="color: white; font-size: 18px;">ENERGY RATING</span>
                <span style="color: #FF6B6B; font-size: 18px;">{prop_data['energy_rating']}/100</span>
            </div>
            <div style="
                height: 25px;
                width: 100%;
                background-color: #556270;
                border: 3px solid black;
                margin-top: 5px;
            ">
                <div style="
                    height: 19px;
                    width: {prop_data['energy_rating']}%;
                    background-color: #FF6B6B;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Maintenance Score Bar
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between;">
                <span style="color: white; font-size: 18px;">MAINTENANCE SCORE</span>
                <span style="color: #4ECDC4; font-size: 18px;">{prop_data['maintenance_score']}/100</span>
            </div>
            <div style="
                height: 25px;
                width: 100%;
                background-color: #556270;
                border: 3px solid black;
                margin-top: 5px;
            ">
                <div style="
                    height: 19px;
                    width: {prop_data['maintenance_score']}%;
                    background-color: #4ECDC4;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Smart Devices Readiness
        smart_device_percent = min(100, int(prop_data['smart_devices'] * 2))
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between;">
                <span style="color: white; font-size: 18px;">SMART DEVICE READINESS</span>
                <span style="color: #FFE66D; font-size: 18px;">{smart_device_percent}/100</span>
            </div>
            <div style="
                height: 25px;
                width: 100%;
                background-color: #556270;
                border: 3px solid black;
                margin-top: 5px;
            ">
                <div style="
                    height: 19px;
                    width: {smart_device_percent}%;
                    background-color: #FFE66D;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>FINANCIAL PERFORMANCE</h3>", unsafe_allow_html=True)
        import plotly.graph_objects as go
        
        # Create sample revenue data
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        revenue = [
            prop_data['revenue_per_sqft'] * prop_data['size_sqft'] * (0.9 + random.uniform(-0.1, 0.1)) / 1000
            for _ in range(6)
        ]
        expenses = [rev * random.uniform(0.4, 0.6) for rev in revenue]
        profit = [rev - exp for rev, exp in zip(revenue, expenses)]
        
        # Create financial performance chart
        fig = go.Figure()
        
        # Revenue bars
        fig.add_trace(go.Bar(
            x=months,
            y=revenue,
            name="REVENUE",
            marker_color="#FF6B6B"
        ))
        
        # Expenses bars
        fig.add_trace(go.Bar(
            x=months,
            y=expenses,
            name="EXPENSES",
            marker_color="#556270"
        ))
        
        # Profit line
        fig.add_trace(go.Scatter(
            x=months,
            y=profit,
            mode="lines+markers",
            name="PROFIT",
            line=dict(color="#4ECDC4", width=4),
            marker=dict(size=10, symbol="square")
        ))
        
        # Update layout for retro gaming aesthetic
        fig.update_layout(
            title="MONTHLY PERFORMANCE (IN $K)",
            barmode="group",
            plot_bgcolor="#2A2A72",
            paper_bgcolor="#2A2A72",
            font=dict(family="VT323", size=14, color="white"),
            title_font=dict(family="VT323", size=20, color="white"),
            legend_title_font=dict(family="VT323"),
            legend_font=dict(family="VT323", size=12),
            xaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323")),
            yaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323")),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations section styled as power-ups
    st.markdown("<h3>PROPERTY POWER-UPS AVAILABLE</h3>", unsafe_allow_html=True)
    
    rec_cols = st.columns(3)
    
    with rec_cols[0]:
        st.markdown("""
        <div style="
            background-color: #FF6B6B;
            border: 3px solid black;
            box-shadow: 4px 4px 0px black;
            padding: 15px;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            color: white;
        ">
            <div>
                <h4 style="text-align: center; margin-top: 0;">⚡ ENERGY OPTIMIZER</h4>
                <p style="text-align: center; font-size: 14px;">
                    Install smart thermostats and LED lighting to reduce energy costs by 15-20%
                </p>
            </div>
            <div style="text-align: center;">
                <div style="
                    background-color: #FFE66D;
                    color: black;
                    display: inline-block;
                    padding: 5px 10px;
                    border: 2px solid black;
                    box-shadow: 2px 2px 0px black;
                ">
                    ROI: 128%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with rec_cols[1]:
        st.markdown("""
        <div style="
            background-color: #4ECDC4;
            border: 3px solid black;
            box-shadow: 4px 4px 0px black;
            padding: 15px;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            color: white;
        ">
            <div>
                <h4 style="text-align: center; margin-top: 0;">🔍 SPACE ANALYZER</h4>
                <p style="text-align: center; font-size: 14px;">
                    Deploy occupancy sensors to optimize space utilization and improve tenant experience
                </p>
            </div>
            <div style="text-align: center;">
                <div style="
                    background-color: #FFE66D;
                    color: black;
                    display: inline-block;
                    padding: 5px 10px;
                    border: 2px solid black;
                    box-shadow: 2px 2px 0px black;
                ">
                    ROI: 95%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with rec_cols[2]:
        st.markdown("""
        <div style="
            background-color: #9D65C9;
            border: 3px solid black;
            box-shadow: 4px 4px 0px black;
            padding: 15px;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            color: white;
        ">
            <div>
                <h4 style="text-align: center; margin-top: 0;">🔧 PREDICTIVE MAINTENANCE</h4>
                <p style="text-align: center; font-size: 14px;">
                    Implement predictive maintenance to reduce repair costs and extend equipment life
                </p>
            </div>
            <div style="text-align: center;">
                <div style="
                    background-color: #FFE66D;
                    color: black;
                    display: inline-block;
                    padding: 5px 10px;
                    border: 2px solid black;
                    box-shadow: 2px 2px 0px black;
                ">
                    ROI: 147%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)