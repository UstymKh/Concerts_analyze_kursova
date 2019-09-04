def change_name(name_of_artist):
    name_of_artist.replace(" ", "%20")
    name_of_artist.replace("/", "%252F")
    name_of_artist.replace("?", "%253F")
    name_of_artist.replace("*", "%252A")
    name_of_artist.replace("'", "%27C")
    return name_of_artist
