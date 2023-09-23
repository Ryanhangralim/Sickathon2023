import streamlit as st
import pandas as pd

def get_goal(choice, num):
    goal = sdg.query(f"SELECT year, goal_{num}_score FROM sdg WHERE country = '{choice}'")
    goal[f"goal_{num}_score"] = goal[f"goal_{num}_score"].astype(float)
    return goal

sdg = st.experimental_connection('sdg_db', type='sql')
st.write("""
# SDGs Data Visualization 
""")

#User choicebox
country = sdg.query('SELECT DISTINCT country FROM sdg;')
choice = st.selectbox("Pick a country", country, index=73)


#test goal_1
st.write("""Goal 1""")
goal_1 = get_goal(choice, 1)
st.dataframe(goal_1)
st.bar_chart(goal_1, x='year', y='goal_1_score')
st.line_chart(goal_1, x='year', y='goal_1_score')

# year = st.slider("Pick a year", 2000, 2022)

all = sdg.query(f"SELECT year, goal_1_score, goal_2_score, goal_3_score, goal_4_score, goal_5_score, goal_6_score, goal_7_score, goal_8_score, goal_9_score, goal_10_score, goal_11_score, goal_12_score, goal_13_score, goal_14_score, goal_15_score, goal_16_score, goal_17_score FROM sdg WHERE country = '{choice}';")
for i in range(1, 18):
    all[f"goal_{i}_score"] = all[f"goal_{i}_score"].astype(float)
st.line_chart(all, x="year")
st.dataframe(all)