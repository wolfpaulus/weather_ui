"""
Test the data module.
Author: Wolf Paulus (wolf@paulus.com)
"""
from datetime import datetime
from data import get_forecast, get_gps_coordinates, get_nws_office, updated, clear_cache, cache


def test_get_gps_coordinates():
    """Test the get_gps_coordinates function."""
    lat, lon, timezone = get_gps_coordinates()
    assert isinstance(lat, str)
    assert isinstance(lon, str)
    assert isinstance(timezone, str)
    assert lat != "0"
    assert lon != "0"
    assert timezone != "UTC"  # Assuming the test is run from a location other than UTC


def test_get_nws_office():
    """Test the get_nws_office function."""
    lat, lon, _ = get_gps_coordinates()
    grid_id, grid_x, grid_y = get_nws_office(lat, lon)
    assert isinstance(grid_id, str)
    assert isinstance(grid_x, int)
    assert isinstance(grid_y, int)
    assert grid_id != ""
    assert grid_x != ""
    assert grid_y != ""


def test_get_forecast():
    """Test the get_forecast function."""
    lat, lon, _ = get_gps_coordinates()
    grid_id, grid_x, grid_y = get_nws_office(lat, lon)
    forecast = get_forecast(grid_id, grid_x, grid_y)
    assert isinstance(forecast, dict)
    assert "properties" in forecast
    assert "periods" in forecast["properties"]
    assert isinstance(forecast["properties"]["periods"], list)
    assert len(forecast["properties"]["periods"]) > 0
    for period in forecast["properties"]["periods"]:
        assert isinstance(period, dict)
        assert "temperature" in period
        assert "windSpeed" in period
        assert "shortForecast" in period


def test_updated():
    """Test the updated function."""
    lat, lon, timezone = get_gps_coordinates()
    grid_id, grid_x, grid_y = get_nws_office(lat, lon)
    forecast = get_forecast(grid_id, grid_x, grid_y)
    last_updated = updated(forecast, timezone)
    assert isinstance(last_updated, str)
    assert last_updated != ""


def test_clear_cache():
    """Test the clear_cache function."""
    # First, we need to ensure that the cache is not empty
    lat, lon, _ = get_gps_coordinates()
    grid_id, grid_x, grid_y = get_nws_office(lat, lon)
    _ = get_forecast(grid_id, grid_x, grid_y)

    # Check that the cache has some data
    assert len(cache) > 0

    # Clear the cache
    clear_cache()

    # Check that the cache is now empty
    assert len(cache) == 0
