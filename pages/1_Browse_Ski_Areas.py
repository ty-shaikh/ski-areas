import sqlite3

import pandas as pd
from pandas_geojson import to_geojson

import folium
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(layout='wide')
st.title('Browse ski areas')
st.write("""Search for ski areas around the US and Canada by
            using the filters in the sidebar.""")

with st.sidebar:
    vert_to_filter = st.slider('Vertical Descent (feet)', 0, 5000, 0)
    summit_to_filter = st.slider('Summit Elevation (feet)', 0, 15000, 0)
    area_to_filter = st.slider('Skiable Area (acres)', 0, 300, 0)
    longest_run_to_filter = st.slider('Longest Run (miles)', 0, 10, 0)
    snow_to_filter = st.slider('Average Snowfall (inches)', 0, 500, 0)
    snowmaking_to_filter = st.slider('Snowmaking (%)', 0, 100, 0)

attr = """Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)"""

tiles = "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"

m = folium.Map(location=(42.2903, -74.6532), zoom_start=6, tiles=tiles, attr=attr)

# m = folium.Map(location=(42.2903, -74.6532), zoom_start=6, tiles="Cartodb Positron")

# (id, name, vertical, base, summit, snowfall, trails, acres, snowmaking,
#   longest_run, state, latitude, longitude)
connection = sqlite3.connect("./data/load_output.db")
cursor = connection.cursor()
result = cursor.execute(f"""
                        SELECT * FROM areas WHERE vertical >= {vert_to_filter}
                        AND summit >= {summit_to_filter}
                        AND acres >= {area_to_filter}
                        AND longest_run >= {longest_run_to_filter}
                        AND snowfall >= {snow_to_filter}
                        AND snowmaking >= {snowmaking_to_filter}
                        AND latitude != 0;
                        """)

for row in result:
    popup_html = f"""<p style="font-family: Gill Sans, sans-serif;">
            The summit is <b>{f"{row[4]} feet" if row[4] != 0 else "N/A"}</b> high<br>
            Total vertical is <b>{f"{row[2]} feet" if row[2] != 0 else "N/A"}</b><br>
            <b>{f"{row[7]} acres" if row[7] != 0 else "N/A"}</b> to ski<br>
            The longest run is <b>{f"{row[9]} miles" if row[9] != 0 else "N/A"}</b><br>
            <b>{f"{row[5]} inches" if row[5] != 0 else "N/A"}</b> of average snowfall<br>
            <b>{f"{row[8]}%" if row[8] != 0 else "N/A"}</b> of runs have snowmaking<br>
            </p>
            """

    iframe = folium.IFrame(popup_html, width=340, height=140)
    popup = folium.Popup(iframe, max_width=230)
    icon = folium.CustomIcon("./imgs/mtn-icon.png", icon_size=(30, 28))

    tooltip_html = f"<h5>{row[1]}</p>"

    folium.Marker(
        location=[row[11], row[12]],
        tooltip=tooltip_html,
        icon=icon,
        popup=popup).add_to(m)

st_data = st_folium(m, use_container_width=True)
connection.close()
