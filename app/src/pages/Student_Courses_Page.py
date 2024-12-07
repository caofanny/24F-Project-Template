import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
import numpy as np
from modules.nav import SideBarLinks

# Set up logger
logger = logging.getLogger(__name__)

SideBarLinks()

# Sets title
st.title('Course Page')

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