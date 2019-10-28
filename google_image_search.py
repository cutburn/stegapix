#!/usr/bin/env python

"""This module will encapsulate the stuff we need to do in order to
grab a few of the top Google image search results for a search
term.

For those who want to replicate at home, this requires a few
things like a Google Custom Search API key (which at time of writing
this comment is free for anyone with a Google account) and a Custom
Search Engine (see https://cse.google.com/cse/all). Once you've got an
API key and a custom search cx ID, you need only plug them into a
file called `settings.ini` like so:

[GOOGLE]
API_key = YOUR_KEY_HERE
cx_ID = YOUR_ID_HERE

And you should be in business!

"""

import json

import requests

import environment_utils as env_utils


def encode_search_term(search_term):
    """Encode multi-word search term as '+'-separated string."""
    return "+".join(search_term.split(" "))


def build_query_string(search_term, start_index):
    """Build and return a Google image search URL query string."""
    query_dict = {}
    query_dict["q"] = encode_search_term(search_term)
    query_dict["start"] = start_index
    query_dict["key"] = env_utils.get_ini_setting("GOOGLE", "API_Key")
    query_dict["cx"] = env_utils.get_ini_setting("GOOGLE", "cx_ID")
    query_dict["searchType"] = "image"
    query_dict["imgSize"] = "large"
    return "&".join([k + "=" + v for k, v in query_dict.items()])


def build_url(search_term, start_index):
    """Build and return a Google image search URL."""
    base_url = "https://www.googleapis.com/customsearch/v1"
    return base_url + "?" + build_query_string(search_term,
                                               start_index)


def get_json_results(search_term, start_index="1"):
    """Get Google image search JSON results for a search term."""
    search_url = build_url(search_term, start_index)
    print(search_url)
    response = requests.get(search_url)
    if response.status_code == requests.codes.ok:
        response_content = response.content.decode("utf-8")
        return json.loads(response_content)
    else:
        print("ERROR: Did not receive 200 OK response on query")
        exit(1)
