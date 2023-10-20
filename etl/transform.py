"""Data Transformation

This script processes the raw data.

The script takes a pickle file and outputs another pickle file.

This script requires that 'geocoder' and 'dotenv' be installed within the
local Python environment.
"""

import sys
import re
import time
import pickle

import geocoder
from dotenv import dotenv_values

def get_longest_run(text: str):
    """Parses string and extracts longest run value

    Parameters
    ----------
    text : str
        The text to be cleaned

    Returns
    -------
    float
        A float representing the longest run in miles
    """
    try:
        run_values = re.findall("\d+\.\d+", text)
        run_miles = float(run_values[0])
        return run_miles
    except:
        return 0.0

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
    if text == '':
        return ''

    try:
        address_list = text.split('\n')[1].split(' ')[-6:]
        joined_address = ' '.join(address_list)
        address =  joined_address.replace(u'\xa0', u' ').strip()
        return address
    except:
        return ''

def get_state(address: str):
    """Extracts the state from the input text

    Parameters
    ----------
    address : str
        The address string to be parsed

    Returns
    -------
    string
        A string of the state abbreviation
    """
    if address == '':
        return ''

    try:
        state = address.split(',')[-1].strip().split(' ')[0]
        return state
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
    if address == '':
        return (0, 0)

    try:
        time.sleep(1)
        secrets = dotenv_values("./.env")
        g = geocoder.bing(address, key=secrets["BING_MAPS_API_KEY"])
        results = g.json
        return (results['lat'], results['lng'])
    except:
        return (0, 0)

def main():
    print("Running the transform cleaning script")
    raw_data = pickle.load(open('./data/extract_output.pkl', 'rb'))
    # raw_data = raw_data[:20]

    names = [row['Name'] for row in raw_data]

    vertical = [convert_to_int(row['Vertical Rise']) for row in raw_data]
    base = [convert_to_int(row['Base Elevation']) for row in raw_data]
    summit = [convert_to_int(row['Summit Elevation']) for row in raw_data]
    snowfall = [convert_to_int(row['Annual Snowfall']) for row in raw_data]
    trails = [convert_to_int(row['Number of Trails']) for row in raw_data]
    acres = [convert_to_int(row['Skiable Acres']) for row in raw_data]
    snowmaking = [convert_to_int(row['Snowmaking']) for row in raw_data]
    longest_run = [get_longest_run(row['Longest Run']) for row in raw_data]

    cleaned_addresses = [clean_address(row['Address']) for row in raw_data]
    states = [get_state(address) for address in cleaned_addresses]
    lat_longs = [get_lat_long(address) for address in cleaned_addresses]
    unzipped_lat_longs = list(map(list, zip(*lat_longs)))
    latitudes = unzipped_lat_longs[0]
    longitudes = unzipped_lat_longs[1]

    cleaned_data = list(zip(names, vertical, base, summit, snowfall, trails, acres,
                            snowmaking, longest_run, states, latitudes, longitudes))
    pickle.dump(cleaned_data, open('./data/transform_output.pkl', 'wb'))
    print("The raw data has been processed")

if __name__ == "__main__":
    main()
