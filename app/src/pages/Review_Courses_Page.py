import logging
import requests
import streamlit as st

# Logger setup
logger = logging.getLogger(__name__)

# Title
st.title("Course Dashboard")

# Sidebar Menu
back = st.sidebar.button("Back")

# Function to Display Courses on the Main Page
def display_courses():
    st.write("### All Courses")
    try:
        response = requests.get("http://api:4000/c/courses")  # Assuming courses endpoint
        if response.status_code == 200:
            courses_data = response.json()

            if courses_data:
                st.dataframe(courses_data, use_container_width=True)
            else:
                st.write("No courses found in the database.")

        else:
            st.error(f"Failed to fetch courses. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")

# Main Page - Display Courses
display_courses()

# Navigation Button to Reviews Page
if st.button("Go to Reviews"):
    st.switch_page('pages/Review_Management.py')  # Replace with actual page name

if back:
    st.switch_page('pages/3_Mentor_Home.py')
