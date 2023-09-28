import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

st.header('SDG Score of Countries Around The World with Interactive Map', divider='rainbow')

# User input
year = st.slider('Select year', 2000, 2022, 2011)

# DB Connection
db = st.experimental_connection('sdg_db', type='sql')

map_df: pd.DataFrame = db.query(f"SELECT latlon.lat, latlon.lon, sdg_index.sdg_index_score, sdg_index.country FROM latlon JOIN sdg_index ON latlon.country = sdg_index.country WHERE sdg_index.year = {year}")
map_df['lat'] = map_df['lat'].astype(float)
map_df['lon'] = map_df['lon'].astype(float)
map_df['sdg_index_score'] = map_df['sdg_index_score'].astype(float)
map_df['country'] = map_df['country'].astype(str)

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=18.82,
        longitude=19.57,
        zoom=1,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'ColumnLayer',
           data=map_df,
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

st.write("""The map above shows the index score of each countries in a map.""")

#################Pyplot Section#################
st.subheader("Comparison of country above and below selected index score", divider='rainbow')

# Input
avg = st.slider('Select index score', 0.0, 100.0, 50.0)

# DB query
# Query result return bytes array, so convert it first
df: pd.DataFrame = db.query(f"SELECT country, sdg_index_score FROM sdg_index WHERE year = {year}")
df['country'] = df['country'].astype(str)
df['sdg_index_score'] = df['sdg_index_score'].astype(float)

above_avg = len(df[(df['sdg_index_score'] >= avg)])
below_avg = len(df[(df['sdg_index_score'] < avg)])
total = len(df)

st.write('Total country: ', total)
st.write('Total country above selected index score: ', above_avg)
st.write('Total country below selected index score: ', below_avg)

col1, col2 = st.columns(2)
# Testing (commented)
# st.dataframe(df.sort_values('sdg_index_score').reset_index(drop=True))
above_score = df[(df['sdg_index_score'] >= avg)].sort_values('sdg_index_score').reset_index(drop=True)
under_score = df[(df['sdg_index_score'] < avg)].sort_values('sdg_index_score').reset_index(drop=True)
above_score.index = above_score.index + 1
under_score.index = under_score.index + 1

with col1:
  st.text('Country above selected index score:')
  st.dataframe(above_score)
with col2:
  st.text('Country below selected index score:')
  st.dataframe(under_score)

ratio = pd.DataFrame({
  'above_avg': [(above_avg/total)],
  'below_avg': [(below_avg/total)]
}).round(2)
ratio.index = ['type']

# Commented
# st.dataframe(ratio)

fig, ax = plt.subplots(1, 1, figsize=(6.5, 2.5))
ax.barh(ratio.index, ratio['above_avg'], color='#00CE15', label='Above Average')
ax.barh(ratio.index, ratio['below_avg'], left=ratio['above_avg'], color='#CB0000', label='Below Average')

fig.patch.set_visible(False)
ax.set_facecolor('none')
# Remove the border (spines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

for i in ratio.index:
  ax.annotate(f"{int(ratio['above_avg'][i]*100)}%", xy=(ratio['above_avg'][i]/2,i), va='center', ha='center', color='white', fontweight='bold', fontsize=30)
  ax.annotate(f"Above selected score", xy=(ratio['above_avg'][i]/2,-0.15), va='center', ha='center', color='white', fontweight='bold', fontsize=10)

  ax.annotate(f"{int(ratio['below_avg'][i]*100)}%", xy=(ratio['above_avg'][i]+ratio['below_avg'][i]/2,i), va='center', ha='center', color='white', fontweight='bold', fontsize=30)
  ax.annotate(f"Below selected score", xy=(ratio['above_avg'][i]+ratio['below_avg'][i]/2,-0.15), va='center', ha='center', color='white', fontweight='bold', fontsize=10)

st.pyplot(fig)

st.write("""
The bar above shows the percentage of countries above and below the selected scores.
""")