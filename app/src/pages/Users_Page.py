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
st.write("# Accessing Users Data from the API")

"""
This page retrieves data about users from a REST API running in a separate backend. 
If the backend is not accessible, dummy data will be used to display.
"""

# Default empty data
users_data = {}

# Try to fetch data from the backend API
try:
    response = requests.get("http://api:4000/u/users").json()
except requests.exceptions.RequestException as e:
    st.write("**Important**: Could not connect to the API, so using dummy data.")


st.subheader("List of inactive Users")

st.dataframe(response)  # Display data as a table

if st.button('Manage Inactive Students', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/User_student_inactive.py')


