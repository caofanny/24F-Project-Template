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

# set the header of the page
st.write(f"### Hi, {st.session_state['first_name']}. these are your current mentors:")

## Backend API URL 
BASE_URL = "" "http://api:4000/u/users"


#fetching the needed data, gets all of the students in the database
try:
    response = requests.get(f"{BASE_URL}/students")
    response.raise_for_status()  # Raise an error for bad HTTP status
    students = response.json()
except requests.exceptions.RequestException as e:
    st.write("**Important**: Could not connect to the API, so using dummy data.")


for s in students:
    st.write(f"{s}")








