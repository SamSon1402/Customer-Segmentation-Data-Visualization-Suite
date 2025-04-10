import streamlit as st
import random
import plotly.graph_objects as go
from components.metrics import pixel_style_metric

def create_dashboard():
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