"""
    Streamlit front-end (JSON View) for api.weather.gov
    Author: Wolf Paulus
"""
from json import dumps
import streamlit as st
from data import get_gps_coordinates, get_nws_office, get_forecast, updated

st.title("Weather Data")
try:
    lat, lon, timezone = get_gps_coordinates()
    grid_id, grid_x, grid_y = get_nws_office(lat, lon)
    forecast = get_forecast(grid_id, grid_x, grid_y)
    periods = forecast["properties"]["periods"]
    last_updated = updated(forecast, timezone)

    st.title("Weather Data")
    st.subheader(f"Updated: {last_updated}")
    st.json(forecast)
    st.sidebar.download_button(
        "Download JSON", dumps(forecast), file_name="sedona_weather.json", mime="application/json", type="primary")
except OSError as e:
    st.error(f"Error fetching GPS coordinates: {e}", icon="💣")
    st.stop()
