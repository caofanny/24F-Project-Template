import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests
from datetime import datetime

# Navigation Sidebar
SideBarLinks()
#logout = st.sidebar.button("Logout", key="logout_button")

# About Us Section
st.write("# About Us")

st.markdown(
    """
    U-Connect is a data-driven, student-centric networking platform that 
    empowers students by providing direct access to peer-generated insights 
    and experiences. Through detailed profiles showcasing academic courses, 
    co-op placements, and study-abroad opportunities, students can easily connect 
    with others who have faced similar academic and professional challenges. 
    This platform collects and analyzes real student data, helping users make 
    informed decisions about courses, co-ops, and career paths.
    """
)

# Make a Report Section
st.write("# Make a Report")

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

