import requests


def ask_for_place(latitude, longitude, checkin, checkout, guests,
                  currency="USD", sortby="popularity", radius="5000",
                  limit="10"):
    checkin = "/".join(checkin.split("/")[::-1])
    checkout = "/".join(checkout.split("/")[::-1])
    url = "https://api.stay22.com/v2/hotelscombined?"
    url += "latitude={}&longitude={}&radius={}&checkin={}&checkout={}&guests={}&currency={}&sortby={}&limit={}".format(
        latitude, longitude, radius, checkin, checkout, guests, currency,
        sortby, limit)
    response = requests.get(url)
    try:
        return response.json()["results"][0]["rooms"][0]["rates"][0]["total"]
    except:
        try:
            return response.json()["results"][0]["rooms"]["rates"][0]["total"]
        except:
            return 380