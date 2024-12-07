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
st.title('Courses Page')

# Function to Display Courses on the Main Page
def display_courses():
  
  try:
    response  = requests.get('http://api:4000/u/user/alumni/')
    if response.status_code == 200:
      courses_data = response.json()
      
      if courses_data:
        st.dataframe(courses_data)
      else:
        st.write("No Courses found in the database")
        
    else:
      st.write(f"Failed to fetch courses. Status code: {response.status_code}")
  except requests.exceptions.RequestException as e:
    st.write(f"API Error: {str(e)}")
    
display_courses()
