"""Streamlit Dashboard

This script presents the data visually in different formats.

The script takes in website URLs and outputs a pickle file.

This script requires that 'streamlit', 'folium' and 'streamlit_folium' be installed within the
local Python environment.
"""

import sqlite3

import folium
import streamlit as st
from streamlit_folium import st_folium

st.title('Find your ideal ski area')
st.write("""Search for ski areas around the US and Canada by
            using the filters in the sidebar.""")

with st.sidebar:
    vert_to_filter = st.slider('Vertical Descent', 0, 2000, 0)
    snow_to_filter = st.slider('Average Snowfall', 0, 300, 0)
    area_to_filter = st.slider('Skiable Acres', 0, 200, 0)


m = folium.Map(location=(42.2903, -74.6532), zoom_start=6, tiles="cartodb positron")

# (id, name, vertical, base, summit, snowfall, trails, acres, state, latitude, longitude)
conn = sqlite3.connect("data/load_output.db")
curs = conn.cursor()
result = curs.execute(f"""
                        SELECT * FROM areas WHERE vertical > {vert_to_filter}
                        AND snowfall > {snow_to_filter}
                        AND acres > {area_to_filter}
                        AND latitude != 0;
                        """)

for row in result:
    html = f"""
            <b>Vertical Descent</b>: {f"{row[2]} feet" if row[2] != 0 else "N/A"}<br>
            <b>Annual Snowfall</b>: {f"{row[5]} inches" if row[5] != 0 else "N/A"}<br>
            <b>Skiable Area</b>: {f"{row[7]} acres" if row[7] != 0 else "N/A"}
            """

    iframe = folium.IFrame(html, width=300, height=80)
    popup = folium.Popup(iframe, max_width=200)

    folium.Marker(
        location=[row[9], row[10]],
        tooltip=row[1],
        popup=popup).add_to(m)

st_data = st_folium(m, width=725)
conn.close()
