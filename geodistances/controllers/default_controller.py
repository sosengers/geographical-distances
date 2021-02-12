import connexion
import six

from geodistances.models.locations import Locations  # noqa: E501
from geodistances import util
import logging
from math import radians, cos, sin, asin, sqrt
from opencage.geocoder import OpenCageGeocode
from os import environ

def get_coordinates_from_address(address: str):
    key = environ.get("OPEN_CAGE_API_KEY")
    gecoder = OpenCageGeocode(key)
    results = gecoder.geocode(address)
    return results[0]['geometry']['lat'], results[0]['geometry']['lng'],

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers.
    return c * r


def calculate_distance(locations=None):  # noqa: E501
    """calculateDistance

    Calculates the distance between the given locations. Given addresses are first transformed into coordinates via geocoding, then the distance is computed and returned in kilometers. API for: ACMESky # noqa: E501

    :param locations: 
    :type locations: dict | bytes

    :rtype: float
    """
    if connexion.request.is_json:
        locations = Locations.from_dict(connexion.request.get_json())  # noqa: E501
    lat1, long1 = get_coordinates_from_address(locations.address_1)
    lat2, long2 = get_coordinates_from_address(locations.address_2)
    return haversine(long1, lat1, long2, lat2)
