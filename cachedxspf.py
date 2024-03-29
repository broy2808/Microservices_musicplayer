#README Dev 2:
#Using Memcached to cache JSON responses
#Modifying the existing xspy.py(XSPF Code)

#$ pip3 install --user pymemcache
#sudo apt-get install memcached
#sudo service memcached start

#Run using:  export FLASK_APP=cachedxspf
#            flask run

from flask import request, jsonify
#from pymemcache.client import base
from pymemcache.client import base
#from pymemcache.client.base import Client
import requests
import xspf
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to XSPF conversion! Please add playlist id(existing id's are 1,2,3,4,5) into /xspf/playlist.xspf/  URL to get the details."


def do_playlist_query(id):
    r = requests.get("http://127.0.0.1:9003/recources/playlists/"+id)
    r= r.json()
    return r

def do_user_query(username):
    r= requests.get("http://127.0.0.1:9000/api/users/"+username)
    r=r.json()
    return r

@app.route("/xspf/playlist.xspf/<string:id>")
def playlists(id):
    #instantiating the client
    client = base.Client(('localhost', 11211))
    #now client object started on port 11211
    #store the key-value pair!
    result = client.get(id)
    #client.set(id, result)
    #if the cached object does not exist:
    if result is None:
        #make the HTTP request from the microservice and store the json response in Memcached with expiration time!
        result = do_playlist_query(id)
        print("first result:", result)
        #result key=value(result[username]=do_user_query)
        user_details=do_user_query(result['username'])
        result.update(user_details)
        trackList = result['track_list']
        #loop to request track details(from desc service) of different tracks in the playlist
        for tracks in trackList:
            #calling the tracks service here: (directly from db)
            track_details= requests.get(tracks['trackurl'])
            track_details=track_details.json()[0]
            #for each track, calling the description service
            user_desc=requests.get("http://127.0.0.1:9001/api/users/gettrackdesc/"+result['username']+'/'+track_details['URL_media'])
            user_desc=user_desc.json()
            #track_details.update(user_desc)
        #store the JSON response in Memcached with expiration of atleast 60 sec
        print("Random: ",result)
        result.update(track_details)
        print("Random1 : ",result)
        client.append(id, result, 100)
        #print("the json objects are not properly appended!")
        #print("please check how I am appending the json objects to store in cache")
    #if the cached object exists: use its value(result) to construct the xspf!
    x= xspf.Xspf()
    print("please find the below result")
    print(result)
    #using result json object to construct the xspf
    x.title=result['playlist_title']
    x.creator=result['full_name']
    x.info=result['email']
    # trackList=result['track_list']
    print("below result")
    print(result)
    #each playlist of user has multiple tracks such as file1, file2, file3,file4.mp3
    for track in trackList:
        tr1=xspf.Track()
        tr1.title=result['track_title']
        tr1.creator=result['artist']
        tr1.duration=result['track_length']
        tr1.album=result['album_title']
        tr1.identifier=result['URL_media']
        tr1.annotation=result['description']
        x.add_track(tr1)
    y=x.toXml()
    return y, 200,{'Content-Type': 'application/xml; charset=utf-8'}
