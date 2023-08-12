from flair.models import SequenceTagger
from geopy.geocoders import GeoNames

import pandas as pd
from flair.data import Sentence


def get_coordinates():
    geolocator = GeoNames(username='QuakeText')

    place_name = "Pakistan"
    geonames_instances = geolocator.geocode(place_name, exactly_one=False)
    print(geonames_instances)
    for instance in geonames_instances:
        if instance.address.split(',') == place_name:
            print()
            #do some stuff here to add it to the data base



get_coordinates()