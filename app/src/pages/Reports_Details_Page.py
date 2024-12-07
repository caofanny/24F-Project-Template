import streamlit as st
import requests

# Title
st.title('View Report')

# Ask the user to enter the Report ID
status_options = ["resolved", "pending"]
report_stat = st.selectbox('Select Status', status_options)

# Submit Button
if st.button('View Report'):
    try:
        # Fetch the report from the API
        response = requests.get(f"http://api:4000/r/reports/{report_stat}")

        if response.status_code == 200:
            report_data = response.json()

            if report_data:
                st.dataframe(report_data, use_container_width=True)
            else:
                st.write("No users found in the database.")

        else:
            st.write(f"Failed to fetch users. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.write(f"API Error: {str(e)}")


# Back Button to go back to the previous page
back = st.sidebar.button("Back")
if back:
    st.switch_page('pages/Reports_Page.py')
