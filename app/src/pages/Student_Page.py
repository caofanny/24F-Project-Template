import logging
import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

# Logger setup
logger = logging.getLogger(__name__)

# Sidebar Links
SideBarLinks()

# Title
st.title("Connected Students Dashboard")

# Hardcoded Alumnus ID for Delora Mulvenna
alumnus_id = 233

# Base API URL
BASE_API_URL = "http://api:4000"

# Function to fetch connected students
def fetch_connected_students(mentor_id):
    """Fetch the list of students connected to the specified mentor ID."""
    try:
        response = requests.get(f"{BASE_API_URL}/u/users/alumnus/{mentor_id}/students")
        if response.status_code == 200:
            students_data = response.json()
            return pd.DataFrame(students_data) if students_data else None
        else:
            st.error(f"Failed to fetch students: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"API Request failed: {str(e)}")
        return None

# Function to add a new connection
def add_connection(mentor_id, student_id):
    """Add a new student connection for the specified mentor ID."""
    try:
        connection_data = {"AlumnusID": mentor_id, "StudentID": student_id}
        response = requests.post(f"{BASE_API_URL}/u/users/alumnus/{mentor_id}/students", json=connection_data)
        if response.status_code == 200:
            st.sidebar.success("Student connection added successfully!")
        else:
            st.sidebar.error(f"Failed to add connection. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.sidebar.warning(f"API Request failed: {str(e)}")

# Display Connected Students
def display_connected_students():
    st.write("### Students Connected to You")

    students_df = fetch_connected_students(alumnus_id)

    if students_df is not None and not students_df.empty:
        st.dataframe(students_df, use_container_width=True)
    else:
        st.write("No students are currently connected to you.")

# Sidebar form to add a new connection
def add_connection_form():
    st.sidebar.write("### Add a New Student Connection")
    student_id = st.sidebar.number_input("Enter Student ID", min_value=1, step=1)
    submitted = st.sidebar.button("Add Connection")

    if submitted:
        if student_id:
            add_connection(alumnus_id, int(student_id))
        else:
            st.sidebar.warning("Please provide a valid Student ID.")

# Main Logic
add_connection_form()
display_connected_students()
