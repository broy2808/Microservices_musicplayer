#README Dev 2
#Create a new service to generate playlists in XSPF format.
#This service will sit in front of the API gateway, contacting the other microservices through the gateway as needed.
#Note that there are XSPF fields for every piece of data maintained by various microservices, though you may need to consult the specification to find them.
#In order to retrieve the data for a feed, your microservice will need to make HTTP requests to the other microservices

#installed on Tuffix with the following command:
#$ pip3 install --user requests

from flask import request, jsonify
#from flask_api import exceptions, status
import requests
import xspf
from flask import Flask

#app = flask_api.FlaskAPI(__name__)
app = Flask(__name__)

#retrieve all the details in XML format using playlist_id in url, fetch the specific record

@app.route("/")
def hello():
    return "Welcome to XSPF conversion! Please add username into current URL to get the details."


@app.route("/xspf/playlist.xspf/<string:id>")
def playlists(id):

    #using requests module

    r = requests.get("http://127.0.0.1:9003/recources/playlists/"+id)

    r= r.json()

    #using the xspf to convert in the XSPF format

    x = xspf.Xspf()

    x.title=r['playlist_title']
    username = r['username']

    user_details = requests.get("http://127.0.0.1:9000/api/users/"+username)
    user_details=user_details.json()
    #x.creator=user_details['full_name']
    print(user_details)
    x.creator=user_details['full_name']
    x.info=user_details['email']
    #x.creator=user_details['homeurl']


    trackList = r['track_list']

    for tracks in trackList:

        track_details = requests.get(tracks['trackurl']);
        track_details=track_details.json()[0]
        print(track_details)
        print(track_details['track_title'])
        #requesting the description microservice to fetch the track's description
        user_desc=requests.get("http://127.0.0.1:9001/api/users/gettrackdesc/"+username+'/'+track_details['URL_media'])
        user_desc=user_desc.json()
        print(track_details['URL_media'])
        print(user_desc)
        #{'night.co3': {'description': 'My Favourite Track1'}}
        # y= user_desc[track_details['URL_media']]
        # x.annotation=y['description']

        x.add_track(annotation= user_desc[track_details['URL_media']]['description'], title=track_details['track_title'], creator=track_details['artist'], duration= track_details['track_length'], album=track_details['album_title'], identifier=track_details['URL_media'])

# {'id': 1, 'playlist_title': 'MyPlaylist', 'URL_list': '["Track1","Track2","Track3","Track4"]', 'username': 'Brandon', 'description': 'This Track is good'}

    print(x.toXml())
    y=x.toXml()
    return y, 200,{'Content-Type': 'application/xml; charset=utf-8'}
