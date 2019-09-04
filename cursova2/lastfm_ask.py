import requests
import json
from search_for_result.change_name import change_name


def ask_for_artist(name_of_artist):
    name_of_artist = change_name(name_of_artist)
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=' + \
          name_of_artist + \
          '&api_key=4c01317b97eced217191b8523d01e09c&format=json'
    response = requests.get(url)
    try:
        error = response.json()["error"]
        return None
    except:
        return response.json()


def get_top_track(name_of_artist):
    original_name_of_artist = " " + name_of_artist
    name_of_artist = change_name(name_of_artist)
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks' + \
          '&artist=' + name_of_artist + \
          '&api_key=4c01317b97eced217191b8523d01e09c&format=json'
    response = requests.get(url)
    try:
        error = response.json()["error"]
        return None
    except:
        return response.json()["toptracks"]['track'][0][
                   "name"] + original_name_of_artist


