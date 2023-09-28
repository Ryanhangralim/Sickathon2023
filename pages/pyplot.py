import streamlit as st
import pandas as pd
import pydeck as pdk
from MySQLdb import _mysql
import matplotlib.pyplot as plt

host = 'localhost'
user = 'root'
password = 'Mismag0203i9'
database = 'sdg_streamlit'

db = _mysql.connect(host=host, user=user, password=password, database=database)

year = st.slider('Select year', 2000, 2022, 2011)
avg = st.slider('Select average', 0.0, 100.0, 50.0)

# DB query
db.query(f"SELECT country, sdg_index_score FROM sdg_index WHERE year = {year}")
r = db.store_result()
result = r.fetch_row(0, 1)

df: pd.DataFrame = pd.DataFrame(result)
df['country'] = df['country'].astype(str)
df['sdg_index_score'] = df['sdg_index_score'].astype(float)
st.dataframe(df.sort_values('sdg_index_score').reset_index())

st.dataframe(df[(df['sdg_index_score'] >= avg)].reset_index())
st.dataframe(df[(df['sdg_index_score'] < avg)].reset_index())

above_avg = len(df[(df['sdg_index_score'] >= avg)])
below_avg = len(df[(df['sdg_index_score'] < avg)])
total = len(df)

st.write('Total above average: ', above_avg)
st.write('Total below average: ', below_avg)
st.write('Total country: ', total)

ratio = pd.DataFrame({
  'above_avg': [(above_avg/total)],
  'below_avg': [(below_avg/total)]
}).round(2)
ratio.index = ['type']

st.dataframe(ratio)

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
  ax.annotate(f"Above average", xy=(ratio['above_avg'][i]/2,-0.15), va='center', ha='center', color='white', fontweight='bold', fontsize=10)

  ax.annotate(f"{int(ratio['below_avg'][i]*100)}%", xy=(ratio['above_avg'][i]+ratio['below_avg'][i]/2,i), va='center', ha='center', color='white', fontweight='bold', fontsize=30)
  ax.annotate(f"Below average", xy=(ratio['above_avg'][i]+ratio['below_avg'][i]/2,-0.15), va='center', ha='center', color='white', fontweight='bold', fontsize=10)


st.pyplot(fig)