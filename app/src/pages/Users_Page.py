import streamlit as st
import requests

# Title
st.title("User Management Dashboard")

# Sidebar Menu
menu_options = ["Create User", "Update User", "Delete User"]
choice = st.sidebar.radio("Select an option:", menu_options)

# Function to Create User Form
def create_user_form():
    st.sidebar.write("### Create New User Form")
    first_name = st.sidebar.text_input("First Name")
    last_name = st.sidebar.text_input("Last Name")
    email = st.sidebar.text_input("Email")
    submitted = st.sidebar.button("Submit")

    if submitted:
        if first_name and last_name and email:
            new_user = {
                "FirstName": first_name,
                "LastName": last_name,
                "Email": email
            }
            try:
                response = requests.post("http://api:4000/u/users", json=new_user)

                if response.status_code == 200:
                    st.sidebar.success("User successfully added to the database.")
                    st.query_params(refresh="true")
                else:
                    st.sidebar.warning(f"Failed to create user. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                st.sidebar.warning(f"API Error: {str(e)}")
        else:
            st.sidebar.warning("Please fill out all fields.")

# Function to Update User Form
def update_user_form():
    st.sidebar.write("### Update Existing User")
    user_id = st.sidebar.number_input("Enter User ID", min_value=1, step=1)
    first_name = st.sidebar.text_input("New First Name")
    last_name = st.sidebar.text_input("New Last Name")
    email = st.sidebar.text_input("New Email")
    submitted = st.sidebar.button("Update")

    if submitted:
        if user_id and first_name and last_name and email:
            updated_data = {
                "FirstName": first_name,
                "LastName": last_name,
                "Email": email
            }
            try:
                response = requests.put(f"http://api:4000/u/users/{int(user_id)}", json=updated_data)

                if response.status_code == 200:
                    st.sidebar.success("User successfully updated.")
                    st.query_params(refresh="true")
                else:
                    st.sidebar.warning(f"Failed to update user. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                st.sidebar.warning(f"API Error: {str(e)}")
        else: 
            st.sidebar.warning("Please fill out all fields.")

def delete_user_form(): 
    st.sidebar.write("### Delete Existing User")
    user_id = st.sidebar.number_input("Enter User ID", min_value=1, step=1)
    submitted = st.sidebar.button("Update")

    if submitted:
        if user_id:
            try:
                response = requests.delete(f"http://api:4000/u/users/{user_id}")
                if response.status_code == 200:
                    st.sidebar.success("User successfully deleted!")
                    st.query_params(refresh="true")
                else:
                    st.sidebar.error(f"Failed to delete user: {response.status_code}")
            except requests.exceptions.RequestException as e:
                    st.sidebar.warning(f"API Error: {str(e)}")
        else:
            st.sidebar.warning("Please fill out all fields.")

# Function to Display Users on the Main Page
def display_users():
    st.write("### All Users with Last Login Time")

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

# Show Sidebar Forms Based on Selection
if choice == "Create User":
    create_user_form()
elif choice == "Update User":
    update_user_form()
elif choice == "Update User":
    delete_user_form()

# Main Page - Display Users
display_users()
