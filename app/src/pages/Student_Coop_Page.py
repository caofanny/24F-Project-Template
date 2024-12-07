import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import requests
import plotly.express as px
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Current Coop Search Stats:')

#let's get the information we need for the coop search status 

## Backend API URL 
BASE_URL = "" "http://api:4000/u/users"

#fetching the needed data
try:
    response = requests.get(f"{BASE_URL}/advisor/students")
    response.raise_for_status()  # Raise an error for bad HTTP status
    students = response.json()
except requests.exceptions.RequestException as e:
    students = [
        {"StudentID": 1, "FirstName": "John", "LastName": "Doe", "Email": "john.doe@example.com", "Major": "CS", "College": "Engineering", "CoopStatus": "Searching", "Year": 3, "AdvisorID": 1},
        {"StudentID": 2, "FirstName": "Jane", "LastName": "Smith", "Email": "jane.smith@example.com", "Major": "Math", "College": "Sciences", "CoopStatus": "None", "Year": 2, "AdvisorID": 1},
    ]  # Dummy data if the request fails



#getting the student's that are in that advisors assigned students
assigned_students = list()
assigned_ids = list()

for s in students: 
    if s['AdvisorID'] == 1:
        assigned_students.append(s)



with_coops = list()
without_coops = list()
#now from those students let's get the ones with coops secured
for s in assigned_students:
    if s['CoopStatus'] == 'Found co-op':
        with_coops.append(s)  
    else:
        without_coops.append(s)

#now that we have the info make it into a datafram
df_found_coops = pd.DataFrame(with_coops)

#removing unnecssary columns
df_found_coops.drop('AdvisorID', axis=1, inplace=True)

df_without_coops = pd.DataFrame(without_coops)

#removing unnecssary columns
df_without_coops.drop('AdvisorID', axis=1, inplace=True)


# Making tables 
st.subheader("Students with Co-ops :partying_face:")
if not df_found_coops.empty:
    st.dataframe(df_found_coops)
else:
    st.write("No students have co-ops yet.")

# Display tables for students who are still searching
st.subheader("Students Still Searching for Co-ops :mag_right:")
if not df_without_coops.empty:
    st.dataframe(df_without_coops)
else:
    st.write("All assigned students have found co-ops.")


