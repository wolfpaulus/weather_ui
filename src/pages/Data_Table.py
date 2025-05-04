"""
    Streamlit front-end (Table View) for api.weather.gov
    Author: Wolf Paulus
"""
import streamlit as st
from data import get_gps_coordinates, get_nws_office, get_forecast, updated, clear_cache


st.title("Weather Data Table")
try:
    lat, lon, timezone = get_gps_coordinates()
    grid_id, grid_x, grid_y = get_nws_office(lat, lon)
    forecast = get_forecast(grid_id, grid_x, grid_y)
    periods = forecast["properties"]["periods"]
    last_updated = updated(forecast, timezone)

    st.subheader(f"Updated: {last_updated}")
    updat_btn = st.sidebar.button("Update", type="primary", on_click=clear_cache)
    day_time_only = st.sidebar.toggle("Only show daytime temperatures", value=True)
    columns = st.sidebar.multiselect("Select the columns to be displayed:", list(
        periods[0].keys()), default=["name", "temperature"], placeholder="Select columns")
    custom = [{k: v for k, v in p.items() if k in columns}
              for p in periods if p["isDaytime"] or not day_time_only]
    st.table(custom)
except OSError as e:
    st.error(f"Error fetching GPS coordinates: {e}", icon="💣")
    st.stop()
