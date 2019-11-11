
# Music Player API from "Creating Web APIs with Python and Flask"
# What's new
#  * Switched from Flask to Flask API
#    <https://www.flaskapi.org>
#  * Switched to PugSQL for database access
#    <https://pugsql.org>
#    This  microservice handles all the user specific information
#  * New API calls:
#    - GET /api/users/all -List of all users present in DB
#    - GET and DELETE /api/users/<string:id> to retrieve a specific user information and also delete a users information, input username in the url
#    - POST /api/users to create a new user, input data fields like {"username": "yyy", "full_name": "yyy zzz", "password": "xyz", "email": "xyz@abc", "homeurl":"www.google.com"}
#    - POST  /api/users/authenticate to authenticate a user, input data fields like {"username": "yyy", "password": "xyz"}
#    - PUT /api/users/changepassword to change a user's password, input data fields like {"username": "yyy", "password_old": "xyz","password_new": "xyz2"}

import sys
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import base64, hashlib, bcrypt, os, sys


app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


@app.cli.command('init')
#Initialize the database
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('users.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = queries._engine.raw_connection()
    db.commit ()
    db.close()
#Base url
@app.route('/', methods=['GET'])
def home():
    return '''<h1>User Dataload Microservice running</h1>
<p>A prototype API for musiclist of users.</p>'''

#This method returns all the users in database
@app.route('/api/users/all', methods=['GET'])
def all_users():
    all_users = queries.all_users()
    return list(all_users),status.HTTP_200_OK


#Below url returns particular users information and also we can delete a users information from this
@app.route('/api/users/<string:id>', methods=['GET','DELETE'])
#below method returns a users information
def user(id):
    if request.method == 'GET':
        user = queries.user_by_id(id=id)
        if user:
            return user,status.HTTP_200_OK
        else:
            raise exceptions.NotFound()
    if request.method == 'DELETE':
        return delete_user(id)
#Delete a specific user
def delete_user(userid):
    if request.method == 'DELETE':
        username=userid
        if (queries.delete_user(username=username)):
            db = queries._engine.raw_connection()
            db.commit()
            return {username:" Deleted Successfully!"},status.HTTP_200_OK

        else:
            return {username:"Cannot delete user. Invalid Username!"},status.HTTP_400_BAD_REQUEST
    return {"status":status.HTTP_200_OK}

#This method handles creation of new user's
@app.route('/api/users', methods=['POST','GET'])
def users_ops():
     if request.method == 'POST':
         return create_user(request.data)
     return {"Status":status.HTTP_200_OK},status.HTTP_200_OK


#method to create new user. Also, validate the input json file format. Only one json row can be inserted at a time
def create_user(user):
    user = request.data

    required_fields = ['username','full_name','password','email']
    if not all([field in user for field in required_fields]):
        raise exceptions.ParseError()
    if (request.data.get('username')=="" ) or (request.data.get('full_name')=="") or (request.data.get('password')=="") or (request.data.get('email')=="") :
        raise exceptions.ParseError()
    try:
        username = request.data.get('username')
        full_name = request.data.get('full_name')
        password_hash=bcrypt.hashpw(base64.b64encode(hashlib.sha256(request.data.get('password').encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe').decode('utf-8')
        email = request.data.get('email')
        homeurl=request.data.get('homeurl')
        queries.create_user(username=username,full_name=full_name,password=password_hash,email=email,homeurl=homeurl)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    return {user['username']: status.HTTP_201_CREATED},status.HTTP_201_CREATED


#authenticate a user if the supplied id and password is correct.
@app.route('/api/users/authenticate', methods=['GET','POST'])
def auth_user():
    if request.method == 'POST':
        username=request.data.get('username')
        password_hash=bcrypt.hashpw(base64.b64encode(hashlib.sha256(request.data.get('password').encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe').decode('utf-8')
        valid=queries.validate_user(username=username,password=password_hash)
        if valid:
            return {username:" Authenticated Successfully!"},status.HTTP_200_OK
        else:
            return {username:"Cannot authenticate user. Invalid Username or Password!"},status.HTTP_400_BAD_REQUEST
    return {"status":status.HTTP_200_OK},status.HTTP_200_OK

#Change a users password if new and current password provided
@app.route('/api/users/changepassword', methods=['PUT','GET'])
def changepassword():
    if request.method == 'PUT':
        user = request.data
        required_fields = ['username','password_old','password_new']
        if not all([field in user for field in required_fields]):
            raise exceptions.ParseError()
        if (request.data.get('username')=="" ) or (request.data.get('password_old')=="") or (request.data.get('password_new')==""):
            raise exceptions.ParseError()
        try:
            username=request.data.get('username')
            password_hash_old=bcrypt.hashpw(base64.b64encode(hashlib.sha256(request.data.get('password_old').encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe').decode('utf-8')
            password_hash=bcrypt.hashpw(base64.b64encode(hashlib.sha256(request.data.get('password_new').encode('utf-8')).digest()), b'$2b$12$DbmIZ/a5LByoJHgFItyZCe').decode('utf-8')
            valid=queries.validate_user(username=username,password=password_hash_old)
            if valid:
                queries.update_user(username=username,password=password_hash)
                db = queries._engine.raw_connection()
                db.commit()
                return {username:"Password changed Successfully"},status.HTTP_200_OK
            else:
                return {username:" Cannot authenticate user. Invalid Username or Password!"},status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return { 'error': str(e) }, status.HTTP_409_CONFLICT

        return user['username'], status.HTTP_201_CREATED
    return {"status":status.HTTP_200_OK},status.HTTP_200_OK
