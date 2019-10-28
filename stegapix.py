#!/usr/bin/env python

"""This module leverages the functionality of the standalone
lsb_steganography module with a Google Custom Search Engine API
crawler to post steganographized images of "snow", with hidden images
of "snow the rapper" - usually Darrin Kenneth O'Brien, the man made
famous in the 90s by the song "Informer", but as I learned from the
search results there's also an artist by the name of"Snow tha Product"
that comes up a lot instead.

"""

from io import BytesIO
import os

from PIL import Image
import requests
import sqlite3

import google_image_search as google_search
import lsb_steganography as lsb_steg
import image_posting

message_image_term = "snow the rapper"
veil_image_term = "snow"
local_message_image_name = "LOCAL_STEG"


def init_stegapix_table(cursor):
    """Initialize the steganography table in the db if it isn't already."""
    steg_table_spec = "Stegapix(Id INTEGER PRIMARY KEY, URL TEXT)"
    cursor.execute("CREATE TABLE IF NOT EXISTS {0};".format(steg_table_spec))


def is_image_in_db(cursor, image_url):
    """Test that we have an image with the same URL in the database."""
    cursor.execute("SELECT URL FROM Stegapix WHERE URL=:URL",
                   {"URL": image_url})
    return cursor.fetchone() is not None


def extract_search_items(json_data):
    """Extract search items from JSON data."""
    return json_data["items"]


def generate_candidate_image_object(image_term):
    """Generate candidate image, possibly one we've seen already."""
    search_index = 1
    while True:
        json_index = str(search_index)
        json_result = google_search.get_json_results(image_term,
                                                     start_index=json_index)
        for image_object in extract_search_items(json_result):
            image_object_digest = {}
            image_object_digest["link"] = image_object["link"]
            image_object_digest["height"] = image_object["image"]["height"]
            image_object_digest["width"] = image_object["image"]["width"]
            yield image_object_digest
        search_index += 1


def get_next_image(cursor, search_term):
    """Return next message image result we haven't seen before.

    For the sake of simplicity, we're assuming that if we've seen an
    image at a given URL before, we've seen the image, i.e. we assume
    nobody ever replaces an image at a URL. Not always true of course,
    but we are being idealistic.

    """
    image_generator = generate_candidate_image_object(search_term)
    next_image = next(image_generator)
    response = requests.get(next_image["link"])
    while (is_image_in_db(cursor, next_image["link"]) or
           response.status_code != requests.codes.ok or not
           is_valid_image(response)):
        next_image = next(image_generator)
        response = requests.get(next_image["link"])
    return next_image


def get_next_message_image(cursor):
    """Get next message image."""
    return get_next_image(cursor, message_image_term)


def get_next_veil_image(cursor, message_image):
    """Get next veil image."""
    return get_next_image(cursor, veil_image_term)


def get_response_mime_type(response):
    """Get GET response MIME type."""
    mime_type = response.headers["Content-Type"].split("/")
    if ';' in mime_type[1]:
        mime_type[1] = mime_type[1].split(";")[0]
    return mime_type


def is_valid_image(response):
    """Validate request (make sure it has an image Content-Type)"""
    mime_type = get_response_mime_type(response)
    return mime_type[0] == "image" and mime_type[1] != "gif"


def download_message_image(image_url):
    """Download message image."""
    return download_image(image_url, "MESSAGE_IMAGE")


def download_veil_image(image_url, message_image_object):
    """Download veil image and make it match size of the message image."""
    dimensions = (message_image_object["width"],
                  message_image_object["height"])
    return download_image(image_url, "VEIL_IMAGE", dimensions=dimensions)


def download_image(image_url, file_name, dimensions=None):
    """Download image at argument URL, return the filename if successful."""
    response = requests.get(image_url)
    # Note: at this point no need to check on status code or image
    # being valid, as long as not much has changed since when we last
    # checked it a few milliseconds ago
    extension = get_response_mime_type(response)[1]
    file_name = file_name + "." + extension
    image = Image.open(BytesIO(response.content))
    if dimensions is not None:
        image = image.resize(dimensions, Image.ANTIALIAS)
    image.save(file_name)
    return file_name


def add_image_to_db(cursor, image_url):
    """Add entry for an already-visited image URL to sqlite database."""
    cursor.execute("INSERT INTO Stegapix(URL) VALUES (?);", (image_url,))


def grab_new_image():
    """Download an image we haven't seen before, save it to the DB."""
    connection = sqlite3.connect("stegapix.db")
    with connection:
        cursor = connection.cursor()
        init_stegapix_table(cursor)
        message_image_object = get_next_message_image(cursor)
        message_image_url = message_image_object["link"]
        message_file_name = download_message_image(message_image_url)
        if message_file_name is not None:
            veil_image_object = get_next_veil_image(cursor,
                                                    message_image_object)
            veil_image_url = veil_image_object["link"]
            veil_file_name = download_veil_image(veil_image_url,
                                                 message_image_object)
            
            steg_file_name = lsb_steg.steganographize(veil_file_name,
                                                      message_file_name)
            add_image_to_db(cursor, message_image_url)
            add_image_to_db(cursor, veil_image_url)
            image_posting.post_image(steg_file_name)
            os.remove(message_file_name)
            os.remove(veil_file_name)
            os.remove(steg_file_name)


def main():
    grab_new_image()

if __name__ == "__main__":
    main()
