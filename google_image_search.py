#!/usr/bin/env python

"""This module will encapsulate the stuff we need to do in order to
grab a few of the top Google image search results for a search
term. For those who want to replicate at home, this requires a few
things like a Google Custom Search API key (which at time of writing
this comment is free for anyone with a Google account) and a Custom
Search Engine (see https://cse.google.com/cse/all). Once you've got an
API key and a custom search cx ID, you need only plug them into a
file called `settings.ini` like so:

[DEFAULT]
API_key = YOUR_KEY_HERE
cx_ID = YOUR_ID_HERE

And you should be in business!

"""

import configparser
import json

import requests


def get_ini_setting(setting):
    """Get a named setting from the DEFAULT section of settings.ini."""
    try:
        config_parser = configparser.ConfigParser()
        config_parser.read("settings.ini")
        return config_parser.get("DEFAULT", setting)
    except configparser.NoOptionError:
        print("ERROR: Could not parse settings.ini file")
        exit(1)


def encode_search_term(search_term):
    return "+".join(search_term.split(" "))


def build_query_string(search_term, start):
    """Build and return a Google image search URL query string."""
    query_dict = {}
    query_dict["q"] = encode_search_term(search_term)
    query_dict["start"] = "1"
    query_dict["key"] = get_ini_setting("API_key")
    query_dict["cx"] = get_ini_setting("cx_ID")
    query_dict["searchType"] = "image"
    return "&".join([k + "=" + v for k, v in query_dict.items()])


def build_url(search_term):
    """Build and return a Google image search URL."""
    base_url = "https://www.googleapis.com/customsearch/v1"
    return base_url + "?" + build_query_string(search_term)


def get_json_results_for_term(search_term, start_index="1"):
    """Get Google image search JSON results for a search term."""
    search_url = build_url(search_term)
    print(search_url)
    r = requests.get(search_url, start_index)
    if r.status_code == requests.codes.ok:
        response = r.content.decode("utf-8")
        result = json.loads(response)
        print(result)
    else:
        print("ERROR: Did not receive 200 OK response on query")
        exit(1)
