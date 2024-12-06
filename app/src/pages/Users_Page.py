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
    
    # Check if the request was successful
    #if response.status_code == 200:
    #    users_data = response.json()  # Parse the JSON response into a dictionary
    #else:
    #    st.warning(f"Failed to fetch data. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    st.write("**Important**: Could not connect to the API, so using dummy data.")
    # Fallback to dummy data if the API request fails
    users_data = [
        {"UserID": 1, "FirstName": "John", "LastName": "Doe", "Email": "john.doe@example.com", "Status": "Active"},
        {"UserID": 2, "FirstName": "Jane", "LastName": "Smith", "Email": "jane.smith@example.com", "Status": "Inactive"},
        {"UserID": 3, "FirstName": "Tom", "LastName": "Brown", "Email": "tom.brown@example.com", "Status": "Active"},
    ]


# Display the users data as a table
st.subheader("Users List")
if isinstance(users_data, list):  # Checking if data is in list format
    st.dataframe(users_data)  # Display data as a table
else:
    st.write("No user data to display.")
