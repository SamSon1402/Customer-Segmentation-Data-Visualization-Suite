import streamlit as st
import pandas as pd

def filter_properties_by_selection(properties_df, selected_properties):
    """Filter properties dataframe based on selected property names"""
    if not selected_properties:
        return properties_df
    return properties_df[properties_df["name"].isin(selected_properties)]

def filter_data_by_date_range(df, date_column, start_date, end_date):
    """Filter dataframe by date range"""
    if not isinstance(start_date, pd.Timestamp):
        start_date = pd.Timestamp(start_date)
    if not isinstance(end_date, pd.Timestamp):
        end_date = pd.Timestamp(end_date)
    
    filtered_df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
    return filtered_df

def create_alert_box(title, message, color, button_text=None):
    """Create a game-like alert box with pixel styling"""
    html = f"""
    <div style="background-color: {color}; border: 3px solid black; padding: 10px; box-shadow: 4px 4px 0px black;">
        <h4 style="text-align: center; margin: 0; color: {'black' if color == '#FFE66D' else 'white'};">{title}</h4>
        <p style="text-align: center; margin: 10px 0; color: {'black' if color == '#FFE66D' else 'white'}; font-size: 16px;">
            {message}
        </p>
    """
    
    if button_text:
        html += f"""
        <div style="text-align: center;">
            <button style="font-family: 'VT323'; background-color: black; color: white; border: none; padding: 5px 15px;">
                {button_text}
            </button>
        </div>
        """
    
    html += "</div>"
    return html