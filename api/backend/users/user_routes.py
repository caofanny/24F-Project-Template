########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
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
users = Blueprint('users', __name__)


#------------------------------------------------------------
# Get all users from the system
@users.route('/users', methods=['GET'])
def get_users():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT u.UserID, u.FirstName, u.LastName, u.Email, 
                   FROM Users u
    ''')
    
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

    # Get a database cursor
    cursor = db.get_db().cursor()
        
    # Insert the new user into the database
    cursor.execute('''
        INSERT INTO Users (FirstName, LastName, Email)
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
    firstname = user_info.get('firstname')  # Key 'firstname' from JSON
    lastname = user_info.get('lastname')    # Key 'lastname' from JSON
    email = user_info.get('email')          # Key 'email' from JSON
    
    # Print or log the extracted values for debugging
    current_app.logger.info(f'Received data: firstname={firstname}, lastname={lastname}, email={email}')
    
    # Use the extracted data in your SQL query or application logic
    query = '''
        UPDATE Users
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
    query = "DELETE FROM Users WHERE UserID = %s"
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
    time_threshold = current_time - timedelta(minutes=30)

    cursor = db.get_db().cursor()

    # Query to select users who have logged in within the last 30 minutes
    query = """
    SELECT u.UserID, u.FirstName, u.LastName, u.Email, u.UserType, s.lastlogin
    FROM Users u
    LEFT JOIN student s ON u.UserID = s.UserID
    LEFT JOIN alumni a ON u.UserID = a.UserID
    LEFT JOIN advisor ad ON u.UserID = ad.UserID
    LEFT JOIN admin ad2 ON u.UserID = ad2.UserID
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
# Get customer detail for customer with particular userID
#   Notice the manner of constructing the query. 
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    current_app.logger.info('GET /customers/<userID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT id, first_name, last_name FROM customers WHERE id = {0}'.format(userID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Makes use of the very simple ML model in to predict a value
# and returns it to the user
@customers.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response