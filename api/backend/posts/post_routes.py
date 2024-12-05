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
posts = Blueprint('post', __name__)


#------------------------------------------------------------
# Return a list of post
@posts.route('/post', methods=['GET'])
def get_post():

    cursor = db.get_db().cursor()
    query = '''
       SELECT p.PostID, u.FirstName AS AuthorFirstName, u.LastName AS AuthorLastName, 
               p.Title, p.Slug, p.Content, p.CreatedAt, p.UpdatedAt, p.PublishedAt
        FROM Post p
        JOIN User u ON p.AuthorID = u.UserID
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a post
@posts.route('/post', methods=['POST'])
def make_post():

    data = request.json
    author_id = data.get('AuthorID')
    title = data.get('Title')
    slug = data.get('Slug')
    content = data.get('Content')
    published_at = data.get('PublishedAt')

    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Post (AuthorID, Title, Slug, Content, PublishedAt)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (author_id, title, slug, content, published_at))
    db.get_db().commit()

    return make_response(jsonify({"message": "Post created successfully"}), 201)



#------------------------------------------------------------
# Update the status of the reports made
@reports.route('/post/{post-id}', methods=['PUT'])
def answer_report(post_id):

    data = request.json
    title = data.get('Title')
    slug = data.get('Slug')
    content = data.get('Content')
    published_at = data.get('PublishedAt')

    cursor = db.get_db().cursor()
    query = '''
        UPDATE Post
        SET Title = %s, Slug = %s, Content = %s, PublishedAt = %s, UpdatedAt = CURRENT_TIMESTAMP
        WHERE PostID = %s
    '''
    cursor.execute(query, (title, slug, content, published_at, post_id))
    db.get_db().commit()

    if cursor.rowcount > 0:
        return make_response(jsonify({"message": "Post updated successfully"}), 200)
    else:
        return make_response(jsonify({"error": "Post not found"}), 404)

#------------------------------------------------------------
# Delete the post
@posts.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM Post
        WHERE PostID = %s
    '''
    cursor.execute(query, (post_id,))
    db.get_db().commit()

    
    return 'report created!'
    