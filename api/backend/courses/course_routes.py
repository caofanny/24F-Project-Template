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
        SELECT r.Name AS Username, r.Title AS Review_Title, r.Rating, r.Content
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
def add_course_reviews(course_name):

    data = request.get_json()
    name = data.get('name')
    author_id = data.get('AuthorID')
    title = data.get('Title')   
    rating = data.get('Rating')  
    content = data.get('Content')  

    cursor = db.get_db().cursor()

    review_query = '''
        INSERT INTO Review (Name, AuthorID, Title, Rating, Content)
        VALUES (%s, %s, %s, %s, %s)
    '''

    cursor.execute(review_query, (name, author_id, title, rating, content))
    db.get_db().commit()
    return 'review created!'

#------------------------------------------------------------
# Update a review for a course
@courses.route('/courses/review/<review-id>', methods=['PUT'])
def update_course_review(review_id):

    current_app.logger.info(f'PUT /courses/review/{review_id} route')

    data = request.get_json()
    title = data.get('Title')
    rating = data.get('Rating')
    content = data.get('Content')

    current_app.logger.info(f'Received data: title={title}, 
                            rating={rating}, content={content}')
    
    cursor = db.get_db().cursor()
    query = '''
        UPDATE Review
        SET Title = %s, Rating = %s, Content = %s
        WHERE ReviewID = %s
    '''
    cursor.execute(query, (title, rating, content, review_id))
    db.get_db().commit()
    
    return 'review updated!'

#------------------------------------------------------------
# Delete the review
@courses.route('/courses/review/<review-id>', methods=['DELETE'])
def delete_report(review_id):

    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM Review
        WHERE ReviewID = %s;
    '''
    cursor.execute(query, (review_id,))
    db.get_db().commit()
    
    return 'review deleted!'