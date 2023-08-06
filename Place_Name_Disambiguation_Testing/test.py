from geopy.geocoders import GeoNames


def get_coordinates():
    geolocator = GeoNames(username='QuakeText')  # Replace with your GeoNames username

    place_name = "New York"
    geonames_instances = geolocator.geocode(place_name, exactly_one=False)

    for instance in geonames_instances:
        hello = instance.raw
        print(instance.raw.get('fclName'))



get_coordinates()
