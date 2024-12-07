import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import requests
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()


st.title("Alumni Dashboard")

# Function to Display Courses on the Main Page
def display_courses():
    st.write("### All Alumni")
    try:
        response = requests.get("http://api:4000/u/users/alumni")  # Assuming courses endpoint
        if response.status_code == 200:
            data = response.json()

            if data:
                st.dataframe(data, use_container_width=True)
            else:
                st.write("No alumni found in the database.")

        else:
            st.error(f"Failed to fetch alumni. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")

# Main Page - Display Courses
display_courses()








