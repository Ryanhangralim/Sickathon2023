import streamlit as st
import pandas as pd

sdg = st.experimental_connection('sdg_db', type='sql')
sdgs = ["Goal 1 : No Poverty", "Goal 2 : Zero Hunger", "Goal 3 : Good Health and Well-Being", "Goal 4 : Quality Education", "Goal 5 : Gender Equality", "Goal 6 : Clean Water and Sanitation", "Goal 7 : Affordable and Clean Energy", "Goal 8 : Decent Work and Economic Growth", "Goal 9 : Industry Innovation and Infrastructure", "Goal 10 : Reduces Inequalities", "Goal 11 : Sustainable Cities and Communities", "Goal 12 : Responsible Consumption and Production", "Goal 13 : Climate Action", "Goal 14 : Life Below Water", "Goal 15 : Life on Land", "Goal 16 : Peace, Justice and Strong Insitutions", "Goal 17 : Partnerships for the Goals"]

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
st.line_chart(all, x="year")
st.dataframe(all, hide_index=True)

goals = st.multiselect("Select goals to view", sdgs, ["Goal 1 : No Poverty", "Goal 2 : Zero Hunger"])
print(goals)
print(len(goals))

#print index chart
if(len(goals)>0):
    for i in range(len(goals)):
        index = sdgs.index(goals[i])
        print(index)
        st.write(f"""### {goals[i]}""")
        goal = get_goal(choice, index+1)
        print(goal)
        st.line_chart(goal, x='year', y=f'goal_{index+1}_score')
