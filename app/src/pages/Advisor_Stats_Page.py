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

# set the header of the page
st.header('Welcome to the Advisor Stats Page')

st.write('Here are a couple of graphs and tables that visualize how Co-op search is going for your students!')

## Backend API URL 
BASE_URL = "" "http://api:4000/u/users"

#fetching the needed data, gets all of the students in the database
try:
    response = requests.get(f"{BASE_URL}/advisor/students")
    response.raise_for_status()  # Raise an error for bad HTTP status
    students = response.json()
except requests.exceptions.RequestException as e:
    st.write("**Important**: Could not connect to the API, so using dummy data.")
    students = [
        {"StudentID": 1, "FirstName": "John", "LastName": "Doe", "Email": "john.doe@example.com", "Major": "CS", "College": "Engineering", "CoopStatus": "Searching", "Year": 3, "AdvisorID": 1},
        {"StudentID": 2, "FirstName": "Jane", "LastName": "Smith", "Email": "jane.smith@example.com", "Major": "Math", "College": "Sciences", "CoopStatus": "None", "Year": 2, "AdvisorID": 1},
    ]  # Dummy data if the request fails


#this is filtering out to only get the students, assigned to the advisor
#getting the student's that are in that advisors assigned students
assigned_students = list()
assigned_ids = list()

for s in students: 
    if s['AdvisorID'] == 1:
        assigned_students.append(s)


#-----------------------------------
#GETTING INFORMATION ABOUT COOP STATUS STATS

with_coops = list()
without_coops = list()
not_searching = list()

#now from those students let's get the ones with coops secured
for s in assigned_students:
    if s['CoopStatus'] == 'Found co-op':
        with_coops.append(s)  
    if s['CoopStatus'] == 'Searching':
        without_coops.append(s)
    if s['CoopStatus'] == 'Not Searching':
        not_searching.append(s)


#Let's make a pie chart with the data
labels = ['With Co-ops', 'Without Co-ops', 'Not Searching']
sizes = [len(with_coops), len(without_coops), len(not_searching)]
#coloring the pie chart
colors = ['#4CAF50', '#FFC107', '#FF5722']  

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})

plt.axis('equal')
plt.title('Co-op Status Distribution')

plt.show()

#Making it show up on stream lit
st.pyplot(plt)



