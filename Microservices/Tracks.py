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
from flask import request, jsonify,_app_ctx_stack
from flask_api import exceptions, status
import pugsql
import os
import time
from sqlite3 import dbapi2 as sqlite3
import uuid
#from hashlib import md5
#from datetime import datetime
#from flask import Flask, request, jsonify, g, json, abort, Response, flash, _app_ctx_stack, session

app = flask_api.FlaskAPI(__name__)
app.config["DEBUG"] = True
app.config.from_envvar('APP_CONFIG')

DATABASE0 = os.path.join(app.root_path, 'track0.db')
DATABASE1 = os.path.join(app.root_path, 'track1.db')
DATABASE2 = os.path.join(app.root_path, 'track2.db')
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
# default authenticated configuration
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin123'
#load all sql queries from queries directory
#queries = pugsql.module('queries/')
#connect to DB
def get_db(server_id):
    """Opens a new database connection if there is none yet for the  current application context.    """
    DATABASE = "DATABASE" + str(server_id)
    print(DATABASE)
    tracktop = _app_ctx_stack.top
    if not hasattr(tracktop, 'track_db0') and server_id == 0:
        tracktop.track_db0 = sqlite3.connect(app.config[DATABASE], detect_types=sqlite3.PARSE_DECLTYPES)
        tracktop.track_db0.row_factory = sqlite3.Row
    if not hasattr(tracktop, 'track_db1') and server_id == 1:
        tracktop.track_db1 = sqlite3.connect(app.config[DATABASE], detect_types=sqlite3.PARSE_DECLTYPES)
        tracktop.track_db1.row_factory = sqlite3.Row
    if not hasattr(tracktop, 'track_db2') and server_id == 2:
        tracktop.track_db2 = sqlite3.connect(app.config[DATABASE], detect_types=sqlite3.PARSE_DECLTYPES)
        tracktop.track_db2.row_factory = sqlite3.Row

    if server_id == 0:
        return tracktop.track_db0
    elif server_id == 1:
        return tracktop.track_db1
    else:
        return tracktop.track_db2
#queries.connect(app.config['DATABASE_URL'])

@app.cli.command('init')
def init_db():
    sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
    sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le))
    for i in range(0,3):
    #with app.app_context():
        db = get_db(i)
        #db = queries._engine.raw_connection()
        with app.open_resource('tracks.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
def get_server_id(track_id):
    """return sharding for server"""

    return track_id % 3

@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    tracktop = _app_ctx_stack.top
    if hasattr(tracktop, 'track_db0'):
        tracktop.track_db0.close()
    if hasattr(tracktop, 'track_db1'):
        tracktop.track_db1.close()
    if hasattr(tracktop, 'track_db2'):
        tracktop.track_db2.close()



@app.route("/")
def hello():
	return "<h1>A Super awesome API that will allow you to create and listen to tracks over and over!</h1>"

#need to also return URL of the newly-created object in the Location header field.
@app.route("/recources/tracks", methods=['GET','POST'])
def create_track():
    required_fields = ['id','track_title','album_title','artist','track_length','URL_media']
    user_data = request.data
    if not all([field in user_data for field in required_fields]):
        raise exceptions.ParseError()
    if (request.data.get('id')=="") or (request.data.get('track_title')=="") or (request.data.get('album_title')=="") or (request.data.get('artist')=="") or (request.data.get('track_length')=="") or (request.data.get('URL_media')==""):
        return exceptions.ParseError()

    server_id = get_server_id(request.data.get('id'))
    db = get_db(server_id)
    if db.execute('''INSERT INTO tracks(id, track_title, album_title, artist, track_length, URL_media, URL_artwork) VALUES(?,?,?,?,?,?,?)''',
            [request.data.get('id'), request.data.get('track_title'), request.data.get('album_title'), request.data.get('artist'),request.data.get('track_length'),request.data.get('URL_media'),request.data.get('URL_artwork')]):
        db.commit()
    #if queries.create_track(track_title= request.data.get('track_title'), album_title=request.data.get('album_title'), artist=request.data.get('artist'),track_length=request.data.get('track_length'),URL_media=request.data.get('URL_media'),URL_artwork=request.data.get('URL_artwork')):
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
    server_id = get_server_id(id)
    db = get_db(server_id)

    if not request.data.get('track_title'):
        return {"Status":status.HTTP_409_CONFLICT}, status.HTTP_409_CONFLICT
    elif db.execute('''UPDATE tracks set track_title= ?  WHERE id = ?''',(request.data.get('track_title'),id,)):
        db.commit()
        return {"Status":status.HTTP_201_CREATED}, status.HTTP_201_CREATED
    else:
        return {"Status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST

#this will delete a track based off of its id
def delete_track(id):
    server_id = get_server_id(id)
    db = get_db(server_id)

    if db.execute('''DELETE FROM tracks WHERE id =?''',(id,)):
        db.commit()
        return {"Status":status.HTTP_204_NO_CONTENT}, status.HTTP_204_NO_CONTENT
    else:
        return {"Status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST

#this method will return a playlist based off of its id
def get_track(id):
    server_id = get_server_id(id)
    db = get_db(server_id)
    cur=db.execute('''SELECT * FROM tracks WHERE id =?''',(id,))
    items=[]
    for row in cur:
        items.append({'id':row[0],'track_title':row[1], 'album_title':row[2], 'artist':row[3], 'track_length':row[4], 'URL_media':row[5], 'URL_artwork':row[5]})
    if items!=[]:
        return items
    else:
        raise exceptions.NotFound()
