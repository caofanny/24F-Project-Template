import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title('System Administator Portal')
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Manage Users', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Users_Page.py')

if st.button('View User Activity', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Users_Activity_Page.py')

if st.button("View Reports",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Reports_Page.py')