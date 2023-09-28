import streamlit as st
import pandas as pd
from st_pages import Page, show_pages
from PIL import Image
import altair as alt

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
st.write("""
## Top Countries Chart
""")
year = st.slider("Select Year", 2000, 2022, 2011)
top = st.slider("Top Country", 1, country_count, 10)

sort = st.radio("Top methods", ["Highest", "Lowest"], captions= ["Countries with the highest index score", "Countries with the lowest index score"])

if sort == "Highest":
    sort = "DESC"
    x = "-x"
elif sort == "Lowest":
    sort = "ASC" 
    x = "x"


top_countries = sdg.query(f"SELECT country, sdg_index_score FROM sdg WHERE year = {year} ORDER BY sdg_index_score {sort} LIMIT {top};")
top_countries.index = top_countries.index + 1

top_countries["sdg_index_score"] = top_countries["sdg_index_score"].astype(float)
top_chart = (
    alt.Chart(top_countries).mark_bar().encode(
        x=alt.X("sdg_index_score", title='Index Score'),
        y=alt.Y('country',title='Country', sort=f'{x}')
    )
)

st.altair_chart(top_chart, use_container_width=True)
st.dataframe(top_countries)

