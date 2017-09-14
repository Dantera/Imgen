#!usr/bin/py

"""

"""

import time
import json
import os
from PIL import Image, ImageDraw, ImageFont
import randomart_x
#from jsonschema import validate


# ----- CONSTANTS

VERBOSE = True

SCHEMA = {}

WRITE_TO_FILE = True


# ----- FUNCTIONS

def output(string):
    """

    this function prints to screen only if VERBOSE is engaged

    Args:
        string (String): the string to print to screen

    Returns:
        None

    """
    if VERBOSE:
        print(string)


def output_(string):
    """
    this function prints to screen without the new line character
    and only if VERBOSE  is engaged

    Args:
        string (String): the string to print to screen

    Returns:
        None

    """
    if VERBOSE:
        print(string, end='')
    return


def leading_chars(string, length=3, char='0'):
    """

    Args:
        string (string): the string to verify length and prepend if necessary
        length (int): how long the string is to be
        char (char): the character to use as filler

    Returns:
        (string): string that is assured to be at least desired length whether modified or not

    ACTION: adds leading chars to the string if shorter than the desired length

    """
    return '{s:{c}{l}}'.format(s = string, c = char, l = length)


def get_now():
    """

    Args:
        None

    Returns:
        (String): current time as ##:##:##

    """
    return time.strftime("%H:%M:%S", time.gmtime())


def get_filename(file):
    """

    Args:
        file (String): filename with extension

    Returns:
        (String): path with os appropriate directory separator and the file

    """
    return os.path.join('images', file)


def get_dimensions(dimensions):
    """

    Args:
        dimensions (Dictionary): Dictionary of width (int), height (int)

    Returns:
        (Tuple): [int, int]

    """
    return dimensions['width'], dimensions['height']


def get_rgba(rgba):
    """

    Args:
        data (Dictionary): Dictionary of red (int), green (int), blue (int), alpha (int)

    Returns:
        (Tuple): [int, int, int, int]

    """
    return rgba['red'], rgba['green'], rgba['blue'], rgba['alpha']


def get_coordinates(coordinates):
    """

    Args:
        coordinates (Dictionary): Dictionary of x (int), y (int)

    Returns:
        (Tuple): [int, int]

    """
    return coordinates['x'], coordinates['y']


def gen_image(data):
    """

    Args:
        data (Dictionary): Dictionary of data

    Returns
        image (Image): Image containing text with a transparent background

    """
    mode = data['mode']
    dimensions = get_dimensions(data['dimensions'])
    if 'randomart' in data['color'].keys():
        image = gen_random_art(dimensions)
    else:
        rgba = get_rgba(data['color'])
        image = Image.new(mode, dimensions, rgba)
    return image


def gen_text(data):
    """

    Args:
        data (Dictionary): Dictionary of data

    Returns:
        image(Image): an image containing text with a transparent background

    """
    mode = data['mode']
    dimensions = get_dimensions(data['dimensions'])
    text = data['text']
    content = text['content']
    rgba = get_rgba(text['color'])
    coordinates = get_coordinates(text['coordinates'])
    text_image = Image.new(mode, dimensions, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_image)
    image_font = ImageFont.truetype(os.path.join('fonts', text['font']), text['size'])
    image_draw.text(coordinates, content, font=image_font, fill=rgba)
    return text_image


def gen_thumbnail(image, dimensions):
    """

    Args:
        image (Image):
        dimensions (Tuple): contains two integers of width of height

    Returns:
        thumbnail (Image): a resized thumbnail version of the original image

    """
    thumbnail = image.copy()
    thumbnail.thumbnail(dimensions)
    return thumbnail


def gen_random_art(data):
    width, height = data
    image = randomart_x.gen_randomart(width, height)
    return image


def clear_workspace():
    output('CLEARING WORKSPACE')
    root_path = 'images'  # MAKE A GLOBAL CONSTANT
    try:
        file_list = os.listdir(root_path)
        for file_name in file_list:
            output(file_name)
            os.remove(os.path.join(root_path, file_name))
    except:
        print('ERROR: unable to clear workspace')  # HANDLE MULTIPLE ERRORS INSTEAD OF GENERIC


def overlay_text(image, text):
    try:
        return Image.alpha_composite(image, text)
    except Exception:
        print('ERROR: could not composite text on image')
        return image


def save_file(file, file_path):
    output('CREATING FILE: ' + file_path)
    if WRITE_TO_FILE:
        try:
            file.save(file_path)
            #return True
        except IOError:
            print('ERROR: could not create file "{0}"'.format(file_path))
            #return False


# ----- VARIABLES


# ----- MAIN
output('READY')

time_start = get_now()
print(time_start)

# PROCESSING DATA
output('PROCESSING DATA')
# DATA
with open('image_data.json') as json_data:
    images = json.load(json_data)

"""
# VALIDATE JSON DATA AGAINST SCHEMA
try:
    validate(json_data, SCHEMA)
except Exception:
    print('ERROR: JSON data did not validate against Schema')
    exit()
"""

# IF THERE IS NO IMAGE DATA, END PROGRAM
if len(images) == 0:
    print('ERROR: no image data in JSON')
    exit()

# CLEAR WORKSPACE
clear_workspace()

# CREATE IMAGES
output('CREATING IMAGES')
for data in images:

    # IMAGE
    image = gen_image(data)

    # TEXT
    output('TEXT: ')

    if 'text' in data.keys():
        output('YES')
        text = gen_text(data)
        image = overlay_text(image, text)
    else:
        output('NO')

    # FILE
    file_path = os.path.join('images', data['filename'] + data['extension'])
    save_file(image, file_path)

    # THUMBNAIL
    output_('THUMBNAIL: ')

    if 'thumbnail' in data.keys():
        output('YES')
        thumbnail = gen_thumbnail(image, get_dimensions(data['thumbnail']['dimensions']))
        # FILE
        file_path = os.path.join('images', data['thumbnail']['filename'] + data['extension'])
        save_file(thumbnail, file_path)
    else:
        output('NO')

output('FINISHED')
time_end = get_now()

print('DURATION ' + time_start + ' - ' + time_end)
