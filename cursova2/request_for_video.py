import urllib.request
import re
import urllib.parse


def make_url(name):
    query_string = "+".join(name.split())
    query_string = "search_query=" + urllib.parse.quote(query_string)
    html_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})',
                                html_content.read().decode())
    return "http://www.youtube.com/watch?v=" + search_results[0]


