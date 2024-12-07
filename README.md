# UConnect Project Repository
# demo video
- https://drive.google.com/file/d/1wKy24YTIGBlPo1hynJ6PyZr_KhUubvE1/view?usp=sharing

## env file setup
Choose a strong password and replace <somepassword>

SECRET_KEY=<somepassword>
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=uconnect
MYSQL_ROOT_PASSWORD=<somepassword>

## Running the Project

- `docker compose up -d` to start all the containers in the background
- `docker compose down` to shutdown and delete the containers
- `docker compose up db -d` only start the database container (replace db with the other services as needed)
- `docker compose stop` to "turn off" the containers but not delete them.

## Current Project Components

Currently, there are three major components which will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST api in the `./api` directory
- SQL files for your data model and data base in the `./database-files` directory

# Project description

U-Connect is a data-driven, student-centric networking platform that empowers students by providing direct access to peer-generated insights and experiences. Through detailed profiles showcasing academic courses, co-op placements, and study-abroad opportunities, students can easily connect with others who have faced similar academic and professional challenges. This platform collects and analyzes real student data, helping users make informed decisions about courses, co-ops, and career paths.
By addressing key pain points—such as the lack of a centralized space for course feedback and co-op insights—U-Connect allows students to search for peers based on shared experiences and access real, peer-generated outcomes. With features like personalized recommendations, instant connections for specific needs, and up-to-date course feedback, students can confidently navigate their academic paths, build networks, and set realistic expectations for their futures. U-Connect is built for undergraduates, co-op advisors, and administrators who need to connect, share, and make data-driven decisions.

# Uconnect users

There are currently 4 users on Uconnect, a student, an alumnus, an advisor, and a system administrator

## Student

A student is someone currently taking classes at Northeastern and looking for more guidance about their education. 
To best help them on their journey they have access to many functions.

- They can view the course catelog 
- They can connect with alumni
- They can make a report

### Course Catelog
- They can view all courses offered without restriction to get a clearer picture of their options
- They can see the average rating of the class
- They can read a description of the class

### Alumni List
- They can see a list of all mentors
  - They can also view their current place and position of employment
  - They can see what they used to major in to get a sense of the career trajectory

### Submitting a Report
- They can submit a report to the system admins if any negative behavior is occurring on the site
 - They can specifiy the users id who they are having an issue with
 - They can also provide a description of the issue
- This better fosters a sense of uplifiting community on U-Connect

## Alumnus

An alumni is a user that has graduated from Northeastern and is currently employeed post-graudation, they also have access to many features.

- They have access to posts to provide tips for undergraduate students
- They have access to their own user profile
- They can also review specific courses offered to give their thoughts 

### Posts
- They can view all current posts to U-connect
  - They can create, update, and delete posts under their username

### User Profile
- They can see their information that is visible to other users on the platform
  - Such as name, email, college, major, number of co-ops, and their current position at their company
- They can also see infomation about other alumnis with similiar characteristics to allow for more connections

### Course Reviews
- They can view a list of all courses offered then write a post about their experience
  - Reviews allow them to give a rating out of five on the courses they took to provide more context for others using the site

## Advisor

An advisor oversees their students and can view data on their current statueses along with some other features.

- They can view which students they have been assigned
- They can view their students co-op status
- They can submit a report

### Viewing Assigned Students
- They can view which students they have been assigned
  - They can see their contact information
  - They can also can see the courses they are enrolled in
### Overview of Students Co-op Status
- They can see a comprehensive list of all their students process in the co-op search
  - Whether or not the student has secured a co-op, still searching, or is not currently searching
### Submitting a Report
- They can submit a report to the system admins if any negative behavior is occurring on the site
 - They can specifiy the users id who they are having an issue with
 - They can also provide a description of the issue
- This better fosters a sense of uplifiting community on U-Connect

## System Administrator

A system administrator oversees the entire application and has access to many functinalities.

- Managing the users
- Viewing the user activity percentage
- Reviewing user reports

#### Managing the users

- They are able view all the users and the login time
- They are able to
  - create a new user,
  - update user details
  - and delete users

#### Viewing the user activity percentage

- They are able to see the latest updated stats, such as
  - Active and Inactive users
  - Active and Inactive students
  - Active and Inactive alumni
  - Active and Inactive advisorrs

#### Reviewing user reports

- They are able to see all of the user reports including who reported, who responded, and its status.
- They are able to update an existing report.
- They are also able to delete an existing report
