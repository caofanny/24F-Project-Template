import logging
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Set up logger
logger = logging.getLogger(__name__)

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# Set the header of the page
st.write("# Manage Inactive Students")

"""
This page retrieves data about users from a REST API running in a separate backend. 
If the backend is not accessible, dummy data will be used to display.
"""

# Backend API URL
BASE_URL = "http://api:4000/u/users"  # Update with the correct URL for your API

# Try to fetch data from the backend API
try:
    response = requests.get(f"{BASE_URL}/students/inactive")
    response.raise_for_status()  # Raise an error for bad HTTP status
    inactive_students = response.json()
except requests.exceptions.RequestException as e:
    st.write("**Important**: Could not connect to the API, so using dummy data.")
    inactive_students = [
        {"StudentID": 1, "FirstName": "John", "LastName": "Doe", "Email": "john.doe@example.com", "Major": "CS", "College": "Engineering", "CoopStatus": "Searching", "Year": 3},
        {"StudentID": 2, "FirstName": "Jane", "LastName": "Smith", "Email": "jane.smith@example.com", "Major": "Math", "College": "Sciences", "CoopStatus": "None", "Year": 2},
    ]  # Dummy data if the request fails

# Display the list of inactive students
st.write("List of students who are generally inactive:")

# Create columns for the table headers manually
columns = ['FirstName', 'LastName', 'Email', 'LastLogin', 'CoopStatus', 'Year', 'Action']

# Display headers above the data table
header_cols = st.columns([1, 1, 1, 1, 1, 1, 1])  # Adjust column widths as needed
with header_cols[0]:
    st.write("FirstName")
with header_cols[1]:
    st.write("LastName")
with header_cols[2]:
    st.write("Email")
with header_cols[3]:
    st.write("LastLogin")
with header_cols[4]:
    st.write("CoopStatus")
with header_cols[5]:
    st.write("Year")
with header_cols[6]:
    st.write("Action")

# Iterate through the student data and display each student in a row with a delete button
for student in inactive_students:
    row_cols = st.columns([1, 1, 1, 1, 1, 1, 1,])  # Same column width for each row
    
    with row_cols[0]:
        st.write(student['FirstName'])
    with row_cols[1]:
        st.write(student['LastName'])
    with row_cols[2]:
        st.write(student['Email'])
    with row_cols[3]:
        st.write(student['LastLogin'])
    with row_cols[4]:
        st.write(student['CoopStatus'])
    with row_cols[5]:
        st.write(student['Year'])
    with row_cols[6]:
        delete_button = st.button(f"Delete {student['FirstName']} {student['LastName']}", key=student["StudentID"])
        if delete_button:
            # Call the delete function for the student (backend API)
            try:
                delete_response = requests.delete(f"{BASE_URL}/{student['StudentID']}")
                delete_response.raise_for_status()  
                st.success(f"User {student['FirstName']} {student['LastName']} deleted successfully!")
                st.experimental_rerun()  
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to delete user {student['FirstName']} {student['LastName']}: {e}")
