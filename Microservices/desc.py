#    This  microservice handles all the track description update specific information
#  * New API calls:
#    - POST /api/users/settrackdesc change description of a track, input data {  "trackurl": "track123","username": "bony2018", "description": "My favourite track1!"}
#      Note if trackurl and username combo not exists it will insert, otherwise it will update the description
#    - GET /api/users/gettrackdesc/<string:username>/<string:trackurl> to retrieve a track description of specific user , input username and trackurl in the API url


import sys
import flask_api
from flask import request,_app_ctx_stack
from flask_api import status, exceptions
import pugsql
import base64, hashlib, bcrypt, os, sys
from sqlite3 import dbapi2 as sqlite3

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])
DATABASE0 = os.path.join(app.root_path, 'track0.db')
DATABASE1 = os.path.join(app.root_path, 'track1.db')
DATABASE2 = os.path.join(app.root_path, 'track2.db')

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
    db.close()
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

# def get_server_id(track_id):
#     """return sharding for server"""
#     return track_id % 3
#
# def check_the_track(url):
#     id1=0
#     print("Inside check 1",url)
#     for id in range(3):
#         server_id = get_server_id(id)
#         db = get_db(server_id)
#         cur=db.execute('''SELECT id FROM tracks WHERE URL_media=?''',(url,))
#         for row in cur:
#             id1=row[0]
#             return id1
#     return id1

def get_server_id(track_id):
    """return sharding for server"""
    #return track_id % 3
    print(track_id)
    return (uuid.UUID(track_id).int) %3


def check_the_track(URL):
    id1=0

    for i in range(3):
        db = get_db(i)
        cur=db.execute('''SELECT id FROM tracks WHERE URL_media=?''',(URL,))
        for row in cur:
              id1=row[0]
              print("Hello ",id1)
              return id1
    return id1


#Base url
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Tracks description microservice running</h1>
<p>A prototype API for musiclist of users.</p>'''


#Set a tracks description if not present. Also, if description already present update it
@app.route('/api/users/settrackdesc', methods=['GET','POST'])
def track_ops():
    if request.method == 'POST':
        return create_desc(request.data)
    return {"status":status.HTTP_200_OK},status.HTTP_200_OK

#Update or create description of track
def create_desc(track):

    track = request.data
    required_fields = ['trackurl','description','username']
    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        username = request.data.get('username')
        trackurl = request.data.get('trackurl')
        description=request.data.get('description')


        if (trackurl==""):
            return { 'error': "Invalid trackurl!" },status.HTTP_400_BAD_REQUEST

        valid=queries.user_by_id(id=username)
        trackid=queries.fetch_track_id(trackurl=trackurl,username=username)
        print("Hello ",trackurl,trackid)
        id_check=check_the_track(trackurl)
        if id_check==0:
            return { 'error': "Track url invalid! No reference found in Track list." }, status.HTTP_400_BAD_REQUEST

        print(trackid,trackurl,username,description)
        if (valid):
            if (trackid):
                queries.update_track(username=username,trackurl=trackurl,description=description)
                return {"Success":status.HTTP_202_ACCEPTED},status.HTTP_202_ACCEPTED
            else:
                queries.insert_track(trackurl=trackurl,username=username,description=description)

        else:
            return {track['username']:" Does not exists"},status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    return {track['trackurl']:status.HTTP_201_CREATED},status.HTTP_201_CREATED

#Get a track specific URL.
@app.route('/api/users/gettrackdesc/<string:username>/<string:trackurl>', methods=['GET'])
def track_ret(username,trackurl):
        track_desc=queries.fetch_track(trackurl=trackurl,username=username)
        if(track_desc!=None):
            return {trackurl:track_desc},status.HTTP_200_OK
        else:
            return {trackurl:"Do not exists"},status.HTTP_400_BAD_REQUEST
