import streamlit as st
import requests

# Define the base URL for Flask API

# Title
st.title('Report Management System')
back = st.sidebar.button("Back")
report_id = st.sidebar.button("View Report Details")

# Sidebar options
menu_options = ["Update Report", "Delete Report"]
choice = st.sidebar.radio("Actions", menu_options)

# Function to display a list of existing reports
def display_reports():
    try:
        response = requests.get("http://api:4000/r/reports")
        if response.status_code == 200:
            reports = response.json()
            if reports:
                st.dataframe(reports, use_container_width=True)
            else:
                st.write("No reports found.")
        else:
            st.write(f"Failed to fetch reports. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.write(f"API Error: {str(e)}")

def update_report():
    st.sidebar.write("### Update Existing Report")
    report_id = st.sidebar.number_input('Enter Report ID to Update', min_value=1, step=1)
    answered_by = st.sidebar.text_input('Answered By')
    status_options = ["resolved", "pending"]
    new_status = st.sidebar.selectbox('Update Status', status_options)
    submitted = st.sidebar.button("Update")

    if submitted:
        if report_id and answered_by and new_status:
            updated_data = {
                "AnsweredBy": answered_by,
                "Status": new_status
            }
            try:
                response = requests.put(f"http://api:4000/r/reports/{report_id}", json=updated_data)

                if response.status_code == 200:
                    st.sidebar.success("Report successfully updated.")
                else:
                    st.sidebar.warning(f"Failed to update report. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                st.sidebar.warning(f"API Error: {str(e)}")
        else: 
            st.sidebar.warning("Please fill out all fields.")

def delete_report(): 
    st.sidebar.write("### Delete Existing Report")
    report_id = st.sidebar.number_input("Enter Report ID", min_value=1, step=1)
    submitted = st.sidebar.button("Update")

    if submitted:
        if report_id:
            try:
                response = requests.delete(f"http://api:4000/r/reports/{report_id}")
                if response.status_code == 200:
                    st.sidebar.success("Report successfully deleted!")
                else:
                    st.sidebar.error(f"Failed to delete report: {response.status_code}")
            except requests.exceptions.RequestException as e:
                    st.sidebar.warning(f"API Error: {str(e)}")
        else:
            st.sidebar.warning("Please fill out all fields.")

# Show Sidebar Forms Based on Selection
if choice == "Update Report":
    update_report()
elif choice == "Delete Report":
    delete_report()

if back:
    st.switch_page('pages/2_System_Administrator_Home.py')
if report_id:
    st.switch_page('pages/Reports_Details_Page.py')

# Main Page - Display Users
display_reports()
