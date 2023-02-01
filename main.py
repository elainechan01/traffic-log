"""
Author: Elaine Yun Ru Chan
Date: 01/31/2023
"""

from geopy.geocoders import Nominatim
import requests

from google.cloud import storage

def get_latlng(address: str) -> str:
    """
    Helper function to convert an address to latitude and longitude

    Required Args
        address (str): Address as a string (eg. 1400 S Lake Shore Dr, Chicago, IL)
    
    Returns
        str: The latitude and langitude of the address (eg. <lat>,<lng>)
    """
    locator = Nominatim(user_agent='<APP NAME>')
    location = locator.geocode(address)
    return str(location.latitude) + ',' + str(location.longitude)

def create_write_to_bucket(message: str) -> None:
    """
    Helper function to write to a file in Cloud Storage

    Required Args
        message (str): The message to be stored in the file
    """
    client = storage.Client(project='<GCP PROJECT ID>')
    bucket = client.bucket('<BUCKET NAME>')
    blob = bucket.blob('<FILENAME>')

    with blob.open('w') as f:
        f.write(message)

def get_duration_in_traffic():
    """
    Main function to get the traffic information of the route

    Returns
        str: The duration in traffic for the route (eg. 30 mins)
    """
    origin = get_latlng('1400 S Lake Shore Dr, Chicago, IL')            # Field Museum
    dest = get_latlng('646 Michigan Ave, Chicago, IL ')                 # Starbucks Reserve Roastery
    base_url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': origin,
        'destination': dest,
        'departure_time': 'now',
        'key': '<DIRECTIONS API KEY>'
    }
    response = requests.get(base_url, params=params)
    return response.json()['routes'][0]['legs'][0]['duration_in_traffic']['text']
    
# duration = get_duration_in_traffic()
# create_write_to_bucket(duration)
