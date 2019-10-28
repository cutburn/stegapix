#!/usr/bin/env python

"""This module encapsulates posting an image file to Imgur and
subsequently tweeting that image to twitter.

"""

from TwitterAPI import TwitterAPI
from imgurpython import ImgurClient

from . import environment_utils as env_utils


def post_image(image_file_name):
    """Post an image to Twitter via Imgur."""
    image_id = post_to_imgur(image_file_name)
    post_to_twitter(image_id)


def post_to_imgur(image_file_name):
    """Post and image to Imgur."""
    client_id = env_utils.get_ini_setting("IMGUR", "Client_ID")
    client_secret = env_utils.get_ini_setting("IMGUR", "Client_Secret")
    client = ImgurClient(client_id, client_secret)
    items = client.upload_from_path(image_file_name, anon=False)
    return items['id']


def post_to_twitter(imgur_id):
    """Tweet an Imgur image with a given ID to Twitter, with a preview."""
    CONSUMER_KEY = env_utils.get_ini_setting("TWITTER", "API_Key")
    CONSUMER_SECRET = env_utils.get_ini_setting("TWITTER", "API_Secret")
    ACCESS_TOKEN_KEY = env_utils.get_ini_setting("TWITTER", "Access_Token_Key")
    ACCESS_TOKEN_SECRET = env_utils.get_ini_setting("TWITTER",
                                                    "Access_Token_Secret")

    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY,
                     ACCESS_TOKEN_SECRET)
    request = api.request("statuses/update", {"status":
                                              "http://imgur.com/" + imgur_id})
    print(request.status_code)
