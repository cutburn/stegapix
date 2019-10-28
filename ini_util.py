#!/usr/bin/env python

"""Very small module that just handles pulling auth info out of
settings.ini file in the root directory of this project."""

import configparser


def get_ini_setting(section, setting):
    """Get a named setting from the specified section of settings.ini."""
    try:
        config_parser = configparser.ConfigParser()
        config_parser.read("settings.ini")
        return config_parser.get(section, setting)
    except configparser.NoOptionError:
        print("ERROR: Could not parse settings.ini file")
        exit(1)
