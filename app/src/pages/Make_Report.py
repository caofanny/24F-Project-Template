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

# Report Form
with st.form("report_form"):
    user_reported = st.text_input("User to Report (User ID):", help="Enter the User ID of the person you are reporting")
    reason = st.text_area("Reason for the Report:", help="Provide a detailed reason for the report")

    # Submit Button
    submit_button = st.form_submit_button("Submit Report")

# Handle form submission
if submit_button:
    if user_reported and reason:
        # Prepare payload
        payload = {
            "UserReported": user_reported,
            "Reason": reason
        }

        # Send data to API
        try:
            response = requests.post("http://api:4000/r/reports", json=payload)
            
            if response.status_code == 200:  # Assuming 201 means "Created"
                st.success("Report successfully submitted!")
            else:
                st.error(f"Failed to submit the report. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
    else:
        st.warning("Please fill out all fields before submitting the report.")


