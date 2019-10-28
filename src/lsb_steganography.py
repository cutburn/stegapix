#!/usr/bin/env python

"""This was written as a proof-of-concept of the data obscuration
technique referred to as LSB steganography, in which data (in the case
of this module, color data for an image of similar dimensions) can be
hidden in the LSBs (Least Significant Bits) of a "veil" image, and can
likewise decode the steganographized image.

For more information on digital steganography:
http://en.wikipedia.org/wiki/Steganography#Digital

"""

from optparse import OptionParser
import os
import sys

from PIL import Image

NORMALIZATION_FACTOR = 255
NUM_LSBS = 2
LSB_MASK = int((NUM_LSBS * '1'), 2)


def handle_args():
    """Parse args and perform actions, or else exit with status 1."""
    
    parser = OptionParser(usage="usage: %prog [options] filename")
    parser.add_option(
        "-m", "--mode", dest="mode", help="'s' or 'steg' to steganographize, "
        "'u' or 'unsteg' to unsteganographize")
    options, args = parser.parse_args()
    
    STEG_MODE, UNSTEG_MODE = 0, 1
    mode_str = options.mode
    if not mode_str:
        parser.error("Please specify a mode.")
    else:
        if mode_str == "s" or mode_str == "steg":
            mode = STEG_MODE
        elif mode_str == "u" or mode_str == "unsteg":
            mode = UNSTEG_MODE
        else:
            print("ERROR: Please enter a valid mode value.")
            exit(1)

    if mode == STEG_MODE:
        if len(args) is not 2:
            parser.error("Please specify exactly two filenames as arguments.")
        elif not os.path.isfile(args[0]) or not os.path.isfile(args[1]):
            print("ERROR: Please specify filenames of existing files.")
            exit(1)
        else:
            # Success case
            veil_filename, message_filename = args[0], args[1]
            steganographize(veil_filename, message_filename)
    elif mode == UNSTEG_MODE:
        if len(args) is not 1:
            parser.error("Please specify exactly one filename as an argument.")
        elif not os.path.isfile(args[0]):
            print("ERROR: Please specify the filename of an existing file.")
            exit(1)
        else:
            # Success case
            steg_filename = args[0]
            unsteganographize(steg_filename)


def steganographize(veil_image_path, message_image_path):
    """Steganographize and save a message image using a veil image.

    Replace the LSBs of the veil image and with the pixel data of the
    message image, renormalized to the range of values the LSBs can
    represent.

    Args:
        veil_image_path (str): location of veiling image
        message_image_path (str): location of message image
    Returns:
        Filename of the steganographized file.

    """
    veil = Image.open(veil_image_path)
    veil_data = veil.getdata().convert("RGB")
    message = Image.open(message_image_path)
    message_data = message.getdata().convert("RGB")
    steg = Image.new(veil.mode, veil.size, 'white')
    steg_data = []

    for i in range(0, len(veil_data)):
        steg_data.append(encode_tuple(veil_data[i], message_data[i]))

    steg.putdata(steg_data)
    steg_file_name = veil_image_path[:-4] + '.steg.png'
    steg.save(steg_file_name)
    return steg_file_name


def encode_tuple(veil_pixel, message_pixel, norm_factor=NORMALIZATION_FACTOR):
    """Pack message_pixel pixel data into the LSBs of a pixel tuple.

    Args:
        veil_pixel: A pixel tuple from the veil image
        message_pixel: A pixel tuple from the message image

    """
    steg = list(veil_pixel)
    for i in range(0, len(steg)):
        LSBs = int(float(message_pixel[i]) * LSB_MASK / norm_factor)
        steg[i] = ((steg[i] >> NUM_LSBS) << NUM_LSBS) | LSBs

    return tuple(steg)


def unsteganographize(steg_path):
    """Unsteganographize and save an image.

    By "unpacking" LSBs and re-normalizing them to the 0-norm_factor
    range.

    Args:
        steg_path (str): location of steganographized image

    """
    steg = Image.open(steg_path)
    steg_data = steg.getdata()
    unsteg = Image.new(steg.mode, steg.size, 'white')
    unsteg_data = []
    for i in range(0, len(steg_data)):
        unsteg_data.append(decode_tuple(steg_data[i]))

    unsteg.putdata(unsteg_data)
    unsteg.save(steg_path[:-4] + '.unsteg.png')


def decode_tuple(steg_pixel, norm_factor=NORMALIZATION_FACTOR):
    """Unpack LSBs of pixel data from a steganographized pixel tuple.

    Args:
        steg_pixel (tuple): A pixel tuple

    """
    unsteg_values = []
    for elem in steg_pixel:
        unsteg_values.append(int(norm_factor * (elem & LSB_MASK) / LSB_MASK))
    return tuple(unsteg_values)


def main():
    handle_args()

if __name__ == "__main__":
    main()
