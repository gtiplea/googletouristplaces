from flask import Flask
from flask_restful import Resource, Api
from firebase import firebase
import json
import os.path
import urllib.parse
import requests

app = Flask(__name__)
api = Api(app)
google_places = {}
firebase_url = ""
firebase_name = ""

firebase = firebase.FirebaseApplication(firebase_url, None)

class GooglePlaces(Resource):
    def get(self, language, city_name):
        language_city = language + '+' + city_name
        if language_city in google_places:
            return google_places[language_city]
        main_api = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
        api_key = ''
        url = main_api + urllib.parse.urlencode({'query': city_name + ' point of interest'})
        url = url + '&' + urllib.parse.urlencode({'language': language})
        url = url + '&' + urllib.parse.urlencode({'key': api_key})
        json_data = requests.get(url).json()
        google_places[language_city] = json_data
        firebase.post('/' + firebase_name + '/googleplaces', {language_city: google_places[language_city]})
        return google_places[language_city]

api.add_resource(GooglePlaces, '/<string:language>/googleplaces/<string:city_name>')

def main():
    result = firebase.get('/' + firebase_name + '/googleplaces', '')
    if result != None:
        for place in result.values():
            for place_name, value in place.items():
                google_places[place_name] = value
    #app.run(host='0.0.0.0', debug=True)

main()