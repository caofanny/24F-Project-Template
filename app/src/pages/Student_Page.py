import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import logging
import sqlite3
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

# Logger Setup
logger = logging.getLogger(__name__)

# Sidebar Links
SideBarLinks()

# Title
st.title("Mentor-Student Management Dashboard")

# Sidebar Menu
menu_options = ["View Connected Students", "Add Connection", "Remove Connection"]
choice = st.sidebar.radio("Select an option:", menu_options)
back = st.sidebar.button("Back")

# Mentor ID for the current logged-in user (example value)
mentor_id = 233  # Replace this with dynamic session state or login data

# Database Connection
def get_db_connection():
    """Establish and return a database connection."""
    return sqlite3.connect('mentorship.db')

# Fetch Connected Students
def fetch_connected_students(mentor_id):
    """Fetch students connected to the logged-in mentor."""
    query = """
        SELECT students.StudentID AS ID, students.FirstName, students.LastName, 
               students.Email, students.College, students.Major, students.Year, students.Num_Coops AS Coops, 
               students.CoopStatus
        FROM Student AS students
        INNER JOIN Alumni_Mentors ON students.StudentID = Alumni_Mentors.StudentID
        WHERE Alumni_Mentors.AlumnusID = 
    """
    try:
        conn = get_db_connection()
        students_df = pd.read_sql_query(query, conn, params=(mentor_id,))
        conn.close()
        return students_df
    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        st.error("An error occurred while fetching student data. Please check your database.")
        return pd.DataFrame()

# Display Connected Students
def display_connected_students(mentor_id):
    """Display connected students in a table."""
    st.write("### Students Connected to You")
    students_df = fetch_connected_students(mentor_id)
    if not students_df.empty:
        st.dataframe(students_df, use_container_width=True)
    else:
        st.write("No students are currently connected to you.")

# Add Student Connection
def add_student_connection(mentor_id):
    st.sidebar.write("### Add a New Student Connection")
    student_id = st.sidebar.number_input("Enter Student ID", min_value=1, step=1)
    submitted = st.sidebar.button("Add Connection")

    if submitted:
        try:
            conn = get_db_connection()
            query = "INSERT INTO Alumni_Mentors (StudentID, AlumnusID) VALUES (?, ?)"
            conn.execute(query, (student_id, mentor_id))
            conn.commit()
            conn.close()
            st.sidebar.success("Student connection added successfully!")
        except sqlite3.IntegrityError:
            st.sidebar.error("This connection already exists.")
        except Exception as e:
            logger.error(f"Error adding connection: {e}")
            st.sidebar.error("Failed to add connection. Please check your database.")

# Remove Student Connection
def remove_student_connection(mentor_id):
    st.sidebar.write("### Remove a Student Connection")
    student_id = st.sidebar.number_input("Enter Student ID to Remove", min_value=1, step=1)
    submitted = st.sidebar.button("Remove Connection")

    if submitted:
        try:
            conn = get_db_connection()
            query = "DELETE FROM Alumni_Mentors WHERE StudentID = ? AND AlumnusID = ?"
            conn.execute(query, (student_id, mentor_id))
            conn.commit()
            conn.close()
            st.sidebar.success("Student connection removed successfully!")
        except Exception as e:
            logger.error(f"Error removing connection: {e}")
            st.sidebar.error("Failed to remove connection. Please check your database.")

# Show Sidebar Forms Based on Selection
if choice == "View Connected Students":
    display_connected_students(mentor_id)
elif choice == "Add Connection":
    add_student_connection(mentor_id)
elif choice == "Remove Connection":
    remove_student_connection(mentor_id)

if back:
    st.switch_page('pages/Mentor_Home.py')

