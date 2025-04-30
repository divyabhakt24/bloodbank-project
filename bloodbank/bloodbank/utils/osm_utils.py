import requests
from typing import List, Dict

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def fetch_osm_hospitals(location: str, filters: Dict = None) -> List[Dict]:
    """
    Fetch hospitals from OpenStreetMap using Overpass API

    Args:
        location: City/region name (e.g., "Mumbai")
        filters: Additional OSM tags (e.g., {"healthcare": "blood_bank"})

    Returns:
        List of hospital dictionaries with name, coordinates, etc.
    """
    base_query = f"""
    [out:json];
    area["name"="{location}"]->.searchArea;
    (
        node["amenity"="hospital"](area.searchArea);
        way["amenity"="hospital"](area.searchArea);
    );
    out center;
    """

    # Add additional filters if provided
    if filters:
        filter_str = "".join([f'["{k}"="{v}"]' for k, v in filters.items()])
        base_query = base_query.replace('"hospital"', f'"hospital"{filter_str}')

    try:
        response = requests.get(OVERPASS_URL, params={'data': base_query}, timeout=30)
        response.raise_for_status()
        data = response.json()

        hospitals = []
        for element in data.get('elements', []):
            hospitals.append({
                'osm_id': element.get('id'),
                'name': element.get('tags', {}).get('name', 'Unnamed Hospital'),
                'latitude': element.get('lat'),
                'longitude': element.get('lon'),
                'address': element.get('tags', {}).get('addr:full'),
                'type': element.get('tags', {}).get('healthcare', 'general'),
                'phone': element.get('tags', {}).get('phone')
            })
        return hospitals

    except requests.exceptions.RequestException as e:
        print(f"Overpass API error: {e}")
        return []


# In osm_utils.py, modify the query:
def fetch_osm_hospitals(location):
    # For country-level queries, use states
    if location.lower() == "india":
        return fetch_indian_hospitals_by_state()

    # Original query for cities
    ...


def fetch_indian_hospitals_by_state():
    states = ["Maharashtra", "Delhi", "Tamil Nadu"]  # Top states
    all_hospitals = []

    for state in states:
        try:
            hospitals = fetch_osm_hospitals(state)
            all_hospitals.extend(hospitals)
        except Exception as e:
            print(f"Failed for {state}: {str(e)}")

    return all_hospitals