import streamlit as st
import requests

# Set the title of the page
st.set_page_config(page_title="User Dashboard", layout="wide")

st.title('📊 My Experience Dashboard')
back = st.sidebar.button("Back")

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
    header_cols = st.columns([1, 1, 1, 1])  # Adjust column widths as needed
    with header_cols[0]:
        st.write("**Name:**")
    with header_cols[1]:
        st.write("**Email:**")
    with header_cols[2]:
        st.write("**Current Company:**")
    with header_cols[3]:
        st.write("**Current Position:**")

    # Iterate through the student data and display each student in a row with a delete button
    for user in data:
        row_cols = st.columns([1, 1, 1, 1])  # Same column width for each row
        
        with row_cols[0]:
            st.write(f"{user['FirstName']} {user['LastName']}")
        with row_cols[1]:
            st.write(f"{user['Email']}")
        with row_cols[2]:
            st.write(f"{user['CurrentPosition']}")
        with row_cols[3]:
            st.write(f"{user['CurrentCompany']}")
          
    st.write("---")

# Get data for all statistics
user_data = get_api_data('/users/alumni/major')
alumni_filter_major = get_api_data('/users/alumni/filter/major')
alumni_filter_job = get_api_data('/users/alumni/filter/job')

st.write("---")
if user_data:
    st.write("### My Information")

    for user in user_data:
        cols = st.columns(2)
        with cols[0]:
            st.write("**Name:**")
            st.write("**Email:**")
            st.write("**College:**")
            st.write("**Major:**")
            st.write("**Num Co-ops:**")
            st.write("**Current Company:**")
            st.write("**Current Position:**")
        with cols[1]:
            st.write(f"{user['FirstName']} {user['LastName']}")
            st.write(f"{user['Email']}")
            st.write(f"{user['College']}")
            st.write(f"{user['Major']}")
            st.write(f"{user['Num_Coops']}")
           
            st.write(f"{user['CurrentPosition']}")           
            st.write(f"{user['CurrentCompany']}")

        st.markdown("---")  # Separator between entries
else:
    st.write("No data available.")
#filter by same major
display_data("Alumni with the same major", alumni_filter_major)

#filter by same job
display_data("Alumni at the same company", alumni_filter_job)

if back:
    st.switch_page('pages/3_Mentor_Home.py')
