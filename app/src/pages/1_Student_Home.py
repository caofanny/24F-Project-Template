import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title('Student Portal')
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Mentors', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Mentor_Page.py')

if st.button('View Courses', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Student_Courses_Page.py')

if st.button('View Profile',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Student_Profile_Page.py')

if st.button('Make a Report',
             type='primary',
            use_container_width=True):
   st.switch_page('pages/Make_Report')

