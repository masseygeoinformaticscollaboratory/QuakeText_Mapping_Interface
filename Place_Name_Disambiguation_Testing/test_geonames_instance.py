from flair.models import SequenceTagger
from geopy.geocoders import GeoNames

import pandas as pd
from flair.data import Sentence


def get_coordinates():
    geolocator = GeoNames(username='QuakeText')

    place_name = "Balochistan"
    geonames_instances = geolocator.geocode(place_name, exactly_one=False)

    for instance in geonames_instances:
        hello = instance.raw
        print(instance.raw.get('fclName'))
