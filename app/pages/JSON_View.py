""" 
    Streamlit front-end (JSON View) for api.weather.gov 
    Author: Wolf Paulus
"""
import streamlit as st
from data import get_data, last_updated


forecast = get_data()

st.title("Weather Data")
st.subheader(f"Updated: {last_updated(forecast)}")
st.json(forecast)
with open("./data/weather.json", encoding="utf-8") as f:
    st.sidebar.download_button(
        "Download JSON", f, file_name="sedona_weather.json", mime="application/json", type="primary")
