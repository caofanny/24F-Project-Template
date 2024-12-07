import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import requests
import plotly.express as px
from modules.nav import SideBarLinks


# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Make a Report')

st.write('Here are a couple of graphs and tables that visualize how Co-op search is going for your students!')
