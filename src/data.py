"""
    Obtain Weather Forecast
    Author: Wolf Paulus
"""
from time import time
from datetime import datetime
from typing import Callable
from dateutil import tz
from requests import get


def cache_with_expiry(expiry_time: int) -> Callable:
    """ Decorator to cache function results with an expiry time in seconds. """
    def decorator(func: Callable) -> Callable:
        """ Decorator to cache function results with an expiry time. """
        def wrapper(*args, **kwargs):
            """ Wrapper function to cache results with expiry time. """
            key = (*args, *kwargs.items())  # Create a unique key for the cache
            if key in cache:
                value, timestamp = cache[key]
                if time() - timestamp < expiry_time:
                    return value
            result = func(*args, **kwargs)
            cache[key] = (result, time())
            return result
        return wrapper
    return decorator


@cache_with_expiry(3600)  # Cache for 1 hour
def get_gps_coordinates() -> tuple[str, str, str]:
    """ Return the GPS coordinates for the location of interest. """
    try:
        d = get("https://ipinfo.io/json", timeout=3).json()
        return *d.get("loc", "0,0").split(","), d.get("timezone", "UTC")
    except OSError as err:
        raise OSError(f"Error fetching GPS coordinates: {err}") from err


@cache_with_expiry(3600)  # Cache for 1 hour
def get_nws_office(lat: str, lon: str) -> tuple[str, int, int]:
    """ Return the NWS office identifier for the given GPS coordinates. """
    try:
        url = f"https://api.weather.gov/points/{lat},{lon}"
        d = get(url, timeout=3).json()
        grid_id = d.get("properties", {}).get("gridId", "")
        grid_x = d.get("properties", {}).get("gridX", 0)
        grid_y = d.get("properties", {}).get("gridY", 0)
        return grid_id, grid_x, grid_y
    except OSError as err:
        raise OSError(f"Error fetching GPS coordinates: {err}") from err


@cache_with_expiry(3600)  # Cache for 1 hour
def get_forecast(grid_id: str, grid_x: int, grid_y: int) -> dict:
    """ Fetch data from a file or the api. """
    try:
        url = f"https://api.weather.gov/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast"
        forecast = get(url, timeout=3).json()
        if not forecast.get("properties", {}).get("periods"):
            raise ValueError("No periods found in the forecast data.")
        return forecast
    except OSError as err:  # IOErrors (file and network)
        raise OSError(f"Error fetching GPS coordinates: {err}") from err
    except TypeError as err:  # JSON decoder problems
        raise OSError(f"Error fetching GPS coordinates: {err}") from err


def updated(forecast: dict, timezone: str) -> str:
    """ returns a display string of the last update timestamp """
    dtime = datetime.fromisoformat(forecast['properties']['updateTime'])
    dtime = dtime.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz(timezone))
    return dtime.strftime('%A, %B %-d, %Y %-I:%M:%S %p %Z')


def clear_cache():
    """ Clear the cache. """
    cache.clear()


cache = {}
