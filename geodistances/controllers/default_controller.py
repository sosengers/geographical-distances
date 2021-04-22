import connexion

from geodistances.models.locations import Locations  # noqa: E501
from math import radians, cos, sin, asin, sqrt
from opencage.geocoder import OpenCageGeocode
from os import environ
import sys


def get_coordinates_from_address(address: str):
    """
    Performs the geocoding process on address.
    @param address: string representing an address.
    @return: the latitude and longitude of the best match found for the given address.
    """

    if "OPEN_CAGE_API_KEY" not in environ:
        print("Environment variable OPEN_CAGE_API_KEY was not set.")
        sys.exit(1)
    key = environ.get("OPEN_CAGE_API_KEY")
    api = OpenCageGeocode(key)
    results = api.geocode(address)
    return results[0]['geometry']['lat'], results[0]['geometry']['lng']


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the [Haversine distance](https://en.wikipedia.org/wiki/Haversine_formula)
    between point P1 and P2.
    """
    # Converting longitude and latitude of the two points from degrees to radians.
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Applying the formula
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Approximated radius of earth in kilometers.
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
