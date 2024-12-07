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

st.write("We value our community guidelines greatly and if you feel like they were violated, please make a report:")

BASE_URL = "http://api:4000/r/reports"  # Adjust the URL as needed

#form that will get the input from the user
with st.form("report_form"):
        user_reported = st.text_input("User Reported (UserID):", "")
        report_reason = st.text_area("Reason for the Report:")
        submit_button = st.form_submit_button("Submit Report")


#uploading the new user into the database
if submit_button:
    if user_reported and report_reason:
        try:
            # Prepare the data payload
            user_data = {
                "UserReported": user_reported,
                "Reason": report_reason,
            }
            # Send POST request
            response = requests.post(BASE_URL, json=user_data)
            if response.status_code == 200:
                st.success("Report successfully submitted")
            else:
                st.error(f"Failed to create report: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please fill in all fields.")
    


    
        




