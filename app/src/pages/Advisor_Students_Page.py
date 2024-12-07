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
st.header('Your Assigned Students')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

## Backend API URL 
BASE_URL = "" "http://api:4000/u/users"

#fetching the needed data
try:
    response = requests.get(f"{BASE_URL}/advisor/students")
    response.raise_for_status()  # Raise an error for bad HTTP status
    students = response.json()
except requests.exceptions.RequestException as e:
    st.write("**Important**: Could not connect to the API, so using dummy data.")
    students = [
        {"StudentID": 1, "FirstName": "John", "LastName": "Doe", "Email": "john.doe@example.com", "Major": "CS", "College": "Engineering", "CoopStatus": "Searching", "Year": 3, "AdvisorID": 1},
        {"StudentID": 2, "FirstName": "Jane", "LastName": "Smith", "Email": "jane.smith@example.com", "Major": "Math", "College": "Sciences", "CoopStatus": "None", "Year": 2, "AdvisorID": 1},
    ]  # Dummy data if the request fails

st.write("These are your assigned students:")


# Display headers above the data table
header_cols = st.columns([1, 1, 1, 1, 1, 1, 1])  # Adjust column widths as needed
with header_cols[0]:
    st.write("**FirstName**")
with header_cols[1]:
    st.write("**LastName**")
with header_cols[2]:
    st.write("**Email**")
with header_cols[3]:
    st.write("**Year**")
with header_cols[4]:
    st.write ("**CoopStatus**")
with header_cols[5]:
    st.write("**Courses**")
with header_cols[6]:
    st.write("**StudentID**")



#getting the student's that are in that advisors assigned students
assigned_students = list()
assigned_ids = list()

for s in students: 
    if s['AdvisorID'] == 1:
        assigned_students.append(s)
    



# displaying the student info
for student in assigned_students:
    row_cols = st.columns([1, 1, 1, 1, 1, 1, 1])
    with row_cols[0]:
        st.write(student['FirstName'])
    with row_cols[1]:
        st.write(student['LastName'])
    with row_cols[2]:
        st.write(student['Email'])
    with row_cols[3]:
        st.write(student['Year'])
    with row_cols[4]:
        st.write(student['CoopStatus'])
    with row_cols[5]:
        view_courses_button = st.button(f"View {student['FirstName']} {student['LastName']}'s courses")
        #call the method that gets the courses for a student 
        if view_courses_button:
            #saving student information for use in other page
            st.session_state["student_id"] = student['StudentID']
            st.session_state["student_first_name"] = student['FirstName']
            st.session_state["student_last_name"] = student['LastName']
            st.switch_page('pages/Advisor_Student_Courses_Page.py')
    with row_cols[6]:
        st.write(student['StudentID'])









    


