""" 
    Streamlit front-end for api.weather.gov 
    Author: Wolf Paulus
"""
import pandas as pd
import streamlit as st
import altair as alt
from data import reload_data, get_data, last_updated

st.set_page_config(
    page_title="Sedona Weather",
    page_icon="🏜️",
)
import os
st.warning(os.getcwd()) 

forecast = get_data()
periods = forecast["properties"]["periods"]

for p in periods:
    p["wind"] = max([int(w) for w in p["windSpeed"].split() if w.isdigit()])

st.title("Weather Forecast")
st.header("for Sedona, AZ")
st.subheader(f"Updated: {last_updated(forecast)}")

with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", f"{periods[0]['temperature']} °F")
    col2.metric("Wind", f"{periods[0]['windSpeed']}")
    col3.metric("Humidity", f"{periods[0]['relativeHumidity']['value']} %")

updat_btn = st.sidebar.button("Update", type="primary", on_click=reload_data)
columns = ["isDaytime", "temperature", "name", "wind", "shortForecast"]
chart_data = pd.DataFrame(periods, columns=columns)

c = (
    alt.Chart(chart_data)
    .mark_circle()
    .encode(x=alt.X("name", sort=None, title="Day"),
            y=alt.Y("temperature", title="Temperature (F)"),
            size=alt.Size("wind", title="Wind Speed (mph)"),
            color=alt.Color("isDaytime", legend=None).scale(
        scheme="blueorange"),
        tooltip=alt.Tooltip("shortForecast"))
)
st.altair_chart(c, use_container_width=True, theme=None)
