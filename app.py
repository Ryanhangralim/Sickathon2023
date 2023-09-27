import streamlit as st
import pandas as pd
from st_pages import Page, show_pages
from PIL import Image

st.set_page_config(
    page_title="Homepage",
    page_icon=":house:",
)

# show_pages(
#     [
#         Page("app.py", "Homepage", ":house:"),
#         Page("pages/Details.py", "Details", ":chart:")
#     ]
# )

sdg = st.experimental_connection('sdg_db', type='sql')
st.write("""
# SDGs Data Visualization 
""")

img = Image.open("assets/Sustainable_Development_Goals.png", mode="r")
st.image(img)

st.write("""
## Comparison Chart 
""")

#Comparison input
countries = sdg.query('SELECT DISTINCT country FROM sdg;')
country_count = sdg.query('SELECT count(*) FROM (SELECT DISTINCT country FROM sdg);')
country_count = int(country_count["count(*)"])
choice_1 = st.selectbox("Pick first country", countries, index=73)
choice_2 = st.selectbox("Pick second country", countries, index=80)

index_1 = sdg.query(f'SELECT year, sdg_index_score FROM sdg WHERE country = "{choice_1}";')
index_2 = sdg.query(f'SELECT year, sdg_index_score FROM sdg WHERE country = "{choice_2}";')
index_1["sdg_index_score"] = index_1["sdg_index_score"].astype(float)
index_2["sdg_index_score"] = index_2["sdg_index_score"].astype(float)
df = pd.DataFrame(
    {
        'Year': index_1["year"],
        f'{choice_1}': index_1["sdg_index_score"],
        f'{choice_2}': index_2["sdg_index_score"],
    },
    columns=['Year', f'{choice_1}', f'{choice_2}']
)
st.line_chart(df, x="Year", y=[f'{choice_1}', f'{choice_2}'])

#Select top countries
year = st.slider("Select Year", 2000, 2022, 2011)
top = st.slider("Top Country", 1, country_count, 10)
top_countries = sdg.query(f"SELECT country, sdg_index_score FROM sdg WHERE year = {year} ORDER BY sdg_index_score DESC LIMIT {top};")
top_countries.index = top_countries.index + 1
st.dataframe(top_countries)