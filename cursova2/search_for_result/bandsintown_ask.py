import requests
import json
from search_for_result.change_name import change_name


def ask_for_artist(name_of_artist):
    headers = {
        'accept': 'application/json',
    }
    params = (
        ('app_id', '6aee7836db71e6ad959e61e00f7b436f'),
    )
    url = 'https://rest.bandsintown.com/artists/'
    name_of_artist = change_name(name_of_artist)
    url += name_of_artist
    response = requests.get(url, headers=headers, params=params)
    try:
        return response.json()
    except:
        return None


def ask_for_events(name_of_artist, date="all"):
    name_of_artist = change_name(name_of_artist)
    url = "https://rest.bandsintown.com/artists/" + name_of_artist + \
          "/events?app_id=6aee7836db71e6ad959e61e00f7b436f&date=" + date
    response = requests.get(url)
    try:
        return response.json()
    except:
        return None

