import streamlit as st
import pandas as pd
from st_pages import Page, show_pages
from PIL import Image

st.set_page_config(
    page_title="Homepage",
    page_icon="🏠",
)

show_pages(
    [
        Page("app.py", "Homepage", ":house:"),
        Page("pages/details.py", "Details", "📊")
    ]
)

sdg = st.experimental_connection('sdg_db', type='sql')

st.write("""
# SDGs Data Visualization 
""")

img = Image.open("assets/Sustainable_Development_Goals.png")
st.image(img)

st.write("""
## Comparison Chart 
""")

#Comparison input
countries = sdg.query('SELECT DISTINCT country FROM sdg;')
choice_1 = st.selectbox("Pick first country", countries, index=73)
choice_2 = st.selectbox("Pick second country", countries, index=80)

index_1 = sdg.query(f"SELECT year, sdg_index_score FROM sdg WHERE country = '{choice_1}';")
index_2 = sdg.query(f"SELECT year, sdg_index_score FROM sdg WHERE country = '{choice_2}';")
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