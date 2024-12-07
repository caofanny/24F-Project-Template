import streamlit as st
import requests

# Title
st.title("Review Management Dashboard")

# Sidebar Menu
menu_options = ["Create Review", "Update Review", "Delete Review"]
choice = st.sidebar.radio("Select an option:", menu_options)
back = st.sidebar.button("Back")

# Function to Display Users on the Main Page
def display_reviews():
    st.write("### All Reviews")

    try:
        response = requests.get("http://api:4000/c/courses/review")
        if response.status_code == 200:
            review_data = response.json()

            if review_data:
                st.dataframe(review_data, use_container_width=True)
            else:
                st.write("No reviews found in the database.")

        else:
            st.write(f"Failed to fetch review. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.write(f"API Error: {str(e)}")

# Function to Create Review Form
def create_review_form():
    st.sidebar.write("### Add a New Review")
    author_id = st.sidebar.text_input("Your ID")
    username = st.sidebar.text_input("Your username")
    title = st.sidebar.text_input("Title")
    rating = st.sidebar.slider("Rating (1-5)", min_value=1, max_value=5, step=1)
    comment = st.sidebar.text_area("Comment")
    submitted = st.sidebar.button("Submit")

    if submitted:
        if rating and author_id and usernamea and comment:
            new_review = {
                "Name": username,
                "AuthorID": author_id,
                "Title": title,
                "Rating": rating,
                "Comment": comment
            }
            try:
                response = requests.post(f"http://api:4000/c/courses/review/", json=new_review)

                if response.status_code == 201:  # Assuming 201 for successful creation
                    st.sidebar.success("Review successfully added to the course.")
                else:
                    st.sidebar.error(f"Failed to create review. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"API Error: {str(e)}")
        else:
            st.sidebar.warning("Please fill out all fields.")

# Function to Update Review Form
def update_review_form():
    st.sidebar.write("### Update Existing Review")
    title = st.sidebar.text_input("Title")
    review_id = st.sidebar.number_input("Review ID", min_value=1, step=1)
    rating = st.sidebar.slider("New Rating (1-5)", min_value=1, max_value=5, step=1)
    comment = st.sidebar.text_area("New Comment")
    submitted = st.sidebar.button("Update")

    if submitted:
        if review_id and title and comment:
            updated_data = {
                "Title": title,
                "Rating": rating,
                "Comment": comment
            }
            try:
                response = requests.put(f"http://api:4000/c/courses/review/{review_id}", json=updated_data)

                if response.status_code == 200:
                    st.sidebar.success("Review successfully updated.")
                else:
                    st.sidebar.error(f"Failed to update review. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"API Error: {str(e)}")
        else: 
            st.sidebar.warning("Please fill out all fields.")

# Function to Delete Review Form
def delete_review_form(): 
    st.sidebar.write("### Delete Existing Review")
    review_id = st.sidebar.number_input("Review ID", min_value=1, step=1)
    submitted = st.sidebar.button("Delete")

    if submitted:
        if review_id:
            try:
                response = requests.delete(f"http://api:4000/c/courses/review/{review_id}")
                if response.status_code == 200:
                    st.sidebar.success("Review successfully deleted!")
                else:
                    st.sidebar.error(f"Failed to delete review. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"API Error: {str(e)}")
        else:
            st.sidebar.warning("Please fill out all fields.")

# Show Sidebar Forms Based on Selection
if choice == "Create Review":
    create_review_form()
elif choice == "Update Review":
    update_review_form()
elif choice == "Delete Review":
    delete_review_form()

display_reviews()

if back:
    st.switch_page('pages/Review_Courses_Page.py')  # Replace with actual page name
