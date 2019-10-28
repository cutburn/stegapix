#!/usr/bin/env python

"""Very small module that handles pulling auth info out of
settings.ini file, as well as interfacing with the SQLlite3 db which
stores information about images we've seen already.

"""

import configparser

import sqlite3


def make_db_connection():
    """Make connection to stegapix SQLite3 database."""
    return sqlite3.connect("stegapix.db")


def init_stegapix_tables(cursor):
    """Initialize the steganography tables in the db if they aren't already."""
    init_image_table(cursor)
    init_search_index_table(cursor)


def init_image_table(cursor):
    """Initialize table that keeps track of images visited."""
    image_table_spec = "Stegapix(ID INTEGER PRIMARY KEY, URL TEXT)"
    cursor.execute("CREATE TABLE IF NOT EXISTS {0};".format(image_table_spec))


def init_search_index_table(cursor):
    """Initialize table that records search terms' last result page indices."""
    field_specs = []
    field_specs.append("ID INTEGER PRIMARY KEY")
    field_specs.append("TERM TEXT")
    field_specs.append("SEARCH_INDEX INTEGER")
    search_table_spec = "Search_Indices({0})".format(", ".join(field_specs))
    cursor.execute("CREATE TABLE IF NOT EXISTS {0};".format(search_table_spec))


def is_image_in_db(cursor, image_url):
    """Test that we have an image with the same URL in the database."""
    cursor.execute("SELECT URL FROM Stegapix WHERE URL=:URL",
                   {"URL": image_url})
    return cursor.fetchone() is not None


def add_images_to_db(cursor, image_objects):
    """Add entry for an already-visited image URL to sqlite database."""
    for image_object in image_objects:
        image_url = image_object.get("link")
        if image_url:
            cursor.execute("INSERT INTO Stegapix(URL) VALUES (?);",
                           (image_url,))


def check_start_from_last_visited():
    """Check settings to see if we will search from last index or index 1."""
    return get_ini_setting("GOOGLE",
                           "skip_traversed_result_indices",
                           required=False)


def get_last_visited_index(cursor, search_term):
    """Get last search result page index visited for a given term.

    This is part of an optional "cheat", wherein if we assume that
    search results don't move around much - or don't care much if they
    do, as long as what we find is less likely to have already been
    turned over if we start where we left off - we can start at the
    last search result page index we were on for a given search term,
    and save ourselves some queries.

    """
    cursor.execute("SELECT SEARCH_INDEX FROM Search_Indices WHERE TERM=:TERM",
                   {"TERM": search_term})
    term_item = cursor.fetchone()
    if term_item is not None:
        return term_item[0]
    else:
        return None


def set_last_visited_index(cursor, search_term, new_index):
    """Get last search result page index visited for a given term."""
    if get_last_visited_index(cursor, search_term) is None:
        cursor.execute("INSERT INTO Search_Indices(TERM, SEARCH_INDEX) "
                       "VALUES (?, ?);", (search_term, new_index))
    else:
        cursor.execute("UPDATE Search_Indices SET SEARCH_INDEX = ? "
                       "WHERE TERM = ?", (new_index, search_term))


def get_ini_setting(section, setting, required=True):
    """Get a named setting from the specified section of settings.ini."""
    try:
        config_parser = configparser.ConfigParser()
        config_parser.read("settings.ini")
        return config_parser.get(section, setting)
    except configparser.NoOptionError:
        if required:
            print("ERROR: Could not parse settings.ini file")
            exit(1)
        else:
            return None
