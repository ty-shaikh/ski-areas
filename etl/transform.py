"""Data Transformation

This script processes the raw data.

The script takes a pickle file and outputs another pickle file.

This script requires that 'geocoder' and 'dotenv' be installed within the
local Python environment.
"""

import re
import time
import pickle

import geocoder
from dotenv import dotenv_values

def convert_to_int(text: str):
    """Removes all non-digit characters from a given string and converts into an integer

    Parameters
    ----------
    text : str
        The text to be cleaned

    Returns
    -------
    integer
        An integer of the text without non-digit characters
    """
    try:
        non_digit_string = re.sub("[^0123456789\.]", "", text)
        converted_int = int(non_digit_string)
        return converted_int
    except:
        return 0

def clean_address(text: str):
    """Extracts the street address from the input text

    Parameters
    ----------
    text : str
        The text to be processed

    Returns
    -------
    string
        A string of the street address
    """
    try:
        address_list = text.split('\n')[1].split(' ')[-6:]
        joined_address = ' '.join(address_list)
        address =  joined_address.replace(u'\xa0', u' ').strip()
        state = address.split(',')[-1].strip().split(' ')[0]
        return address
    except:
        return ''

def get_lat_long(address: str):
    """Queries the Bing Maps API to get geolocation coordinates

    Parameters
    ----------
    address : str
        The street address

    Returns
    -------
    tuple
        Latitude and longitude coordinates for the street address
    """
    try:
        time.sleep(1)
        secrets = dotenv_values("./.env")
        g = geocoder.bing(address, key=secrets["BING_MAPS_API_KEY"])
        results = g.json
        return (results['lat'], results['lng'])
    except:
        return (0, 0)

def main():
    print("Running the tranform script")
    raw_data = pickle.load(open('./data/extract_output.pkl', 'rb'))
    cleaned_db = []

    names = [row['Name'] for row in raw_data]

    vertical = [convert_to_int(row['Vertical Rise']) for row in raw_data]
    base = [convert_to_int(row['Base Elevation']) for row in raw_data]
    summit = [convert_to_int(row['Summit Elevation']) for row in raw_data]
    snowfall = [convert_to_int(row['Annual Snowfall']) for row in raw_data]
    trails = [convert_to_int(row['Number of Trails']) for row in raw_data]
    acres = [convert_to_int(row['Skiable Acres']) for row in raw_data]
    snowmaking = [convert_to_int(row['Snowmaking']) for row in raw_data]

    cleaned_addresses = [clean_address(row['Address']) for row in raw_data]
    lat_longs = [get_lat_long(address) for address in cleaned_addresses]
    unzipped_lat_longs = list(map(list, zip(*lat_longs)))
    latitudes = unzipped_lat_longs[0]
    longitudes = unzipped_lat_longs[1]

    cleaned_data = list(zip(names, vertical, base, summit, snowfall, trails, acres,
                            snowmaking, latitudes, longitudes))
    pickle.dump(cleaned_data, open('./data/transform_output.pkl', 'wb'))
    print("The raw data has been processed")

if __name__ == "__main__":
    main()
