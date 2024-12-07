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

# Fetch connected students
def fetch_connected_students(mentor_id):
    """Fetch the list of students connected to the specified mentor ID."""
    try:
        with st.spinner("Fetching connected students..."):
            response = requests.get(f"{BASE_API_URL}/u/users/alumnus/{mentor_id}/students")
            if response.status_code == 200:
                students_data = response.json()
                return pd.DataFrame(students_data) if students_data else None
            elif response.status_code == 404:
                st.info("No students connected to this mentor.")
                return None
            else:
                st.error(f"Failed to fetch students: {response.status_code}")
                return None
    except requests.exceptions.RequestException as e:
        st.error(f"API Request failed: {str(e)}")
        return None

# Add a new connection
def add_connection(mentor_id, student_id):
    """Add a new student connection for the specified mentor ID."""
    try:
        connection_data = {"AlumnusID": mentor_id, "StudentID": student_id}
        response = requests.post(f"{BASE_API_URL}/u/users/alumnus/{mentor_id}/students", json=connection_data)
        if response.status_code == 200:
            st.sidebar.success("Student connection added successfully!")
            st.experimental_rerun()
        else:
            st.sidebar.error(f"Failed to add connection. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.sidebar.warning(f"API Request failed: {str(e)}")

# Remove an existing connection
def remove_connection(mentor_id, student_id):
    """Remove a student connection for the specified mentor ID."""
    try:
        response = requests.delete(f"{BASE_API_URL}/u/users/alumnus/{mentor_id}/students/{student_id}")
        if response.status_code == 200:
            st.success(f"Successfully removed connection with Student ID {student_id}.")
            st.experimental_rerun()
        else:
            st.error(f"Failed to remove connection. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"API Request failed: {str(e)}")

# Display connected students
def display_connected_students():
    st.write("### Students Connected to You")

    students_df = fetch_connected_students(alumnus_id)

    if students_df is not None and not students_df.empty:
        # Add a delete button for each student row
        for index, row in students_df.iterrows():
            cols = st.columns([4, 2])
            with cols[0]:
                st.write(f"**{row['FirstName']} {row['LastName']}**")
                st.write(f"Email: {row['Email']}")
                st.write(f"Major: {row.get('Major', 'N/A')}")
            with cols[1]:
                if st.button(f"Remove {row['FirstName']} {row['LastName']}", key=row['StudentID']):
                    remove_connection(alumnus_id, row['StudentID'])
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
