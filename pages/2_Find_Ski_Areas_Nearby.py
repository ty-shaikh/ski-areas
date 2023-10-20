import sqlite3

import geocoder
from geopy import distance
import pandas as pd

import streamlit as st
from st_aggrid import AgGrid

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
        g = geocoder.bing(address, key=st.secrets["bing_maps_key"])
        results = g.json
        return (results['lat'], results['lng'])
    except:
        return (0, 0)

def find_distance(input_location, database_row):
    """Finds the distance between two coordinates

    Parameters
    ----------
    input_location : tuple
        The user input converted to a tuple of latitude and longitude values
    database_row : tuple
        A tuple of the given database row

    Returns
    -------
    tuple
        A tuple containing the distance between plus other relevant ski area info
    """
    name = database_row[0]
    vertical = database_row[3]
    acres = database_row[4]
    snowfall = database_row[5]
    database_location = (database_row[1], database_row[2])
    distance_between = round(distance.distance(input_location, database_location).miles, 1)
    return (name, distance_between, vertical, acres, snowfall)

st.set_page_config(layout='wide')
st.title('Find nearby ski areas')

connection = sqlite3.connect("./data/load_output.db")
cursor = connection.cursor()
db_results = cursor.execute("""SELECT name, latitude, longitude, vertical, acres,
                                snowfall FROM areas WHERE latitude != 0;""")

with st.form("my_form"):
   st.write("Fill out the fields to see what's nearby.")
   zip_code_value = st.text_input('Your zip code')
   miles_value = st.number_input('How many miles away')
   submitted = st.form_submit_button("Submit")

if submitted:
  user_lat_long = get_lat_long(zip_code_value)
  distances_between = [find_distance(user_lat_long, row) for row in db_results]
  nearby_areas = list(filter(lambda x: x[1] < miles_value, distances_between))
  df = pd.DataFrame(nearby_areas, columns=['Name', 'Distance (miles)', 'Vertical Descent (feet)',
                                            'Skiable Area (acres)', 'Annual Snowfall (inches)'])
  df.sort_values(by='Distance (miles)', inplace=True)
  AgGrid(df)

connection.close()
