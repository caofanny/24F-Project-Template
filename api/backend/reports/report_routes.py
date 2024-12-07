from datetime import datetime
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
reports = Blueprint('reports', __name__)


#------------------------------------------------------------
# Return a list of reports
@reports.route('/reports', methods=['GET'])
def get_reports():

    cursor = db.get_db().cursor()
    query = '''
        SELECT r.ReportID, u.FirstName AS UserReported, a.FirstName AS AnsweredBy, 
               r.Reason, r.Status, r.ReportDate
        FROM Reports r
            LEFT JOIN User_Admin a ON r.AnsweredBy = a.AdminID
            LEFT JOIN User u ON r.UserReported = u.UserID
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a report
@reports.route('/reports', methods=['POST'])
def make_report():

    userReported = request.json.get('UserReported')  # UserID of the person reporting
    reason = request.json.get('Reason')          # Reason for the report
    status = "pending"
    report_date = datetime.now()                 # Date and time of the report (current time)

    # Insert the report into the Reports table
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Reports (UserReported, AnsweredBy, Status, Reason, ReportDate)
        VALUES (%s, NULL, %s, %s, %s)
    '''
    cursor.execute(query, (userReported, status, reason, report_date))
    db.get_db().commit()
    
    return 'report created!'

#------------------------------------------------------------
# Return the specific status report 
@reports.route('/reports/<stats>', methods=['GET'])
def get_specific_status(stats):

    cursor = db.get_db().cursor()
    
    # Query to fetch the specific report by report_id
    query = '''
        SELECT r.ReportID, u.FirstName AS UserReported, a.FirstName AS AnsweredBy, r.Reason, r.Status, r.ReportDate
        FROM Reports r
        JOIN User_Admin a ON r.AnsweredBy = a.AdminID
        JOIN User u ON r.UserReported = u.UserID
        WHERE r.Status = %s;
    '''
    cursor.execute(query, stats)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Update the status of the reports made
@reports.route('/reports/<report_id>', methods=['PUT'])
def answer_report(report_id):

    answered_by = request.json.get('AnsweredBy')  # Admin/user ID handling the report
    status = request.json.get('Status') 
    cursor = db.get_db().cursor()
    query = '''
        UPDATE Reports
        SET AnsweredBy = %s, Status = %s
        WHERE ReportID = %s
    '''

    cursor.execute(query, (answered_by, status, report_id))
    db.get_db().commit()

    return 'report answered!'

#------------------------------------------------------------
# Delete the report
@reports.route('/reports/<report_id>', methods=['DELETE'])
def delete_report(report_id):

    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM Reports
        WHERE ReportID = %s;
    '''
    cursor.execute(query, (report_id,))
    db.get_db().commit()
    
    return 'report deleted!'