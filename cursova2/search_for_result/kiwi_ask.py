import requests
import json


def ask_for_city_code(name_of_city, name_of_country):
    url = "https://api.skypicker.com/locations?"
    url += "term=" + name_of_city
    location_types = "city"
    limit = 1
    url += "&location_types" + location_types
    url += "&limit=" + str(limit)
    response = requests.get(url)
    try:
        city = response.json()["locations"][0]
        if city["country"]["name"] == name_of_country:
            return city["code"]
        else:
            return city["code"]
    except:
        return None


def ask_for_flights(city_from, city_to, date_from, date_to, return_from,
                    return_to, nights_in_dst_to, adults, atime_to, sort,
                    limit="10", curr="USD",
                    partner="picky", nights_in_dst_from="1"):
    city_from = ask_for_city_code(city_from[0], city_from[1])
    city_to = ask_for_city_code(city_to[0], city_to[1])
    url = "https://api.skypicker.com/flights?"
    url += "fly_from={}&fly_to={}&date_from={}&date_to={}&return_from={}&return_to={}&nights_in_dst_from={}&nights_in_dst_to={}&adults={}&atime_to={}&sort={}&limit={}&curr={}&partner={}".format(
        city_from, city_to, date_from, date_to, return_from, return_to,
        nights_in_dst_from, nights_in_dst_to, adults, atime_to, sort, limit,
        curr, partner)
    response = requests.get(url)
    return response.json()
