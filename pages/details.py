import streamlit as st
import pandas as pd

sdg = st.experimental_connection('sdg_db', type='sql')
sdgs = ["No Poverty", "Zero Hunger", "Good Health and Well-Being", "Quality Education", "Gender Equality", "Clean Water and Sanitation", "Affordable and Clean Energy", "Decent Work and Economic Growth", "Industry Innovation and Infrastructure", "Reduces Inequalities", "Sustainable Cities and Communities", "Responsible Consumption and Production", "Climate Action", "Life Below Water", "Life on Land", "Peace, Justice and Strong Insitutions", "Partnerships for the Goals"]

def get_goal(choice, num):
    goal = sdg.query(f"SELECT year, goal_{num}_score FROM sdg WHERE country = '{choice}'")
    goal[f"goal_{num}_score"] = goal[f"goal_{num}_score"].astype(float)
    return goal

st.write("""
# SDGs Data Visualization 
""")

#User choicebox
country = sdg.query('SELECT DISTINCT country FROM sdg;')
choice = st.selectbox("Pick a country", country, index=73)

#all chart
all = sdg.query(f"SELECT year, sdg_index_score, goal_1_score, goal_2_score, goal_3_score, goal_4_score, goal_5_score, goal_6_score, goal_7_score, goal_8_score, goal_9_score, goal_10_score, goal_11_score, goal_12_score, goal_13_score, goal_14_score, goal_15_score, goal_16_score, goal_17_score FROM sdg WHERE country = '{choice}';")
for i in range(1, 18):
    all[f"goal_{i}_score"] = all[f"goal_{i}_score"].astype(float)
all["sdg_index_score"] = all['sdg_index_score'].astype(float)
st.line_chart(all, x="year", width=1500)
st.dataframe(all, hide_index=True)

#print index chart
on = st.toggle("SDG Index Score", value=True)
if on:
    st.write("""SDG Index Score""")
    goal = sdg.query(f"SELECT year, sdg_index_score FROM sdg WHERE country = '{choice}'")
    goal["sdg_index_score"] = goal["sdg_index_score"].astype(float)
    st.line_chart(goal, x='year', y='sdg_index_score')

#printing single chart
for i in range(1, 18):
    on = st.toggle(f"Goal {i}: {sdgs[i-1]}", value=True)
    if on:
        st.write(f"""Goal {i} score""")
        goal = get_goal(choice, i)
        st.line_chart(goal, x='year', y=f'goal_{i}_score')