import streamlit as st
import requests

# Define the base URL for Flask API

# Title
st.title('Report Management System')
back = st.sidebar.button("Back")

def get_report():
    st.write("### Report")

    try:
        response = requests.get("http://api:4000/u/users")
        if response.status_code == 200:
            users_data = response.json()

            if users_data:
                st.dataframe(users_data, use_container_width=True)
            else:
                st.write("No users found in the database.")

        else:
            st.write(f"Failed to fetch users. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.write(f"API Error: {str(e)}")


if back:
    st.switch_page('pages/2_System_Administrator_Home.py')

