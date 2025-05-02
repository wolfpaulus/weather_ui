"""
Test the data module.
Author: Wolf Paulus (wolf@paulus.com)
"""
from os.path import exists, join
from os import remove
from unittest import TestCase
from data import get_data


class Test(TestCase):
    """ Test the data module. """

    def test_data_acquisition(self):
        """
            fetching new data and pooking around a little
        """
        path_to_data_file = join("src", "dta", "weather.json")
        get_data.clear()

        if exists(path_to_data_file):
            remove(path_to_data_file)
        assert not exists(path_to_data_file)
        forecast = get_data()
        assert exists(path_to_data_file)
        periods = forecast["properties"]["periods"]
        assert len(periods)
        assert periods[0]["temperature"]
