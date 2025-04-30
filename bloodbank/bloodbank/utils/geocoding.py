# bloodbank/utils/geocoding.py
from geopy.geocoders import Nominatim
from time import sleep
from django.conf import settings

def get_coordinates(address):
    """
    Convert address to (latitude, longitude) using Nominatim.
    Handles rate limiting (1 request/second).
    """
    geolocator = Nominatim(user_agent=settings.OSM_USER_AGENT)  # Set in settings.py
    try:
        location = geolocator.geocode(address)
        sleep(1)  # Respect Nominatim's 1 request/second limit
        if location:
            return (location.latitude, location.longitude)
        return (None, None)
    except Exception as e:
        print(f"Geocoding error for '{address}': {e}")
        return (None, None)