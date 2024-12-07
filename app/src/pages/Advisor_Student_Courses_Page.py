import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import requests


back = st.sidebar.button("Back")

# set the header of the page
st.header('Here are the Student Courses For:')

## Backend API URL 
BASE_URL = "http://api:4000/u/users"

#getting the data for the courses a specific student is taking 

st.write(f"### These are the courses that the student is taking currently:")

#fetching the needed data
try:
    #response = requests.get(f'{BASE_URL}/students/courses/{st.session_state["student_id"]}')
    response = requests.get(f'{BASE_URL}/students/courses/2')
    if response.status_code == 200:
        courses = response.json()
    else:
            st.write(f"Failed to fetch courses. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
      # Dummy data if the request fails
    courses = [
        {"CoursesID": 1, 'Name': "Algorithms and Data", "Professor": "Andrew Van der Poel", "Description": "Fundamentals of algorithm design." },
        {"CoursesID": 3, 'Name': "OOD", "Professor": "Mark Fontenot", "Description": "OOD Principles." }

    ]


st.write("Courses:")

header_cols = st.columns([1, 2, 2, 3])  # Adjust column widths
with header_cols[0]:
    st.write("**Course ID**")
with header_cols[1]:
    st.write("**Course Name**")
with header_cols[2]:
    st.write("**Professor**")
with header_cols[3]:
    st.write("**Description**")



# Display each course
for course in courses:
    row_cols = st.columns([1, 2, 2, 3])
    with row_cols[0]:
        st.write(course.get('CoursesID', 'N/A'))
    with row_cols[1]:
        st.write(course.get('Name', 'N/A'))
    with row_cols[2]:
        st.write(course.get('Professor', 'N/A'))
    with row_cols[3]:
        st.write(course.get('Description', 'N/A'))

if back:
    st.switch_page('pages/Advisor_Students_Page.py')



