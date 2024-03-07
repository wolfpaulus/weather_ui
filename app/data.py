""" 
    Obtain Weather Forecast
    Author: Wolf Paulus 
"""
from json import dump, load
from datetime import datetime
from dateutil import tz
from requests import get
import streamlit as st


DATA_URL = "https://api.weather.gov/gridpoints/FGZ/67,74/forecast"
DATA_FILE = "./app/data/weather.json"


@st.cache_data(show_spinner="Fetching data from API...", ttl=60*10)
def get_data(data_url: str = DATA_URL, data_file: str = DATA_FILE) -> dict:
    """ Fetch data from a file or the api. """
    try:
        forecast = get(url=data_url, timeout=3).json()
        if forecast and forecast.get("properties", {}).get("periods"):
            # as a backup, save the forecast in a file
            with open(data_file, "w", encoding="utf-8") as file:
                dump(forecast, file)
            st.info("forecast backup created", icon="📂")    
            return forecast
        with open(data_file, "r", encoding="utf-8") as file:
            forecast = load(file)
        st.warning("Using cached forecast data", icon="⚠️")
        return forecast
    except OSError as err:  # IOErrors (file and network)
        st.error(str(err), icon="💣")
    except TypeError as err:  # JSON decoder problems
        st.error(str(err), icon="💣")
    return {}


def reload_data() -> None:
    """ clear the weather data cache, next get_data call will request json from web service """
    get_data.clear()


def last_updated(forecast: dict) -> str:
    """ returns a display string of the last update timestamp """
    dtime = datetime.fromisoformat(forecast['properties']['updated'])
    dtime = dtime.replace(tzinfo=tz.gettz('UTC')).astimezone(
        tz.gettz("MST"))  # tz.gettz('America/Arizona'))
    return dtime.strftime('%A, %B %-d, %Y %-I:%-M:%-S %p %Z')
