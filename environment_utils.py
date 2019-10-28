#!/usr/bin/env python

"""Very small module that handles pulling auth info out of
settings.ini file, as well as interfacing with the SQLlite3 db which
stores information about images we've seen already.

"""

import configparser

import sqlite3


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

def make_db_connection():
    """Make connection to stegapix SQLite3 database."""
    return sqlite3.connect("stegapix.db")


def init_stegapix_table(cursor):
    """Initialize the steganography table in the db if it isn't already."""
    steg_table_spec = "Stegapix(Id INTEGER PRIMARY KEY, URL TEXT)"
    cursor.execute("CREATE TABLE IF NOT EXISTS {0};".format(steg_table_spec))


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
