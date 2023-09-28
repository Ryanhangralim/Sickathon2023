import streamlit as st
import pandas as pd
import pydeck as pdk
from MySQLdb import _mysql

host = 'sql12.freesqldatabase.com'
user = 'sql12649391'
password = 'uM2sjJuZT2'
database = 'sql12649391'

# Year input slider
sdg_year: int = st.slider('Select year', 2000, 2022, 2011)

db = _mysql.connect(host=host, user=user, password=password, database=database)

# DB query
db.query(f"SELECT latlon.lat, latlon.lon, sdg_index.sdg_index_score, sdg_index.country FROM latlon JOIN sdg_index ON latlon.country = sdg_index.country WHERE sdg_index.year = {sdg_year}")
r = db.store_result()
result = r.fetch_row(0, 1)

df: pd.DataFrame = pd.DataFrame(result)
df['lat'] = df['lat'].astype(float)
df['lon'] = df['lon'].astype(float)
df['sdg_index_score'] = df['sdg_index_score'].astype(float)
df['country'] = df['country'].astype(str)
st.dataframe(df)

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=-2.4833826,
        longitude=117.8902853,
        zoom=5,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'ColumnLayer',
           data=df,
           get_position='[lon, lat]',
           get_elevation='sdg_index_score',
           radius=50000,
           elevation_scale=15000,
           pickable=True,
           get_fill_color=[255, 50, 0, 70]
        ),
    ],
    tooltip = {
    "html": "<b>{country}</br> SDG Index Score:<b>{sdg_index_score}</b> NTD/sqm",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
    }
))