"""
    Streamlit front-end for api.weather.gov
    Author: Wolf Paulus
"""

import pandas as pd
import streamlit as st
import altair as alt
from data import get_gps_coordinates, get_nws_office, get_forecast, updated, clear_cache


st.set_page_config(
    page_title="Local Weather",
    page_icon="🏜️",
)
# Add custom CSS to hide the Header
st.markdown(
    """
    <style>
        header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)
try:
    lat, lon, timezone = get_gps_coordinates()
    grid_id, grid_x, grid_y = get_nws_office(lat, lon)
    forecast = get_forecast(grid_id, grid_x, grid_y)
    periods = forecast["properties"]["periods"]
    last_updated = updated(forecast, timezone)

    for p in periods:
        p["wind"] = max([int(w) for w in p["windSpeed"].split() if w.isdigit()])

    st.title("Weather Forecast")
    st.header("for Sedona, AZ")
    st.subheader(f"Updated: {last_updated}")

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", f"{periods[0]['temperature']} °F")
        col2.metric("Wind", f"{periods[0]['windSpeed']}")
        col3.metric("Rain Chance", f"{periods[0]['probabilityOfPrecipitation']['value']} %")

    updat_btn = st.sidebar.button("Update", type="primary", on_click=clear_cache)
    columns = ["isDaytime", "temperature", "name", "wind", "shortForecast"]
    chart_data = pd.DataFrame(periods, columns=columns)

    c = (
        alt.Chart(chart_data)
        .mark_circle()
        .encode(
            x=alt.X("name", sort=None, title="Day"),
            y=alt.Y("temperature", title="Temperature (F)"),
            size=alt.Size("wind", title="Wind Speed (mph)"),
            color=alt.Color("isDaytime", legend=None).scale(scheme="blueorange"),
            tooltip=alt.Tooltip("shortForecast"),
        )
    )
    st.altair_chart(c, use_container_width=True, theme=None)
except OSError as e:
    st.error(f"Error fetching GPS coordinates: {e}", icon="💣")
    st.stop()
