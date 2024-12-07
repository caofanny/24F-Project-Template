import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Here are the Student Courses For:')

## Backend API URL 
BASE_URL = "http://api:4000/u/users"

#getting the data for the courses a specific student is taking 

st.write(f"### These are the courses that {st.session_state['student_first_name']} is taking currently:")

#fetching the needed data
try:
    response = requests.get(f'{BASE_URL}/students/courses/{st.session_state["student_id"]}')
    response.raise_for_status()  # Raise an error for bad HTTP status
    st.write(f"Response Status: {response.status_code}")
    st.write(f"Response Data: {response.text}")
    courses = response.json()
except requests.exceptions.RequestException as e:
      # Dummy data if the request fails
    courses = [
        {"CoursesID": 1, 'Name': "Algorithms and Data", "Professor": "Andrew Van der Poel", "Description": "Fundamentals of algorithm design." },
        {"CoursesID": 3, 'Name': "OOD", "Professor": "Mark Fontenot", "Description": "OOD Principlles." }

    ]


st.write("Courses:")

# displaying headers
# Display headers above the data table
header_cols = st.columns([1, 1, 1, 1])  # Adjust column widths as needed
with header_cols[0]:
    st.write("**Course ID**")
with header_cols[1]:
    st.write("**Course Name**")
with header_cols[2]:
    st.write("**Proffessor**")
with header_cols[3]:
    st.write("**Course Description**")



#displaying the course info
for course in courses:
    row_cols = st.columns([1, 1, 1, 1, 1, 1, 1])
    with row_cols[0]:
        st.write(course['CoursesID'])
    with row_cols[1]:
        st.write(course['Name'])
    with row_cols[2]:
        st.write(course['Professor'])
    with row_cols[3]:
        st.write(course['Description'])





