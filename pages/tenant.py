import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from components.metrics import pixel_style_metric

def create_dashboard(tenants_df):
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
    
    # Generate colors for the chart
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