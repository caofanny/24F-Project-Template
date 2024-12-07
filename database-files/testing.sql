#-- SQL QUERY TO FIND WHICH COURSES A STUDENT IS TAKING
use uconnect;

SELECT Courses.CoursesID, Courses.Name, Courses.Professor, Courses.Description
FROM User JOIN Student ON
    User.UserID = Student.UserID
JOIN Courses_Taken ON
    Student.UserID = Courses_Taken.UserID
JOIN Courses ON
    Courses_Taken.CoursesID = Courses.CoursesID
WHERE studentID = 2;