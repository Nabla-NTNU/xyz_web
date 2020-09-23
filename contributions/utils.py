"""Utility functions. Mainly used by models.py."""

from urllib.parse import urlparse
import secrets
import html


def get_random_token(token_length):
    return secrets.token_urlsafe(token_length)


# Naming convention:
#
# `players` and `parsers` are dicts with key begin the name of the player ("youtube" or "vimeo") and the value is either the
# appropriate parser or player.
# Parser here refers to the parser that finds the video id given a video url,
# and player is the embeded player.
#
# The parsers have names on the form `get_video_id_<service_name>` and
# players have names `<service_name>Player`.

def get_video_id_youtube(video_url):
    parsed = urlparse(video_url)
    queries = parsed.query.split("&")
    for query in queries:
        key, value = query.split("=")
        if key == "v":
            return value
    return None


def get_video_id_vimeo(video_url):
    parsed = urlparse(video_url)
    id = parsed.path.strip('/')
    return id


def youtubePlayer(video_id):
    return f'<iframe width="640" height="360" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'


def vimeoPlayer(video_id):
    return f'<iframe src="https://player.vimeo.com/video/{video_id}?embedparameter=value" width="640" height="360" frameborder="0" allowfullscreen></iframe>'


def player(url_parser, specific_player):
    def video_player(video_url):
        video_id = url_parser(video_url)
        video_id = html.escape(video_id)
        return specific_player(video_id)
    return video_player

parsers = {
    "youtube": get_video_id_youtube,
    "vimeo": get_video_id_vimeo,
}


players = {
    "youtube": player(get_video_id_youtube, youtubePlayer),
    "vimeo": player(get_video_id_vimeo, vimeoPlayer),
}
