"""
Test the app module.
Author: Wolf Paulus (wolf@paulus.com)
"""
from unittest import TestCase
from streamlit.testing.v1 import AppTest


class Test(TestCase):    
    def test_ui_title_and_header(self):
        """
        find out more about how to test streamlit apps:
        https://docs.streamlit.io/library/api-reference/app-testing
        """
        at = AppTest.from_file("./app/Sedona_Weather.py")
        at.run()

        assert at.title[0].value.startswith("Weather Forecast")
        assert at.subheader[0].value.startswith("Updated")
        assert not at.exception
