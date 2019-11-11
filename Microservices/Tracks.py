#README
#Tracks methods

#To create a track use the URL http://127.0.0.1:5000/recources/tracks
#Arguments- in json format - track_title: newTitle, album_title: newAlbumTitle, artist:newArtist, track_length:newLength, URL_media:newMedia (URL_media not required)

#To retrieve a track use use URL GET http://127.0.0.1:5000/recources/tracks/<int:id>
#Arguments - in URL - an integer representing the ID of a given track

#To edit a Track use URL PUT http://127.0.0.1:5000/recources/tracks/<int:id>
#Arguments - in URL - an integer representing the ID of a given track
#Arguments - in json format - track_title:newTrackTitle

#To Delete a Track use URL DELETE http://127.0.0.1:5000/recources/tracks/<int:id>
#Arguments - in URL - an integer representing the ID of a given track

import flask_api
from flask import request
from flask import jsonify
from flask_api import exceptions, status
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config["DEBUG"] = True
app.config.from_envvar('APP_CONFIG')

#load all sql queries from queries directory
queries = pugsql.module('queries/')
#connect to DB
queries.connect(app.config['DATABASE_URL'])

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('users.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route("/")
def hello():
	return "<h1>A Super awesome API that will allow you to create and listen to tracks over and over!</h1>"

#need to also return URL of the newly-created object in the Location header field.
@app.route("/recources/tracks", methods=['GET','POST'])
def create_track():
    required_fields = ['track_title','album_title','artist','track_length','URL_media']
    user_data = request.data
    if not all([field in user_data for field in required_fields]):
        raise exceptions.ParseError()
    if (request.data.get('track_title')=="") or (request.data.get('album_title')=="") or (request.data.get('artist')=="") or (request.data.get('track_length')=="") or (request.data.get('URL_media')==""):
        return exceptions.ParseError()
    if queries.create_track(track_title= request.data.get('track_title'), album_title=request.data.get('album_title'), artist=request.data.get('artist'),track_length=request.data.get('track_length'),URL_media=request.data.get('URL_media'),URL_artwork=request.data.get('URL_artwork')):
        return {"Status":status.HTTP_201_CREATED}, status.HTTP_201_CREATED
    else:
        return {"Status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST

#this method will simply route to modify, delete, or get and item based on its id
@app.route("/recources/tracks/<int:id>", methods=['GET','PUT','DELETE'])
def tracks(id):
    if request.method == 'PUT':
        return modify_track(id)
    elif request.method == 'DELETE':
        return delete_track(id)
    elif request.method == 'GET':
        return get_track(id)

#This URL with a POST will allow a user to modify a track with a given ID
#For now a user will only be able to modify the song name
#The data that we will request to modify will be in JSON format
#where the method will expect to key to be track_title or else an exception will be raised
def modify_track(id):
    if not request.data.get('track_title'):
        return {"Status":status.HTTP_409_CONFLICT}, status.HTTP_409_CONFLICT
    elif queries.update_by_id(id=id, track_title=request.data.get('track_title')):
        return {"Status":status.HTTP_201_CREATED}, status.HTTP_201_CREATED
    else:
        return {"Status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST

#this will delete a track based off of its id
def delete_track(id):
    if queries.delete_by_id(id=id):
        return {"Status":status.HTTP_204_NO_CONTENT}, status.HTTP_204_NO_CONTENT
    else:
        return {"Status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST

#this method will return a playlist based off of its id
def get_track(id):
    temp = queries.search_by_id(id=id)
    #return queries.search_by_id(id=id)
    if temp:
        return temp, status.HTTP_200_OK
    else:
        raise exceptions.NotFound()
