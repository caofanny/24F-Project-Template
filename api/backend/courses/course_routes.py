########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
import datetime
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
courses = Blueprint('courses', __name__)


#------------------------------------------------------------
# Return a list of courses
@courses.route('/course', methods=['GET'])
def get_courses():

    cursor = db.get_db().cursor()
    query = '''
        SELECT * FROM Courses
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Return a list of courses students have completed
@courses.route('/course/completed', methods=['GET'])
def get_courses_from_student():

    cursor = db.get_db().cursor()
    query = '''
        SELECT s.StudentID, s.FirstName, s.LastName, s.Email, s.Major, c.Name AS CourseName 
        FROM Student s 
            JOIN Courses_Taken ct ON s.UserID = ct.UserID 
            JOIN Courses c ON ct.CoursesID = c.CoursesID 
        ORDER BY s.StudentID, c.Name;
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Return all reviews for a specific course
@courses.route('/courses/<couse-name>/review/', methods=['GET'])
def get_course_reviews(course_name):

    cursor = db.get_db().cursor()
    query = '''
        SELECT r.Title AS Review_Title, r.Rating, r.Content
        FROM Reviews_Made rm 
            JOIN Review r ON rm.ReviewID = r.ReviewID 
            JOIN Courses c ON rm.CoursesID = c.CoursesID 
        WHERE c.Name = %s
        ORDER BY r.Rating DESC;

    '''
    cursor.execute(query, course_name)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a new review for the specific course
@courses.route('/courses/<couse-name>/review/', methods=['POST'])
def get_course_reviews(course_name):

    cursor = db.get_db().cursor()
    query = '''
        SELECT r.Title AS Review_Title, r.Rating, r.Content
        FROM Reviews_Made rm 
            JOIN Review r ON rm.ReviewID = r.ReviewID 
            JOIN Courses c ON rm.CoursesID = c.CoursesID 
        WHERE c.Name = %s
        ORDER BY r.Rating DESC;

    '''
    cursor.execute(query, course_name)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Update a review for a specific course
@courses.route('/courses/<couse-name>/review/<review-id>', methods=['PUT'])
def make_report():

    reported_by = request.json.get('ReportedBy')  # UserID of the person reporting
    reason = request.json.get('Reason')          # Reason for the report
    status = request.json.get('Status')          # Status of the report
    report_date = datetime.now()                 # Date and time of the report (current time)

    # Insert the report into the Reports table
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Reports (UserReported, AnsweredBy, Status, Reason, ReportDate)
        VALUES (%s, NULL, %s, %s, %s)
    '''
    cursor.execute(query, (reported_by, status, reason, report_date))
    db.get_db().commit()
    
    return 'report created!'

#------------------------------------------------------------
# Delete the report
@reports.route('/courses/<couse-name>/review/<review-id>', methods=['DELETE'])
def delete_report(report_id):

    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM Reports
        WHERE ReportID = %s;
    '''
    cursor.execute(query, (report_id,))
    db.get_db().commit()
    
    return 'report deleted!'