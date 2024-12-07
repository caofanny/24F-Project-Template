import streamlit as st
import requests

# Set the title of the page
st.set_page_config(page_title="User Dashboard", layout="wide")

back = st.sidebar.button("Back")
st.title('📊 User Activity Dashboard')

# Define a function to make API calls and get JSON responses
def get_api_data(endpoint):
    try:
        response = requests.get(f'http://api:4000/u/{endpoint}')
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data from {endpoint}")
            return {}
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
        return {}

# Function to display data in a neat card style
def display_data(category_name, data):
    st.subheader(category_name)
    getUser = "TotalUsers"
    if category_name == "Student Statistics":
        getUser = "TotalStudents"
    elif category_name == "Alumni Statistics":
        getUser = "TotalAlumni"
    if category_name == "Advisor Statistics":
        getUser = "TotalAdvisors"

    if data:
        active_data = data.get('Active', {}).get(getUser, 0)
        inactive_data = data.get('Inactive', {}).get(getUser, 0)
        percentage_active = data.get('Active', {}).get(getUser, 0)

        col1, col2, col3 = st.columns(3)

        col1.metric("Active Users", active_data)
        col2.metric("Inactive Users", inactive_data)
        col3.metric("Active Percentage", f"{percentage_active}%")
    else:
        st.write("No data available.")

# Get data for all statistics
user_data = get_api_data('/users/status')
student_data = get_api_data('/users/students-status')
alumni_data = get_api_data('/users/alumni-status')
advisor_data = get_api_data('/users/advisors-status')

st.write("---")
display_data('User Statistics', user_data)
st.write("---")
display_data('Student Statistics', student_data)
st.write("---")
display_data('Alumni Statistics', alumni_data)
st.write("---")
display_data('Advisor Statistics', advisor_data)

if back:
    st.switch_page('pages/2_System_Administrator_Home.py')
