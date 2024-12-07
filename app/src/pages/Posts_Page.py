import logging
import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

# Logger setup
logger = logging.getLogger(__name__)

# Sidebar Links
SideBarLinks()

# Title
st.title("Your Posts Dashboard")

# Hardcoded Alumnus ID for demonstration purposes
alumnus_id = 233  # Replace with dynamic ID from session or login

# Base URL for API requests
BASE_API_URL = "http://api:4000"  # Ensure this matches your Flask API URL

# Function to fetch posts for the given alumnus
def fetch_user_posts(alumnus_id):
    """Fetch all posts made by the specified alumnus."""
    try:
        # Filter posts by author using the `AuthorID` from the API
        response = requests.get(f"{BASE_API_URL}/p/posts")
        if response.status_code == 200:
            all_posts = response.json()
            # Filter posts for the specific author ID
            user_posts = [post for post in all_posts if post['AuthorID'] == alumnus_id]
            return pd.DataFrame(user_posts) if user_posts else None
        else:
            st.error(f"Failed to fetch posts: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"API Request failed: {str(e)}")
        return None

# Function to create a new post
def create_post_form():
    st.sidebar.write("### Create a New Post")
    title = st.sidebar.text_input("Post Title")
    slug = st.sidebar.text_input("Post Slug")
    content = st.sidebar.text_area("Post Content")
    published_at = st.sidebar.text_input("Publish Date (YYYY-MM-DD HH:MM:SS)", "")

    submitted = st.sidebar.button("Create Post")

    if submitted:
        if title and slug and content:
            new_post = {
                "AuthorID": alumnus_id,
                "Title": title,
                "Slug": slug,
                "Content": content,
                "PublishedAt": published_at if published_at else None,
            }
            try:
                response = requests.post(f"{BASE_API_URL}/p/posts", json=new_post)
                if response.status_code == 201:
                    st.sidebar.success("Post created successfully!")
                else:
                    st.sidebar.error(f"Failed to create post. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"API Error: {str(e)}")
        else:
            st.sidebar.warning("Please fill out all fields.")

# Function to delete a post
def delete_post_form():
    st.sidebar.write("### Delete a Post")
    post_id = st.sidebar.number_input("Enter Post ID to Delete", min_value=1, step=1)

    submitted = st.sidebar.button("Delete Post")

    if submitted:
        try:
            response = requests.delete(f"{BASE_API_URL}/p/posts/{int(post_id)}")
            if response.status_code == 200:
                st.sidebar.success("Post deleted successfully!")
            else:
                st.sidebar.error(f"Failed to delete post. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.sidebar.error(f"API Error: {str(e)}")

# Display User's Posts
def display_user_posts():
    st.write("### Your Posts")

    # Fetch posts
    posts_df = fetch_user_posts(alumnus_id)

    if posts_df is not None and not posts_df.empty:
        st.dataframe(posts_df, use_container_width=True)
    else:
        st.write("You have not made any posts yet.")

# Main Display Logic
create_post_form()  # Sidebar for creating a new post
delete_post_form()  # Sidebar for deleting a post
display_user_posts()  # Main content: Display all posts
