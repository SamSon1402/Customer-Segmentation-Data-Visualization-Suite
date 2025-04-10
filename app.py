import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import base64
from PIL import Image
import io

# ==== PAGE CONFIGURATION ====
st.set_page_config(
    page_title="PROPTECH-8BIT",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==== CUSTOM CSS FOR RETRO GAMING AESTHETIC ====
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

# ==== HELPER FUNCTIONS ====

def generate_sample_property_data(num_properties=10):
    """Generate sample property data for demo purposes"""
    property_types = ["Residential", "Commercial", "Retail", "Industrial", "Mixed-Use"]
    cities = ["New York", "San Francisco", "Chicago", "Miami", "Austin", "Seattle", "Boston"]
    
    data = {
        "property_id": [f"PROP-{i:03d}" for i in range(1, num_properties + 1)],
        "name": [f"Property {chr(65 + i % 26)}{i}" for i in range(1, num_properties + 1)],
        "type": [random.choice(property_types) for _ in range(num_properties)],
        "location": [random.choice(cities) for _ in range(num_properties)],
        "size_sqft": [random.randint(5000, 100000) for _ in range(num_properties)],
        "occupancy_rate": [random.uniform(0.7, 1.0) for _ in range(num_properties)],
        "revenue_per_sqft": [random.uniform(20, 100) for _ in range(num_properties)],
        "energy_rating": [random.randint(50, 100) for _ in range(num_properties)],
        "smart_devices": [random.randint(5, 50) for _ in range(num_properties)],
        "maintenance_score": [random.randint(60, 100) for _ in range(num_properties)]
    }
    
    return pd.DataFrame(data)

def generate_iot_sensor_data(num_days=30, num_sensors=5):
    """Generate sample IoT sensor data"""
    date_range = [datetime.now() - timedelta(days=i) for i in range(num_days)]
    date_range.reverse()
    
    sensor_types = ["Temperature", "Humidity", "Occupancy", "Energy", "Water"]
    
    data = []
    for date in date_range:
        for sensor_id in range(1, num_sensors + 1):
            # Base values for each sensor type
            if sensor_types[sensor_id-1] == "Temperature":
                base_value = 72  # Fahrenheit
                fluctuation = 5
                unit = "°F"
            elif sensor_types[sensor_id-1] == "Humidity":
                base_value = 45  # Percent
                fluctuation = 10
                unit = "%"
            elif sensor_types[sensor_id-1] == "Occupancy":
                base_value = 65  # Percent
                fluctuation = 20
                unit = "%"
            elif sensor_types[sensor_id-1] == "Energy":
                base_value = 30  # kWh
                fluctuation = 15
                unit = "kWh"
            else:  # Water
                base_value = 120  # Gallons
                fluctuation = 30
                unit = "gal"
            
            # Add some time-based patterns and randomness
            hour_factor = 1 + 0.2 * np.sin(2 * np.pi * date.hour / 24)
            day_factor = 1 + 0.1 * np.sin(2 * np.pi * date.weekday() / 7)
            random_factor = 1 + random.uniform(-0.1, 0.1)
            
            value = base_value * hour_factor * day_factor * random_factor
            # Add a controlled fluctuation
            value = value + random.uniform(-fluctuation, fluctuation)
            
            # Create anomalies occasionally (1% chance)
            if random.random() < 0.01:
                value = value * random.uniform(1.5, 2.0)
            
            data.append({
                "date": date,
                "sensor_id": f"S-{sensor_id:03d}",
                "sensor_type": sensor_types[sensor_id-1],
                "value": value,
                "unit": unit,
                "location": f"Zone-{random.randint(1, 3)}"
            })
    
    return pd.DataFrame(data)

def generate_tenant_data(num_tenants=20):
    """Generate sample tenant data"""
    business_types = ["Retail", "Office", "Restaurant", "Medical", "Tech", "Financial"]
    lease_terms = [1, 2, 3, 5, 10]
    
    data = {
        "tenant_id": [f"TEN-{i:03d}" for i in range(1, num_tenants + 1)],
        "name": [f"Tenant {chr(65 + i % 26)}{i}" for i in range(1, num_tenants + 1)],
        "business_type": [random.choice(business_types) for _ in range(num_tenants)],
        "lease_term_years": [random.choice(lease_terms) for _ in range(num_tenants)],
        "lease_start": [datetime.now() - timedelta(days=random.randint(30, 1000)) for _ in range(num_tenants)],
        "monthly_rent": [random.randint(2000, 15000) for _ in range(num_tenants)],
        "space_utilized_sqft": [random.randint(1000, 10000) for _ in range(num_tenants)],
        "satisfaction_score": [random.randint(60, 100) for _ in range(num_tenants)],
        "retention_probability": [random.uniform(0.6, 0.95) for _ in range(num_tenants)],
        "service_requests_monthly": [random.randint(0, 10) for _ in range(num_tenants)]
    }
    
    df = pd.DataFrame(data)
    # Calculate lease end dates
    df['lease_end'] = df.apply(lambda row: row['lease_start'] + timedelta(days=int(row['lease_term_years']*365)), axis=1)
    return df

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
    properties_df = generate_sample_property_data()
    selected_properties = st.sidebar.multiselect(
        "SELECT PROPERTIES",
        options=properties_df["name"].tolist(),
        default=properties_df["name"].tolist()[:3]
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

def create_executive_dashboard(properties_df, iot_df, tenants_df):
    """Create the executive dashboard with retro gaming aesthetic"""
    st.markdown("<h2>EXECUTIVE COMMAND CENTER</h2>", unsafe_allow_html=True)
    
    # Key Metrics in Retro Gaming Style
    col1, col2, col3, col4 = st.columns(4)
    
    avg_occupancy = f"{round(properties_df['occupancy_rate'].mean() * 100)}%"
    avg_energy = f"{round(properties_df['energy_rating'].mean())}/100"
    total_revenue = f"${round(sum(properties_df['revenue_per_sqft'] * properties_df['size_sqft']) / 1000)}K"
    tenant_satisfaction = f"{round(tenants_df['satisfaction_score'].mean())}/100"
    
    with col1:
        st.markdown(pixel_style_metric("Occupancy", avg_occupancy, 5, "#FF6B6B"), unsafe_allow_html=True)
    with col2:
        st.markdown(pixel_style_metric("Energy Rating", avg_energy, -2, "#4ECDC4"), unsafe_allow_html=True)
    with col3:
        st.markdown(pixel_style_metric("Revenue", total_revenue, 8, "#FFE66D"), unsafe_allow_html=True)
    with col4:
        st.markdown(pixel_style_metric("Tenant Score", tenant_satisfaction, 3, "#556270"), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Portfolio Overview with pixel art style
    st.markdown("<h3>PROPERTY PORTFOLIO OVERVIEW</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create a property comparison bar chart with retro colors
        fig = px.bar(
            properties_df,
            x="name",
            y="revenue_per_sqft",
            color="type",
            color_discrete_map={
                "Residential": "#FF6B6B",
                "Commercial": "#4ECDC4",
                "Retail": "#FFE66D",
                "Industrial": "#556270",
                "Mixed-Use": "#9D65C9"
            },
            title="PROPERTY REVENUE COMPARISON",
            labels={"name": "PROPERTY", "revenue_per_sqft": "$ PER SQFT", "type": "TYPE"}
        )
        
        # Make it more retro by changing the layout
        fig.update_layout(
            plot_bgcolor="#2A2A72",
            paper_bgcolor="#2A2A72",
            font=dict(family="VT323", size=14, color="white"),
            title_font=dict(family="VT323", size=24, color="white"),
            legend_title_font=dict(family="VT323", size=12),
            legend_font=dict(family="VT323", size=12),
            xaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323")),
            yaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323"))
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Property type distribution with a pixel-style pie chart
        fig = px.pie(
            properties_df, 
            names="type", 
            title="PROPERTY TYPE DISTRIBUTION",
            color="type",
            color_discrete_map={
                "Residential": "#FF6B6B",
                "Commercial": "#4ECDC4",
                "Retail": "#FFE66D",
                "Industrial": "#556270",
                "Mixed-Use": "#9D65C9"
            },
        )
        
        fig.update_layout(
            plot_bgcolor="#2A2A72",
            paper_bgcolor="#2A2A72",
            font=dict(family="VT323", size=14, color="white"),
            title_font=dict(family="VT323", size=24, color="white"),
            legend_font=dict(family="VT323", size=12)
        )
        
        fig.update_traces(textfont=dict(family="VT323", size=14))
        
        st.plotly_chart(fig, use_container_width=True)
    
    # IoT Analytics Overview
    st.markdown("<h3>SMART BUILDING SYSTEMS STATUS</h3>", unsafe_allow_html=True)
    
    # Filter IoT data for the most recent date
    latest_date = iot_df["date"].max()
    latest_iot = iot_df[iot_df["date"] == latest_date]
    
    # Create columns for sensor values
    sensor_cols = st.columns(5)
    
    for i, (idx, row) in enumerate(latest_iot.iterrows()):
        with sensor_cols[i]:
            # Create a game-like gauge with pixelated style
            if row["sensor_type"] == "Temperature":
                color = "#FF6B6B"  # Red for temperature
            elif row["sensor_type"] == "Humidity":
                color = "#4ECDC4"  # Teal for humidity
            elif row["sensor_type"] == "Occupancy":
                color = "#FFE66D"  # Yellow for occupancy
            elif row["sensor_type"] == "Energy":
                color = "#9D65C9"  # Purple for energy
            else:  # Water
                color = "#556270"  # Gray for water
            
            # Create a pixelated gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=row["value"],
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": row["sensor_type"], "font": {"family": "VT323", "size": 24}},
                gauge={
                    "axis": {"range": [0, row["value"] * 1.5], "tickfont": {"family": "VT323"}},
                    "bar": {"color": color},
                    "bgcolor": "white",
                    "borderwidth": 2,
                    "bordercolor": "black",
                    "steps": [
                        {"range": [0, row["value"] * 0.5], "color": "lightgray"},
                        {"range": [row["value"] * 0.5, row["value"]], "color": color}
                    ],
                },
                number={"font": {"family": "VT323", "size": 40}, "suffix": row["unit"]}
            ))
            
            fig.update_layout(
                height=200,
                plot_bgcolor="#2A2A72",
                paper_bgcolor="#2A2A72",
                font={"family": "VT323", "color": "white"},
                margin=dict(l=30, r=30, t=50, b=30)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Alerts Section styled as game notifications
    st.markdown("<h3>SYSTEM ALERTS</h3>", unsafe_allow_html=True)
    
    alert_cols = st.columns(3)
    
    with alert_cols[0]:
        st.markdown("""
        <div style="background-color: #FF6B6B; border: 3px solid black; padding: 10px; box-shadow: 4px 4px 0px black;">
            <h4 style="text-align: center; margin: 0; color: white;">CRITICAL ALERT</h4>
            <p style="text-align: center; margin: 10px 0; color: white; font-size: 16px;">
                Temperature spike detected in Zone-2.<br>+8°F above normal range.
            </p>
            <div style="text-align: center;">
                <button style="font-family: 'VT323'; background-color: black; color: white; border: none; padding: 5px 15px;">
                    INVESTIGATE
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with alert_cols[1]:
        st.markdown("""
        <div style="background-color: #FFE66D; border: 3px solid black; padding: 10px; box-shadow: 4px 4px 0px black;">
            <h4 style="text-align: center; margin: 0; color: black;">WARNING</h4>
            <p style="text-align: center; margin: 10px 0; color: black; font-size: 16px;">
                Energy consumption 15% above<br>baseline in Property B2.
            </p>
            <div style="text-align: center;">
                <button style="font-family: 'VT323'; background-color: black; color: white; border: none; padding: 5px 15px;">
                    OPTIMIZE
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with alert_cols[2]:
        st.markdown("""
        <div style="background-color: #4ECDC4; border: 3px solid black; padding: 10px; box-shadow: 4px 4px 0px black;">
            <h4 style="text-align: center; margin: 0; color: white;">INFO</h4>
            <p style="text-align: center; margin: 10px 0; color: white; font-size: 16px;">
                3 maintenance requests<br>pending assignment.
            </p>
            <div style="text-align: center;">
                <button style="font-family: 'VT323'; background-color: black; color: white; border: none; padding: 5px 15px;">
                    SCHEDULE
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_property_analytics(properties_df):
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

def create_iot_dashboard(iot_df):
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
    
    # IoT device control panel with game-like buttons
    st.markdown("<h3>DEVICE CONTROL PANEL</h3>", unsafe_allow_html=True)
    
    control_cols = st.columns(3)
    
    with control_cols[0]:
        st.markdown("""
        <div style="
            background-color: #2A2A72;
            border: 3px solid white;
            box-shadow: 4px 4px 0px black;
            padding: 15px;
            text-align: center;
            color: white;
        ">
            <h4 style="margin-top: 0;">TEMPERATURE CONTROL</h4>
            <div style="display: flex; justify-content: space-between; margin: 15px 0;">
                <button style="
                    background-color: #FF6B6B;
                    color: white;
                    border: 2px solid black;
                    padding: 5px 10px;
                    box-shadow: 2px 2px 0px black;
                    font-family: 'VT323', monospace;
                    font-size: 16px;
                ">-</button>
                <span style="font-size: 24px;">72°F</span>
                <button style="
                    background-color: #FF6B6B;
                    color: white;
                    border: 2px solid black;
                    padding: 5px 10px;
                    box-shadow: 2px 2px 0px black;
                    font-family: 'VT323', monospace;
                    font-size: 16px;
                ">+</button>
            </div>
            <button style="
                background-color: #4ECDC4;
                color: white;
                border: 2px solid black;
                padding: 5px 15px;
                box-shadow: 3px 3px 0px black;
                font-family: 'VT323', monospace;
                font-size: 16px;
                margin-top: 10px;
            ">APPLY SETTINGS</button>
        </div>
        """, unsafe_allow_html=True)
    
    with control_cols[1]:
        st.markdown("""
        <div style="
            background-color: #2A2A72;
            border: 3px solid white;
            box-shadow: 4px 4px 0px black;
            padding: 15px;
            text-align: center;
            color: white;
        ">
            <h4 style="margin-top: 0;">LIGHTING CONTROL</h4>
            <div style="margin: 15px 0;">
                <div style="
                    width: 100%;
                    height: 20px;
                    background-color: #556270;
                    border: 2px solid black;
                    position: relative;
                ">
                    <div style="
                        width: 70%;
                        height: 16px;
                        background-color: #FFE66D;
                    "></div>
                    <div style="
                        width: 15px;
                        height: 25px;
                        background-color: white;
                        border: 2px solid black;
                        position: absolute;
                        top: -5px;
                        left: 70%;
                        transform: translateX(-50%);
                    "></div>
                </div>
                <div style="margin-top: 5px; font-size: 18px;">70% BRIGHTNESS</div>
            </div>
            <button style="
                background-color: #4ECDC4;
                color: white;
                border: 2px solid black;
                padding: 5px 15px;
                box-shadow: 3px 3px 0px black;
                font-family: 'VT323', monospace;
                font-size: 16px;
                margin-top: 10px;
            ">APPLY SETTINGS</button>
        </div>
        """, unsafe_allow_html=True)
    
    with control_cols[2]:
        st.markdown("""
        <div style="
            background-color: #2A2A72;
            border: 3px solid white;
            box-shadow: 4px 4px 0px black;
            padding: 15px;
            text-align: center;
            color: white;
        ">
            <h4 style="margin-top: 0;">DEVICE STATUS</h4>
            <div style="display: flex; flex-direction: column; gap: 10px; margin: 15px 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span>HVAC SYSTEM</span>
                    <span style="color: #4ECDC4;">ONLINE</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>LIGHTING</span>
                    <span style="color: #4ECDC4;">ONLINE</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>SECURITY</span>
                    <span style="color: #FF6B6B;">OFFLINE</span>
                </div>
            </div>
            <button style="
                background-color: #FF6B6B;
                color: white;
                border: 2px solid black;
                padding: 5px 15px;
                box-shadow: 3px 3px 0px black;
                font-family: 'VT323', monospace;
                font-size: 16px;
                margin-top: 10px;
            ">RESTART DEVICES</button>
        </div>
        """, unsafe_allow_html=True)

def create_tenant_insights(tenants_df):
    """Create the tenant insights page with retro gaming aesthetic"""
    st.markdown("<h2>TENANT ANALYTICS ARENA</h2>", unsafe_allow_html=True)
    
    # Overview metrics in game-style cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(pixel_style_metric(
            "TOTAL TENANTS", 
            str(len(tenants_df)), 
            5, 
            "#FF6B6B"
        ), unsafe_allow_html=True)
    
    with col2:
        avg_satisfaction = round(tenants_df["satisfaction_score"].mean())
        st.markdown(pixel_style_metric(
            "AVG SATISFACTION", 
            f"{avg_satisfaction}/100", 
            3, 
            "#4ECDC4"
        ), unsafe_allow_html=True)
    
    with col3:
        retention_rate = round(tenants_df["retention_probability"].mean() * 100)
        st.markdown(pixel_style_metric(
            "RETENTION RATE", 
            f"{retention_rate}%", 
            -2, 
            "#FFE66D"
        ), unsafe_allow_html=True)
    
    with col4:
        total_revenue = sum(tenants_df["monthly_rent"]) / 1000
        st.markdown(pixel_style_metric(
            "MONTHLY REVENUE", 
            f"${total_revenue:.0f}K", 
            8, 
            "#9D65C9"
        ), unsafe_allow_html=True)
        
    # Tenant business type breakdown
    st.markdown("<h3>TENANT BUSINESS TYPE DISTRIBUTION</h3>", unsafe_allow_html=True)
    
    # Count tenants by business type
    business_type_counts = tenants_df["business_type"].value_counts().reset_index()
    business_type_counts.columns = ["business_type", "count"]
    
    # Generate pastel colors for the chart
    colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#9D65C9", "#556270", "#F9ADA0"]
    
    # Create a pixel-style bar chart
    fig = px.bar(
        business_type_counts,
        x="business_type",
        y="count",
        color="business_type",
        color_discrete_sequence=colors,
        title="TENANT DISTRIBUTION BY BUSINESS TYPE",
        labels={"business_type": "BUSINESS TYPE", "count": "NUMBER OF TENANTS"}
    )
    
    # Update layout for retro gaming aesthetic
    fig.update_layout(
        plot_bgcolor="#2A2A72",
        paper_bgcolor="#2A2A72",
        font=dict(family="VT323", size=14, color="white"),
        title_font=dict(family="VT323", size=20, color="white"),
        showlegend=False,
        xaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323", size=14)),
        yaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323", size=14))
    )
    
    # Make bars look more pixel-like
    fig.update_traces(
        marker=dict(line=dict(width=2, color="black")),
        hovertemplate="<b>%{x}</b><br>Tenants: %{y}<extra></extra>"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tenant lease timeline
    st.markdown("<h3>LEASE TIMELINE RADAR</h3>", unsafe_allow_html=True)
    
    # Calculate months until lease expiration
    current_date = datetime.now().date()
    tenants_df["months_to_expiration"] = tenants_df.apply(
        lambda row: (row["lease_end"].date() - current_date).days / 30,
        axis=1
    )
    
    # Create columns for the lease timeline and tenant satisfaction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Filter to just show next 12 months of expirations
        next_year_expirations = tenants_df[tenants_df["months_to_expiration"] <= 12].sort_values("months_to_expiration")
        
        if not next_year_expirations.empty:
            # Create a timeline-like visualization
            fig = go.Figure()
            
            for i, (idx, row) in enumerate(next_year_expirations.iterrows()):
                # Determine color based on retention probability
                if row["retention_probability"] >= 0.8:
                    color = "#4ECDC4"  # High retention - teal
                elif row["retention_probability"] >= 0.6:
                    color = "#FFE66D"  # Medium retention - yellow
                else:
                    color = "#FF6B6B"  # Low retention - red
                
                # Add horizontal line for lease duration
                fig.add_trace(go.Scatter(
                    x=[0, row["months_to_expiration"]],
                    y=[i, i],
                    mode="lines",
                    line=dict(color=color, width=8),
                    showlegend=False,
                    hoverinfo="text",
                    hovertext=f"{row['name']} - {row['business_type']}<br>Expires in {row['months_to_expiration']:.1f} months<br>Retention: {row['retention_probability']*100:.0f}%"
                ))
                
                # Add point at the end
                fig.add_trace(go.Scatter(
                    x=[row["months_to_expiration"]],
                    y=[i],
                    mode="markers",
                    marker=dict(color=color, size=14, symbol="square"),
                    showlegend=False,
                    hoverinfo="skip"
                ))
                
                # Add tenant name
                fig.add_annotation(
                    x=-0.5,
                    y=i,
                    text=row["name"],
                    showarrow=False,
                    font=dict(family="VT323", size=12, color="white"),
                    xanchor="right"
                )
            
            # Update layout for retro gaming aesthetic
            fig.update_layout(
                title="UPCOMING LEASE EXPIRATIONS",
                plot_bgcolor="#2A2A72",
                paper_bgcolor="#2A2A72",
                font=dict(family="VT323", size=14, color="white"),
                title_font=dict(family="VT323", size=20, color="white"),
                xaxis=dict(
                    title="MONTHS UNTIL EXPIRATION",
                    range=[-3, 13],
                    gridcolor="#556270",
                    tickfont=dict(family="VT323", size=12)
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    range=[-1, len(next_year_expirations)]
                ),
                margin=dict(l=100, r=20, t=50, b=50)
            )
            
            # Add vertical lines for month markers
            for month in range(0, 13, 3):
                fig.add_shape(
                    type="line",
                    x0=month,
                    y0=-1,
                    x1=month,
                    y1=len(next_year_expirations),
                    line=dict(color="#556270", width=1, dash="dot")
                )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style="
                background-color: #4ECDC4;
                border: 3px solid black;
                box-shadow: 4px 4px 0px black;
                padding: 15px;
                text-align: center;
                color: white;
                margin: 20px 0;
            ">
                <h4 style="margin: 0;">NO LEASE EXPIRATIONS IN THE NEXT 12 MONTHS</h4>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Create a tenant satisfaction distribution histogram
        fig = px.histogram(
            tenants_df,
            x="satisfaction_score",
            nbins=5,
            title="TENANT SATISFACTION DISTRIBUTION",
            labels={"satisfaction_score": "SATISFACTION SCORE"},
            color_discrete_sequence=["#4ECDC4"]
        )
        
        # Update layout for retro gaming aesthetic
        fig.update_layout(
            plot_bgcolor="#2A2A72",
            paper_bgcolor="#2A2A72",
            font=dict(family="VT323", size=14, color="white"),
            title_font=dict(family="VT323", size=16, color="white"),
            xaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323", size=12)),
            yaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323", size=12), title="COUNT")
        )
        
        # Make bars look more pixel-like
        fig.update_traces(
            marker=dict(
                line=dict(width=2, color="black"),
                color="#4ECDC4"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tenant retention analysis
    st.markdown("<h3>TENANT RETENTION ANALYSIS</h3>", unsafe_allow_html=True)
    
    # Create a scatter plot of satisfaction vs retention probability
    fig = px.scatter(
        tenants_df,
        x="satisfaction_score",
        y="retention_probability",
        size="monthly_rent",
        color="business_type",
        color_discrete_map={
            "Retail": "#FF6B6B",
            "Office": "#4ECDC4",
            "Restaurant": "#FFE66D",
            "Medical": "#9D65C9",
            "Tech": "#556270",
            "Financial": "#F9ADA0"
        },
        hover_name="name",
        title="TENANT SATISFACTION VS RETENTION PROBABILITY",
        labels={
            "satisfaction_score": "SATISFACTION SCORE",
            "retention_probability": "RETENTION PROBABILITY",
            "business_type": "BUSINESS TYPE",
            "monthly_rent": "MONTHLY RENT"
        }
    )
    
    # Update layout for retro gaming aesthetic
    fig.update_layout(
        plot_bgcolor="#2A2A72",
        paper_bgcolor="#2A2A72",
        font=dict(family="VT323", size=14, color="white"),
        title_font=dict(family="VT323", size=20, color="white"),
        legend_title_font=dict(family="VT323", size=14),
        legend_font=dict(family="VT323", size=12),
        xaxis=dict(
            gridcolor="#556270", 
            tickfont=dict(family="VT323", size=14),
            range=[55, 105]
        ),
        yaxis=dict(
            gridcolor="#556270", 
            tickfont=dict(family="VT323", size=14),
            range=[0.55, 1.0],
            tickformat=".0%"
        )
    )
    
    # Make markers look more pixel-like
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color="black"),
            symbol="square"
        )
    )
    
    # Add a reference box for high-value at-risk tenants
    fig.add_shape(
        type="rect",
        x0=55,
        y0=0.55,
        x1=75,
        y1=0.7,
        line=dict(color="#FF6B6B", width=2, dash="dash"),
        fillcolor="rgba(255, 107, 107, 0.1)"
    )
    
    # Add annotation for the reference box
    fig.add_annotation(
        x=65,
        y=0.625,
        text="AT-RISK TENANTS",
        showarrow=False,
        font=dict(family="VT323", size=14, color="#FF6B6B")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top tenants by revenue
    st.markdown("<h3>TOP TENANTS LEADERBOARD</h3>", unsafe_allow_html=True)
    
    # Sort tenants by monthly rent
    top_tenants = tenants_df.sort_values("monthly_rent", ascending=False).head(5)
    
    # Create a pixel-style table
    st.markdown("""
    <div style="
        background-color: #2A2A72;
        border: 4px solid white;
        box-shadow: 6px 6px 0px black;
        padding: 15px;
        margin-top: 10px;
        color: white;
    ">
        <h4 style="text-align: center; color: #FFE66D; margin-top: 0;">HIGH-VALUE TENANTS</h4>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #556270;">
                <th style="padding: 8px; border: 2px solid white; text-align: center;">RANK</th>
                <th style="padding: 8px; border: 2px solid white; text-align: center;">TENANT NAME</th>
                <th style="padding: 8px; border: 2px solid white; text-align: center;">BUSINESS TYPE</th>
                <th style="padding: 8px; border: 2px solid white; text-align: center;">MONTHLY RENT</th>
                <th style="padding: 8px; border: 2px solid white; text-align: center;">SATISFACTION</th>
                <th style="padding: 8px; border: 2px solid white; text-align: center;">RETENTION</th>
            </tr>
    """, unsafe_allow_html=True)
    
    for i, (idx, row) in enumerate(top_tenants.iterrows()):
        # Determine row color based on rank
        if i == 0:
            row_color = "#FFE66D"  # Gold for first place
        elif i == 1:
            row_color = "#C0C0C0"  # Silver for second place
        elif i == 2:
            row_color = "#CD7F32"  # Bronze for third place
        else:
            row_color = "#556270"  # Gray for others
        
        # Determine color for satisfaction score
        if row["satisfaction_score"] >= 85:
            satisfaction_color = "#4ECDC4"  # Good - teal
        elif row["satisfaction_score"] >= 70:
            satisfaction_color = "#FFE66D"  # Medium - yellow
        else:
            satisfaction_color = "#FF6B6B"  # Poor - red
        
        # Determine color for retention probability
        if row["retention_probability"] >= 0.8:
            retention_color = "#4ECDC4"  # Good - teal
        elif row["retention_probability"] >= 0.6:
            retention_color = "#FFE66D"  # Medium - yellow
        else:
            retention_color = "#FF6B6B"  # Poor - red
        
        st.markdown(f"""
        <tr style="background-color: {row_color}20;">
            <td style="padding: 8px; border: 2px solid white; text-align: center; font-weight: bold; color: {row_color};">#{i+1}</td>
            <td style="padding: 8px; border: 2px solid white; text-align: center;">{row['name']}</td>
            <td style="padding: 8px; border: 2px solid white; text-align: center;">{row['business_type']}</td>
            <td style="padding: 8px; border: 2px solid white; text-align: center;">${row['monthly_rent']:,}</td>
            <td style="padding: 8px; border: 2px solid white; text-align: center; color: {satisfaction_color};">{row['satisfaction_score']}/100</td>
            <td style="padding: 8px; border: 2px solid white; text-align: center; color: {retention_color};">{row['retention_probability']*100:.0f}%</td>
        </tr>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </table>
    </div>
    """, unsafe_allow_html=True)

def create_predictive_dashboard():
    """Create the predictive analytics dashboard with retro gaming aesthetic"""
    st.markdown("<h2>FUTURE VISION SIMULATOR</h2>", unsafe_allow_html=True)
    
    # Prediction model selector
    model_selection = st.selectbox(
        "SELECT PREDICTION MODEL",
        options=["Revenue Forecasting", "Occupancy Prediction", "Tenant Retention", "Maintenance Planning"]
    )
    
    if model_selection == "Revenue Forecasting":
        # Revenue forecasting section
        st.markdown("<h3>REVENUE FORECAST SIMULATION</h3>", unsafe_allow_html=True)
        
        # Simulation controls that look like game controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            growth_rate = st.slider(
                "MARKET GROWTH RATE",
                min_value=-5.0,
                max_value=10.0,
                value=3.0,
                step=0.5,
                format="%f%%"
            )
        
        with col2:
            occupancy_change = st.slider(
                "OCCUPANCY CHANGE",
                min_value=-10.0,
                max_value=10.0,
                value=2.0,
                step=1.0,
                format="%f%%"
            )
        
        with col3:
            pricing_strategy = st.selectbox(
                "PRICING STRATEGY",
                options=["Conservative", "Balanced", "Aggressive"]
            )
        
        # Create simulated forecast data
        months = list(range(1, 13))
        base_revenue = 500000  # Starting monthly revenue
        
        # Adjust growth based on pricing strategy
        if pricing_strategy == "Conservative":
            strategy_factor = 0.8
            color = "#4ECDC4"
        elif pricing_strategy == "Balanced":
            strategy_factor = 1.0
            color = "#FFE66D"
        else:  # Aggressive
            strategy_factor = 1.2
            color = "#FF6B6B"
        
        # Generate forecast with some seasonal variation
        forecast = []
        for month in months:
            # Base growth
            monthly_growth = (1 + (growth_rate / 100)) ** (month / 12)
            
            # Occupancy effect
            occupancy_effect = (1 + (occupancy_change / 100)) ** (month / 12)
            
            # Seasonal variation (Q4 boost for retail properties)
            seasonal_factor = 1.0
            if month >= 9:  # Q4 months
                seasonal_factor = 1.1
            
            # Combined factors
            monthly_revenue = base_revenue * monthly_growth * occupancy_effect * seasonal_factor * strategy_factor
            
            # Add some randomness
            noise_factor = 1 + random.uniform(-0.02, 0.02)
            monthly_revenue *= noise_factor
            
            forecast.append(monthly_revenue)
        
        # Create a pixel-style line chart
        fig = go.Figure()
        
        # Add forecast line
        fig.add_trace(go.Scatter(
            x=months,
            y=forecast,
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=8, symbol="square"),
            name="Forecast"
        ))
        
        # Add baseline (no growth) line
        baseline = [base_revenue] * len(months)
        fig.add_trace(go.Scatter(
            x=months,
            y=baseline,
            mode="lines",
            line=dict(color="white", width=2, dash="dot"),
            name="Baseline"
        ))
        
        # Calculate annual growth
        annual_growth = forecast[-1] / base_revenue - 1
        total_annual_revenue = sum(forecast)
        
        # Update layout for retro gaming aesthetic
        fig.update_layout(
            title="12-MONTH REVENUE FORECAST",
            plot_bgcolor="#2A2A72",
            paper_bgcolor="#2A2A72",
            font=dict(family="VT323", size=14, color="white"),
            title_font=dict(family="VT323", size=24, color="white"),
            legend_title_font=dict(family="VT323"),
            legend_font=dict(family="VT323", size=12),
            xaxis=dict(
                title="MONTH",
                gridcolor="#556270",
                tickfont=dict(family="VT323", size=14),
                tickvals=months
            ),
            yaxis=dict(
                title="MONTHLY REVENUE ($)",
                gridcolor="#556270",
                tickfont=dict(family="VT323", size=14),
                tickformat="$,.0f"
            )
        )
        
        # Add annotation for annual growth
        fig.add_annotation(
            x=months[-1],
            y=forecast[-1],
            text=f"Annual Growth: {annual_growth*100:.1f}%",
            showarrow=True,
            arrowhead=1,
            font=dict(family="VT323", size=14, color=color),
            bgcolor="#2A2A72",
            bordercolor="white",
            borderwidth=2
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display key metrics from the simulation
        metric_cols = st.columns(3)
        
        with metric_cols[0]:
            st.markdown(pixel_style_metric(
                "ANNUAL REVENUE", 
                f"${total_annual_revenue/1000000:.2f}M", 
                annual_growth*100, 
                color
            ), unsafe_allow_html=True)
        
        with metric_cols[1]:
            avg_monthly = sum(forecast) / len(forecast)
            st.markdown(pixel_style_metric(
                "AVG MONTHLY", 
                f"${avg_monthly/1000:.0f}K", 
                None, 
                color
            ), unsafe_allow_html=True)
        
        with metric_cols[2]:
            peak_month = months[forecast.index(max(forecast))]
            st.markdown(pixel_style_metric(
                "PEAK MONTH", 
                f"Month {peak_month}", 
                None, 
                color
            ), unsafe_allow_html=True)
        
        # Game-like action buttons
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        with col2:
            st.button("🎮 RUN SIMULATION AGAIN", key="run_simulation")
        with col3:
            st.button("💾 SAVE FORECAST", key="save_forecast")
    
    elif model_selection == "Occupancy Prediction":
        # Occupancy prediction section
        st.markdown("<h3>OCCUPANCY LEVEL PREDICTOR</h3>", unsafe_allow_html=True)
        
        # Input controls that look like game controls
        col1, col2 = st.columns(2)
        
        with col1:
            market_demand = st.slider(
                "MARKET DEMAND LEVEL",
                min_value=1,
                max_value=10,
                value=7,
                step=1
            )
            
            rental_adjustment = st.slider(
                "RENTAL RATE ADJUSTMENT",
                min_value=-15.0,
                max_value=15.0,
                value=0.0,
                step=1.0,
                format="%f%%"
            )
        
        with col2:
            property_improvements = st.multiselect(
                "PROPERTY IMPROVEMENTS",
                options=["Smart Building Features", "Renovated Common Areas", "Improved Amenities", "Sustainable Features", "Enhanced Security"],
                default=["Smart Building Features"]
            )
            
            marketing_investment = st.slider(
                "MARKETING INVESTMENT",
                min_value=1,
                max_value=10,
                value=5,
                step=1
            )
        
        # Calculate predicted occupancy based on inputs
        base_occupancy = 0.75  # Starting point
        
        # Market demand effect (0.5 to 1.0 multiplier)
        market_factor = 0.5 + (market_demand / 20)
        
        # Rental adjustment effect (inverse relationship)
        rental_factor = 1.0 - (rental_adjustment / 100)
        
        # Property improvements effect (each adds 2%)
        improvement_factor = 1.0 + (len(property_improvements) * 0.02)
        
        # Marketing investment effect (0.9 to 1.1 multiplier)
        marketing_factor = 0.9 + (marketing_investment / 50)
        
        # Combined effect with limits
        predicted_occupancy = base_occupancy * market_factor * rental_factor * improvement_factor * marketing_factor
        predicted_occupancy = max(0.5, min(0.98, predicted_occupancy))  # Cap between 50% and 98%
        
        # Create a gauge chart for predicted occupancy
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=predicted_occupancy * 100,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "PREDICTED OCCUPANCY", "font": {"family": "VT323", "size": 24, "color": "white"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 2, "tickcolor": "white", "tickfont": {"family": "VT323"}},
                "bar": {"color": "#4ECDC4" if predicted_occupancy >= 0.8 else "#FFE66D" if predicted_occupancy >= 0.65 else "#FF6B6B"},
                "bgcolor": "#556270",
                "borderwidth": 2,
                "bordercolor": "white",
                "steps": [
                    {"range": [0, 65], "color": "#FF6B6B30"},
                    {"range": [65, 80], "color": "#FFE66D30"},
                    {"range": [80, 100], "color": "#4ECDC430"}
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": base_occupancy * 100
                }
            },
            number={"font": {"family": "VT323", "size": 40, "color": "white"}, "suffix": "%"}
        ))
        
        # Update layout for retro gaming aesthetic
        fig.update_layout(
            height=300,
            plot_bgcolor="#2A2A72",
            paper_bgcolor="#2A2A72",
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add impact factors breakdown
        st.markdown("<h3>IMPACT FACTORS</h3>", unsafe_allow_html=True)
        
        impact_cols = st.columns(4)
        
        with impact_cols[0]:
            market_impact = (market_factor - 0.75) * 2  # Scale to percentage impact
            st.markdown(pixel_style_metric(
                "MARKET IMPACT", 
                f"{market_impact*100:.1f}%", 
                None, 
                "#4ECDC4" if market_impact > 0 else "#FF6B6B"
            ), unsafe_allow_html=True)
        
        with impact_cols[1]:
            rental_impact = (rental_factor - 1.0)  # Convert to percentage impact
            st.markdown(pixel_style_metric(
                "PRICE IMPACT", 
                f"{rental_impact*100:.1f}%", 
                None, 
                "#4ECDC4" if rental_impact > 0 else "#FF6B6B"
            ), unsafe_allow_html=True)
        
        with impact_cols[2]:
            improvement_impact = (improvement_factor - 1.0)  # Convert to percentage impact
            st.markdown(pixel_style_metric(
                "IMPROVEMENTS", 
                f"{improvement_impact*100:.1f}%", 
                None, 
                "#4ECDC4"
            ), unsafe_allow_html=True)
        
        with impact_cols[3]:
            marketing_impact = (marketing_factor - 1.0)  # Convert to percentage impact
            st.markdown(pixel_style_metric(
                "MARKETING", 
                f"{marketing_impact*100:.1f}%", 
                None, 
                "#4ECDC4" if marketing_impact > 0 else "#FF6B6B"
            ), unsafe_allow_html=True)
        
        # Recommendations based on prediction
        st.markdown("<h3>AI RECOMMENDATIONS</h3>", unsafe_allow_html=True)
        
        rec_cols = st.columns(2)
        
        with rec_cols[0]:
            if predicted_occupancy < 0.7:
                recommendation_color = "#FF6B6B"
                recommendation_title = "CRITICAL: OCCUPANCY RISK"
                recommendations = [
                    "Consider 5-10% rental rate reduction",
                    "Increase marketing budget significantly",
                    "Expedite planned property improvements",
                    "Offer signing incentives for new tenants"
                ]
            elif predicted_occupancy < 0.85:
                recommendation_color = "#FFE66D"
                recommendation_title = "MODERATE: OPTIMIZATION NEEDED"
                recommendations = [
                    "Fine-tune rental rates (±3%)",
                    "Target marketing to high-potential segments",
                    "Prioritize tenant experience improvements",
                    "Develop competitive analysis report"
                ]
            else:
                recommendation_color = "#4ECDC4"
                recommendation_title = "POSITIVE: MAINTAIN STRATEGY"
                recommendations = [
                    "Consider selective price increases",
                    "Invest in tenant retention programs",
                    "Plan for property upgrades from increased revenue",
                    "Expand to adjacent markets if possible"
                ]
            
            st.markdown(f"""
            <div style="
                background-color: {recommendation_color};
                border: 3px solid black;
                box-shadow: 4px 4px 0px black;
                padding: 15px;
                color: white;
                margin-bottom: 20px;
            ">
                <h4 style="text-align: center; margin-top: 0; color: {'black' if recommendation_color == '#FFE66D' else 'white'};">{recommendation_title}</h4>
                <ul style="color: {'black' if recommendation_color == '#FFE66D' else 'white'}; list-style-type: none; padding-left: 10px;">
            """, unsafe_allow_html=True)
            
            for rec in recommendations:
                st.markdown(f"""
                <li style="margin-bottom: 10px; font-size: 16px;">→ {rec}</li>
                """, unsafe_allow_html=True)
            
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with rec_cols[1]:
            # Create a simple bar chart showing occupancy by property type
            property_types = ["Retail", "Office", "Mixed-Use", "Industrial"]
            occupancies = [0.85, 0.72, 0.91, 0.88]  # Sample values
            
            fig = go.Figure()
            
            # Add bars with pixel-style colors
            fig.add_trace(go.Bar(
                x=property_types,
                y=occupancies,
                marker_color=["#FF6B6B", "#9D65C9", "#4ECDC4", "#FFE66D"],
                marker_line_color="black",
                marker_line_width=2,
                text=[f"{occ*100:.0f}%" for occ in occupancies],
                textposition="auto",
                textfont=dict(family="VT323", size=14)
            ))
            
            # Update layout for retro gaming aesthetic
            fig.update_layout(
                title="MARKET OCCUPANCY BY PROPERTY TYPE",
                plot_bgcolor="#2A2A72",
                paper_bgcolor="#2A2A72",
                font=dict(family="VT323", size=14, color="white"),
                title_font=dict(family="VT323", size=18, color="white"),
                xaxis=dict(gridcolor="#556270", tickfont=dict(family="VT323", size=14)),
                yaxis=dict(
                    gridcolor="#556270", 
                    tickfont=dict(family="VT323", size=14),
                    tickformat=".0%",
                    range=[0, 1]
                ),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            st.plotly_chart(fig, use_container_width=True)

def main():
    """Main function to run the Streamlit app"""
    # Apply the pixel art header
    create_pixel_art_header()
    
    # Create the game-like menu
    menu_selection, date_range, selected_properties = create_game_menu()
    
    # Generate sample data
    properties_df = generate_sample_property_data(15)
    iot_df = generate_iot_sensor_data(30, 5)
    tenants_df = generate_tenant_data(25)
    
    # Display the selected page
    if menu_selection == "🏢 Executive Dashboard":
        create_executive_dashboard(properties_df, iot_df, tenants_df)
    elif menu_selection == "🔍 Property Analytics":
        create_property_analytics(properties_df)
    elif menu_selection == "🤖 IoT Systems":
        create_iot_dashboard(iot_df)
    elif menu_selection == "👥 Tenant Insights":
        create_tenant_insights(tenants_df)
    elif menu_selection == "📊 Predictive Models":
        create_predictive_dashboard()

if __name__ == "__main__":
    main()