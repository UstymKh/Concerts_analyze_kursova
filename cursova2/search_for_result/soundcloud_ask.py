import soundcloud
import six
import json


def ask_for_track(name_of_track):
    client_id = "gRYERdxaARcAEmU80B9CpaTB8ewz33EI"
    client = soundcloud.Client(client_id=client_id)
    tracks = client.get('/tracks', q=name_of_track)
    track = tracks[0]
    return str(track.stream_url) + "?client_id=" + client_id
print(ask_for_track("Так мало тут тебе друга ріка"))