#!/usr/bin/env python

from io import BytesIO

from PIL import Image
import requests
import sqlite3

import google_image_search as google_search

message_image_term = "snow the rapper"
veil_image_term = "snow"
local_message_image_name = "LOCAL_STEG"


def init_stegapix_table(cursor):
    """Initialize the steganography table in the db if it isn't already."""
    print("CREATE TABLE")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Stegapix(Id INTEGER PRIMARY KEY, URL TEXT);")


def is_image_in_db(cursor, image_url):
    """Test that we have an image with the same URL in the database."""
    cursor.execute("SELECT URL FROM Stegapix WHERE URL=:URL",
                   {"URL": image_url})
    return cursor.fetchone() is not None


def extract_search_items(json_data):
    """Extract search items from JSON data."""
    return json_data["items"]


def generate_candidate_image_object():
    """Generate candidate image, possibly one we've seen already."""
    search_index = 1
    # while True:
    while search_index < 3:
        json_result = google_search.get_json_results(message_image_term)
        for image_object in extract_search_items(json_result):
            image_object_digest = {}
            image_object_digest["link"] = image_object["link"]
            image_object_digest["height"] = image_object["image"]["height"]
            image_object_digest["width"] = image_object["image"]["width"]
            yield image_object_digest
        search_index += 1


def get_next_image(cursor):
    """Return next message image result we haven't seen before.

    For the sake of simplicity, we're assuming that if we've seen an
    image at a given URL before, we've seen the image, i.e. we assume
    nobody ever replaces an image at a URL. Not always true of course,
    but we are being idealistic.

    """
    image_generator = generate_candidate_image_object()
    next_image = next(image_generator)
    while is_image_in_db(cursor, next_image["link"]):
        next_image = next(image_generator)
    return next_image


def get_response_mime_type(response):
    """Get GET response MIME type."""
    return response.headers["Content-Type"].split("/")


def is_valid_image(response):
    """Validate request (make sure it has an image Content-Type)"""
    return get_response_mime_type(response)[0] == "image"


def download_image(image_url):
    """Download image at argument URL, return the filename if successful."""
    response = requests.get(image_url)
    if response.status_code == requests.codes.ok and is_valid_image(response):
        extension = get_response_mime_type(response)[1]
        file_name = "STEG_IMAGE." + extension
        Image.open(BytesIO(response.content)).save(file_name)
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
        image_object = get_next_image(cursor)
        image_url = image_object["link"]
        image_file_name = download_image(image_url)
        add_image_to_db(cursor, image_url)


def main():
    grab_new_image()

if __name__ == "__main__":
    main()
