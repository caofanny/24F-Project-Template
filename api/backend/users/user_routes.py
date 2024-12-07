import datetime
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
users = Blueprint('users', __name__)


#------------------------------------------------------------
# Get all users and their last login from the system
@users.route('/users', methods=['GET'])
def get_users():

    cursor = db.get_db().cursor()
    # Join Users with Students, Alumni, and Advisors to get LastLogin for each user
    query = '''
        SELECT u.UserID, u.FirstName, u.LastName, u.Email,
            COALESCE(s.LastLogin, a.LastLogin, adv.LastLogin) AS LastLogin
        FROM User u
            LEFT JOIN Student s ON u.UserID = s.UserID
            LEFT JOIN Alumnus a ON u.UserID = a.UserID
            LEFT JOIN Advisor adv ON u.UserID = adv.UserID
    '''

    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a new user profile
@users.route('/users', methods=['POST'])
def create_users():

    # Parse JSON payload from the request
    user_data = request.get_json()
    
    # Extract user details
    first_name = user_data.get('FirstName')
    last_name = user_data.get('LastName')
    email = user_data.get('Email')

    if not first_name or not last_name or not email:
            return jsonify({"error": "Missing user data"}), 400
    
    # Get a database cursor
    cursor = db.get_db().cursor()
    
        
    # Insert the new user into the database
    cursor.execute('''
        INSERT INTO User (FirstName, LastName, Email)
        VALUES (%s, %s, %s)
    ''', (first_name, last_name, email))
        
    # Commit the transaction
    db.get_db().commit()
    return 'user made!'

#------------------------------------------------------------
# Update a user status or information
@users.route('/users/<uid>', methods=['PUT'])
def update_user(uid):
    # Log the request route
    current_app.logger.info(f'PUT /users/{uid} route')

    # Get JSON data from the request
    user_info = request.get_json()
    
    # Extract values from the JSON payload
    firstname = user_info.get('FirstName')  # Key 'firstname' from JSON
    lastname = user_info.get('LastName')    # Key 'lastname' from JSON
    email = user_info.get('Email')          # Key 'email' from JSON
    
    # Print or log the extracted values for debugging
    current_app.logger.info(f'Received data: firstname={firstname}, lastname={lastname}, email={email}')
    
    # Use the extracted data in your SQL query or application logic
    query = '''
        UPDATE User
        SET FirstName = %s, LastName = %s, Email = %s
        WHERE UserID = %s
    '''
    data = (firstname, lastname, email, uid)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    return 'user updated!'

#------------------------------------------------------------
# Delete a user 
@users.route('/users/<uid>', methods=['DELETE'])
def delete_user(uid):
    cursor = db.get_db().cursor()

    # Delete the user directly from the Users table
    query = "DELETE FROM User WHERE UserID = %s"
    cursor.execute(query, (uid,))
    db.get_db().commit()

    return 'user deleted!'

#------------------------------------------------------------
# Return a list of all users that logged on within the last 30 minutes 
@users.route('/users/performance', methods=['GET'])
def get_performance():
    # Get the current time
    current_time = datetime.now()

    # Calculate the time 30 minutes ago
    time_threshold = current_time - datetime.timedelta(minutes=30)

    cursor = db.get_db().cursor()

    # Query to select users who have logged in within the last 30 minutes
    query = """
        SELECT u.UserID, u.FirstName, u.LastName, u.Email
        FROM User u
            LEFT JOIN Student s ON u.UserID = s.UserID
            LEFT JOIN Alumnus a ON u.UserID = a.UserID
            LEFT JOIN Advisor ad ON u.UserID = ad.UserID
            LEFT JOIN User_Admin ad2 ON u.UserID = ad2.UserID
        WHERE (s.lastlogin >= %s OR a.lastlogin >= %s OR ad.lastlogin >= %s OR ad2.lastlogin >= %s)
        """

    # Execute the query with the time threshold
    cursor.execute(query, (time_threshold, time_threshold, time_threshold, time_threshold))

    # Fetch all the results
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get the user activity

# Route to get total active and inactive users with percentage
@users.route('/users/status', methods=['GET'])
def get_user_status():
    query = '''
        SELECT 
            IsActive,
            COUNT(*) AS TotalUsers,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM (
                SELECT UserID FROM Advisor 
                UNION ALL 
                SELECT UserID FROM Student 
                UNION ALL 
                SELECT UserID FROM Alumnus
            ) AS AllUsers)), 2) AS Percentage
        FROM (
            SELECT IsActive FROM Advisor
            UNION ALL
            SELECT IsActive FROM Student
            UNION ALL
            SELECT IsActive FROM Alumnus
        ) AS Combined
        GROUP BY IsActive;
        '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    results = cursor.fetchall()

    # Format the data for response
    active_inactive_data = {
        "Active": next((item for item in results if item['IsActive'] == 1), None),
        "Inactive": next((item for item in results if item['IsActive'] == 0), None)
    }

    return jsonify(active_inactive_data)

# didnt use
@users.route('/users/inactive', methods=['GET'])
def get_inactive_users():
    query = '''
        SELECT 
            UserID, FirstName, LastName, Email
        FROM Student
        WHERE IsActive = FALSE
        UNION
        SELECT UserID, FirstName,LastName, Email
        FROM Advisor
        WHERE IsActive = FALSE
        UNION
        SELECT UserID, FirstName,  LastName, Email 
        FROM Alumnus
        WHERE IsActive = FALSE;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    results = cursor.fetchall()
    return jsonify(results)


# Route to get total active and inactive students with percentage
@users.route('/users/students-status', methods=['GET'])
def get_student_status():
    query = '''
    SELECT 
        IsActive,
        COUNT(*) AS TotalStudents,
        ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Student)), 2) AS Percentage
    FROM Student
    GROUP BY IsActive;
'''

    cursor = db.get_db().cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    # Format the data for response
    active_inactive_data = {
        "Active": next((item for item in results if item['IsActive'] == 1), None),
        "Inactive": next((item for item in results if item['IsActive'] == 0), None)
    }
    return jsonify(active_inactive_data)

# didnt use (delete if you are using, otherwise we can delete this function before submitting)
@users.route('/users/students/inactive', methods=['GET'])
def get_inactive_students():
    cursor = db.get_db().cursor()

    query = '''
        SELECT 
            StudentID, 
            FirstName, 
            LastName, 
            Email, 
            LastLogin, 
            CoopStatus, 
            Year
        FROM Student
        WHERE IsActive = FALSE;
    '''
    cursor.execute(query)
    theData = cursor.fetchall()  

    return make_response(jsonify(theData), 200)

    
# Route to get total active and inactive alumni with percentage
@users.route('/users/alumni-status', methods=['GET'])
def get_alumni_status():
    query_alumni = '''
        SELECT 
            IsActive,
            COUNT(*) AS TotalAlumni,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Alumnus)), 2) AS Percentage
        FROM Alumnus
        GROUP BY IsActive;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query_alumni)

    results_alumni = cursor.fetchall()

    # Format the data for response
    active_inactive_alumni = {
        "Active": next((item for item in results_alumni if item['IsActive'] == 1), None),
        "Inactive": next((item for item in results_alumni if item['IsActive'] == 0), None)
    }
    return jsonify(active_inactive_alumni)

# Route to get total active and inactive advisors with percentage
@users.route('/users/advisors-status', methods=['GET'])
def get_advisor_status():
    query_advisors = '''
        SELECT 
            IsActive,
            COUNT(*) AS TotalAdvisors,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Advisor)), 2) AS Percentage
        FROM Advisor
        GROUP BY IsActive;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query_advisors)

    results_advisors = cursor.fetchall()

    # Format the data for response
    active_inactive_advisors = {
        "Active": next((item for item in results_advisors if item['IsActive'] == 1), None),
        "Inactive": next((item for item in results_advisors if item['IsActive'] == 0), None)
    }
    return jsonify(active_inactive_advisors)

#------------------------------------------------------------
# Returns a list of students and their data
@users.route('/users/students', methods=['GET'])
def get_students():
    cursor = db.get_db().cursor()

    query = '''
        SELECT FirstName, LastName, Email, Major, Year
        FROM Student;
    '''

    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Returns a list of alumni and their data
@users.route('/users/alumni', methods=['GET'])
def get_alumni():
    cursor = db.get_db().cursor()

    query = '''
        SELECT FirstName, LastName, Email, College, Major, CurrentCompany 
        FROM Alumnus;
    '''

    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
#------------------------------------------------------------
# get list of student connect with alumnus
@users.route('/users/alumnus/<alumnus_id>/students', methods=['GET'])
def get_connected_students(alumnus_id):
    cursor = db.get_db().cursor()
    query = '''
        SELECT s.StudentID, s.FirstName, s.LastName, s.Email, s.Major, s.Year
        FROM Alumni_Mentors am
        JOIN Student s ON am.StudentID = s.StudentID
        WHERE am.AlumnusID = %s;
    '''
    cursor.execute(query, (alumnus_id,))
    students = cursor.fetchall()
    return make_response(jsonify(students), 200)

@users.route('/u/users/alumnus/<mentor_id>/students', methods=['POST'])
def add_student_connection(mentor_id):
    """Add a student connection to the specified alumnus."""
    # Your logic here, e.g., retrieving data from the request and updating the database.
    request_data = request.get_json()
    student_id = request_data.get('StudentID')
    
    if not student_id:
        return jsonify({"error": "StudentID is required"}), 400
    
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Alumni_Mentors (StudentID, AlumnusID)
        VALUES (%s, %s)
    '''
    try:
        cursor.execute(query, (student_id, mentor_id))
        db.get_db().commit()
        return jsonify({"message": "Connection added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Returns this alumn's data and experience
@users.route('/users/alumni/major', methods=['GET'])
def get_alumni_major():
    cursor = db.get_db().cursor()

    query = '''
        SELECT FirstName, LastName, Email, College, Major, Num_Coops, CurrentCompany, CurrentPosition
        FROM Alumnus
        WHERE UserID = 85;
    '''

    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Returns this alumn's data and experience
@users.route('/users/alumni/filter/major', methods=['GET'])
def get_alumni_filter_major():
    cursor = db.get_db().cursor()

    query = '''
        SELECT FirstName, LastName, Email, CurrentCompany, CurrentPosition
        FROM Alumnus
        WHERE Major = 'Biology'
        AND UserID != 85;
    '''

    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Returns this alumn's data and experience
@users.route('/users/alumni/filter/job', methods=['GET'])
def get_alumni_filter_job():
    cursor = db.get_db().cursor()

    query = '''
        SELECT FirstName, LastName, Email, CurrentCompany, CurrentPosition
        FROM Alumnus
        WHERE CurrentCompany = 'Acme Corporation'
        AND UserID != 85;
    '''

    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response



#------------------------------------------------------------
# Return a list of all students who took the specific course
@users.route('/users/students/<course_name>', methods=['GET'])
def get_students_courses(course_name):
    cursor = db.get_db().cursor()

    query = '''
        SELECT u.FirstName, u.LastName, u.Email 
        FROM USER u
	        JOIN Courses_Taken ct ON ct.UserID = u.UserID
	        JOIN Courses c ON ct.CourseID = c.CourseID
        WHERE c.Name = %s;
    '''
    data = (course_name,)
    cursor.execute(query, data)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Return a list of all students who worked at a specific company
@users.route('/users/students/<company_name>', methods=['GET'])
def get_students_company(company_name):
    cursor = db.get_db().cursor()

    query = '''
        SELECT u.FirstName, u.LastName, u.Email 
        FROM USER u
	        JOIN Company_Worked cw ON cw.UserID = u.UserID
	        JOIN Company c ON c.CompanyID = cw.CompanyId
        WHERE c.Name = %s;
    '''
    data = (company_name,)
    cursor.execute(query, data)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Returns a list of students and their coop status
@users.route('/users/advisor/students/', methods=['GET'])
def get_students_coop():
    cursor = db.get_db().cursor()

    query = '''
        SELECT FirstName, LastName, Email, Major, Year, CoopStatus, AdvisorID, StudentID
        FROM Student;
    '''
    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#--------------------------------------------------------------
#Returns a list of courses a student took
@users.route('/users/students/courses/<studentid>', methods=['GET'])
def get_courses(studentid):
    cursor = db.getdb().cursor()
    
    # The SQL query with placeholder for studentid
    query = '''
    SELECT Courses.CoursesID, Courses.Name, Courses.Professor, Courses.Description
    FROM User
    JOIN Student ON User.UserID = Student.UserID
    JOIN Courses_Taken ON Student.UserID = Courses_Taken.UserID
    JOIN Courses ON Courses_Taken.CoursesID = Courses.CoursesID
    WHERE Student.StudentID = %s;
    '''
    
    # Execute the query, passing studentid as the parameter
    cursor.execute(query, (studentid,))
    
    # Fetch all results
    theData = cursor.fetchall()
    
    # Create the response
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response



#------------------------------------------------------------
# Returns the coop placement rate for students
@users.route('/users/advisor/students/coop', methods=['GET'])
def get_students_coop_rate():
    cursor = db.get_db().cursor()

    query = '''
        SELECT 
            COALESCE(COUNT(*), 0) AS total_students,
            COALESCE(SUM(CASE WHEN CoopStatus = 'Found Co-op' THEN 1 ELSE 0 END), 0) AS students_with_coop,
            COALESCE(SUM(CASE WHEN CoopStatus = 'Searching' THEN 1 ELSE 0 END), 0) AS students_still_searching,
            CASE 
                WHEN COUNT(*) = 0 THEN 0
                ELSE ROUND(SUM(CASE WHEN CoopStatus = 'Found Co-op' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)
            END AS coop_percentage
        FROM Student;

    '''
    cursor.execute(query)
    theData = cursor.fetchone()  # Single row with aggregated results

    # Map results into a dictionary
    # result = {
    #     "total_students": theData[0],
    #     "students_with_coop": theData[1],
    #     "students_still_searching": theData[2],
    #     "coop_percentage": theData[3]
    # }

    # Return the JSON response
    response = make_response(jsonify(theData), 200)
    return response

