# UConnect Project Repository
# video
- https://drive.google.com/file/d/1ghYJkm4rAB-ELgSBYD5wMHzwxi2A8Ac1/view?usp=drive_link 
## env file setup

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

- A student can have access to their informations such as:
  - viewing available alumni mentors
  - viewing courses
  - and also reporting errors or anything that violates the guideline

## Alumnus

- An alumnus has access to many features, for example
  - They can view their profile and also get a list of other alumns that either had the same major or work at the same company.
  - They can also make posts with tips for undergraduate students.
  - They can also add a connection with undergrad students to mentor them personally.

## Advisor

- The advisor has access to their assigned students.
- They also have access to statistics of whether they found a co-op or not
- And they can report a student to the system administrators

## System Administrator

The system administrator oversees the entire applications and has access to many functinalities.

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
