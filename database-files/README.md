# `database-files` Folder

In order to view our presentation video: https://drive.google.com/file/d/1ghYJkm4rAB-ELgSBYD5wMHzwxi2A8Ac1/view?usp=drive_link

## Setup

To reconnect a changed database:

- docker compose down db
- docker compose up db -d

To remove and reconnect all the containers:

- docker compose down
- docker compose up

## Uconnect data

- **Strong entities**:

  User, Student, Advisor, Alumnus, Admin, Reports, Course, Review, Company, Company_Recruiter, Position, Post

- **Weak entity**:
  Post_comment

- **Bridge tables** :positions_offered, recruiters_List, company_worked, Alumni_mentors, post_made, course_taken, reports_made, reviews_made, to_manage, comments_made

### All mock data was made using Mockaroo
