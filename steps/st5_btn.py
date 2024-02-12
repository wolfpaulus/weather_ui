""" Streamlit front-end for api.weather.gov """
import streamlit as st
from requests import get
from time import sleep


def load_data() -> None:
    global periods, all_cols, pre_cols
    sleep(2)  # just to show that requests may take some time
    forecast = get(
        "https://api.weather.gov/gridpoints/FGZ/67,74/forecast", timeout=3).json()
    periods = forecast.get("properties").get("periods")
    all_cols = list(periods[0].keys())
    pre_cols = ["name", "temperature"]


load_data()

st.title("Weather Forecast")
st.sidebar.button("Update", type="primary", on_click=load_data)
day_time_only = st.sidebar.toggle("Only show daytime temperatures", value=True)
columns = st.sidebar.multiselect(
    "Select the columns to be displayed:", all_cols, default=pre_cols, placeholder="Select columns")
custom = [{k: v for k, v in p.items() if k in columns}
          for p in periods if p["isDaytime"] or not day_time_only]
st.table(custom)
