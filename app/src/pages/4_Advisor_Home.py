import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Advisor Portal')
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Your Students', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Advisor_Students_Page.py')

if st.button("View Co-op Statistics",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Student_Coop_Page.py')

if st.button('Make a Report', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Make_Report.py')
