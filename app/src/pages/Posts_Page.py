import logging
import streamlit as st
import requests

from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# Title
st.title("Post Dashboard")

# Sidebar Menu
menu_options = ["Create Post", "Update Post", "Delete Post"]
choice = st.sidebar.radio("Select an option:", menu_options)
back = st.sidebar.button("Back")

# Function to Display Posts on the Main Page
def display_posts():
    st.write("### All Posts")
    try:
        response = requests.get("http://api:4000/p/posts")
        if response.status_code == 200:
            posts_data = response.json()

            if posts_data:
                st.dataframe(posts_data, use_container_width=True)
            else:
                st.write("No posts found in the database.")

        else:
            st.error(f"Failed to fetch posts. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")

# Function to Create Post Form
def create_post_form():
    st.sidebar.write("### Create New Post Form")
    author_id = st.sidebar.text_input("Enter your ID")
    title = st.sidebar.text_input("Title")
    slug = st.sidebar.text_input("Slug")
    content = st.sidebar.text_area("Content")
    submitted = st.sidebar.button("Submit")

    if submitted:
        if title and content and slug and author_id:
            new_post = {
                "AuthorID": author_id,
                "Slug": slug,
                "Title": title,
                "Content": content
            }
            try:
                response = requests.post("http://api:4000/p/posts", json=new_post)

                if response.status_code == 201:  # Assuming 201 for successful creation
                    st.sidebar.success("Post successfully added to the database.")
                else:
                    st.sidebar.error(f"Failed to create post. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"API Error: {str(e)}")
        else:
            st.sidebar.warning("Please fill out all fields.")

# Function to Update Post Form
def update_post_form():
    st.sidebar.write("### Update Existing Post")
    post_id = st.sidebar.number_input("Enter Post ID", min_value=1, step=1)
    title = st.sidebar.text_input("New Title")
    slug = st.sidebar.text_input("New Slug")
    content = st.sidebar.text_area("New Content")
    submitted = st.sidebar.button("Update")

    if submitted:
        if post_id and title and content and slug:
            updated_data = {
                "Title": title,
                "Content": content,
                "Slug": slug
            }
            try:
                response = requests.put(f"http://api:4000/p/posts/{int(post_id)}", json=updated_data)

                if response.status_code == 200:
                    st.sidebar.success("Post successfully updated.")
                else:
                    st.sidebar.error(f"Failed to update post. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"API Error: {str(e)}")
        else: 
            st.sidebar.warning("Please fill out all fields.")

# Function to Delete Post Form
def delete_post_form(): 
    st.sidebar.write("### Delete Existing Post")
    post_id = st.sidebar.number_input("Enter Post ID", min_value=1, step=1)
    submitted = st.sidebar.button("Delete")

    if submitted:
        if post_id:
            try:
                response = requests.delete(f"http://api:4000/p/posts/{post_id}")
                if response.status_code == 200:
                    st.sidebar.success("Post successfully deleted!")
                else:
                    st.sidebar.error(f"Failed to delete post. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"API Error: {str(e)}")
        else:
            st.sidebar.warning("Please fill out all fields.")

# Show Sidebar Forms Based on Selection
if choice == "Create Post":
    create_post_form()
elif choice == "Update Post":
    update_post_form()
elif choice == "Delete Post":
    delete_post_form()

if back:
    st.switch_page('pages/3_Mentor_Home.py')

# Main Page - Display Posts
display_posts()
