from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
posts = Blueprint('posts', __name__)


#------------------------------------------------------------
# Return a list of post
@posts.route('/posts', methods=['GET'])
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
@posts.route('/posts', methods=['POST'])
def make_post():

    data = request.get_json()
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
@posts.route('/posts/<post_id>', methods=['PUT'])
def answer_report(post_id):
    current_app.logger.info(f'PUT /posts/{post_id} route')

    data = request.get_json()
    title = data.get('Title')
    slug = data.get('Slug')
    content = data.get('Content')
    published_at = data.get('PublishedAt')

    current_app.logger.info(f'Received data: title={title}, slug={slug}, content={content}, publishedat={published_at}')
    
    query = '''
        UPDATE Post
        SET Title = %s, Slug = %s, Content = %s, PublishedAt = %s, UpdatedAt = CURRENT_TIMESTAMP
        WHERE PostID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (title, slug, content, published_at, post_id))
    db.get_db().commit()

    if cursor.rowcount > 0:
        return make_response(jsonify({"message": "Post updated successfully"}), 200)
    else:
        return make_response(jsonify({"error": "Post not found"}), 404)

#------------------------------------------------------------
# Delete the post
@posts.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM Post
        WHERE PostID = %s
    '''
    cursor.execute(query, (post_id,))
    db.get_db().commit()

    
    return 'report deleted!'

#------------------------------------------------------------
# Get all comments for a specific post
@posts.route('/posts/<post_id>/comments', methods=['GET'])
def get_comments_for_post(post_id):

    cursor = db.get_db().cursor()
    query = '''
        SELECT c.CommentID, c.AuthorID, u.FirstName AS AuthorFirstName, u.LastName AS AuthorLastName,
            c.Content, c.PublishedAt, c.CreatedAt
        FROM Post_Comment c
        JOIN User u ON c.AuthorID = u.UserID
        WHERE c.PostID = %s
    '''
    cursor.execute(query, (post_id,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Returns the information of the post comment
@posts.route('/posts/<post_id>/comments/<comment_id>', methods=['GET'])
def get_comment(post_id, comment_id):

    cursor = db.get_db().cursor()
    query = '''
        SELECT c.CommentID, c.PostID, c.AuthorID, u.FirstName AS AuthorFirstName, u.LastName AS AuthorLastName,
            c.Content, c.PublishedAt, c.CreatedAt
        FROM Post_Comment c
        JOIN User u ON c.AuthorID = u.UserID
        WHERE c.PostID = %s AND c.CommentID = %s
    '''
    cursor.execute(query, (post_id, comment_id))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a new comment for a specific post
@posts.route('/posts/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()
    author_id = data.get('AuthorID')
    content = data.get('Content')
    published_at = data.get('PublishedAt', None)

    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Post_Comment (PostID, AuthorID, Content, PublishedAt)
        VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(query, (post_id, author_id, content, published_at))
    db.get_db().commit()

    return make_response(jsonify({"message": "Comment created successfully"}), 201)
    