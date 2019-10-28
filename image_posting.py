#!/usr/bin/env python

"""This module encapsulates posting an image file to Imgur and
subsequently tweeting that image to twitter.

For those who want to replicate at home, this requires a few Twitter
API auth pieces, as well as an Imgur account client ID and secret (see
below - a little googling should tell you how these can be
obtained). Once you've got them you need only plug them into a file
called `settings.ini` like so:

[TWITTER]
API_Key = YOUR_API_KEY_HERE
API_Secret = YOUR_API_SECRET_HERE
Access_Token_Key = YOUR_ACCESS_TOKEN_HERE
Access_Token_Secret = YOUR_ACCESS_TOKEN_SECRET_HERE

[IMGUR]
Client_ID = YOUR_CLIENT_ID_HERE
Client_Secret = YOUR_CLIENT_SECRET_HERE

And you should be in business!

"""

from TwitterAPI import TwitterAPI
from imgurpython import ImgurClient

import ini_util


def post_to_imgur(image_file_name):
    """Post and image to Imgur."""
    client_id = ini_util.get_ini_setting("IMGUR", "Client_ID")
    client_secret = ini_util.get_ini_setting("IMGUR", "Client_Secret")
    client = ImgurClient(client_id, client_secret)
    items = client.upload_from_path(image_file_name, anon=False)
    return items['id']


def post_to_twitter(imgur_id):
    """Tweet an Imgur image with a given ID to Twitter, with a preview."""
    CONSUMER_KEY = ini_util.get_ini_setting("TWITTER", "API_Key")
    CONSUMER_SECRET = ini_util.get_ini_setting("TWITTER", "API_Secret")
    ACCESS_TOKEN_KEY = ini_util.get_ini_setting("TWITTER", "Access_Token_Key")
    ACCESS_TOKEN_SECRET = ini_util.get_ini_setting("TWITTER",
                                                   "Access_Token_Secret")

    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY,
                     ACCESS_TOKEN_SECRET)
    request = api.request("statuses/update", {"status":
                                              "http://imgur.com/" + imgur_id})
    print(request.status_code)


def post_image(image_file_name):
    """Post an image to Twitter via Imgur."""
    image_id = post_to_imgur(image_file_name)
    post_to_twitter(image_id)
