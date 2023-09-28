import streamlit as st
import pandas as pd
import pydeck as pdk
from MySQLdb import _mysql
import matplotlib.pyplot as plt

host = 'sql12.freesqldatabase.com'
user = 'sql12649391'
password = 'uM2sjJuZT2'
database = 'sql12649391'

db = _mysql.connect(host=host, user=user, password=password, database=database)

st.header("SDGs index score overview")

# User input
year = st.slider('Select year', 2000, 2022, 2011)
avg = st.slider('Select index score', 0.0, 100.0, 50.0)

# DB query
db.query(f"SELECT country, sdg_index_score FROM sdg_index WHERE year = {year}")
r = db.store_result()
result = r.fetch_row(0, 1)

# Query result return bytes array, so convert it first
df: pd.DataFrame = pd.DataFrame(result)
df['country'] = df['country'].astype(str)
df['sdg_index_score'] = df['sdg_index_score'].astype(float)

above_avg = len(df[(df['sdg_index_score'] >= avg)])
below_avg = len(df[(df['sdg_index_score'] < avg)])
total = len(df)

st.subheader('', divider='rainbow')
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

st.subheader('', divider='rainbow')
st.pyplot(fig)