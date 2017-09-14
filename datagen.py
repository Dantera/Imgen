#!usr/bin/py

import json
import random
import time

military_phonetic_alphabet = [
    'alpha',
    'bravo',
    'charlie',
    'delta',
    'echo',
    'foxtrot',
    'golf',
    'hotel',
    'indian',
    'juliet',
    'kilo',
    'lima',
    'mike',
    'november',
    'oscar',
    'papa',
    'quebec',
    'romeo',
    'sierra',
    'tango',
    'uniform',
    'victor',
    'whiskey',
    'x-ray',
    'yankee',
    'zulu'
]

colors = [
    'red',
    'lime',
    'blue',
    'yellow',
    'cyan',
    'magenta',
    'silver',
    'gray',
    'maroon',
    'olive',
    'green',
    'purple',
    'teal',
    'navy',
    'black',
    'white'
]

# http: # www.rapidtables.com / web / color / RGB_Color.htm
rgbs = {
    "red": [255, 0, 0],
    "lime": [0, 255, 0],
    "blue": [0, 0, 255],
    "yellow": [255, 255, 0],
    "cyan": [0, 255, 255],
    "magenta": [255, 0, 255],
    "silver": [192, 192, 192],
    "gray": [128, 128, 128],
    "maroon": [128, 0, 0],
    "olive": [128, 128, 0],
    "green": [0, 128, 0],
    "purple": [128, 0, 128],
    "teal": [0, 128, 128],
    "navy": [0, 0, 128],
    "black": [0, 0, 0],
    "white": [255, 255, 255]
}

layouts = [
    'portrait',
    'landscape'
]

dimensions = {
    "portrait": [300, 500],
    "landscape": [500, 300],
    "portrait_thumbnail": [90, 150],
    "landscape_thumbnail": [150, 90]
}

# file name format: name_number[_thumbnail}.extension
# example alpha_001.jpg, alpha_001_thumbnail.jpg


def get_now():
    """

    Args:
        None

    Returns:
        (String): current time as ##:##:##

    """
    return time.strftime("%H:%M:%S", time.gmtime())


def gen_font(file, size):
    return {
        "file": file,
        "size": size
    }


def gen_coordinates(x, y):
    return {
        "x": x,
        "y": y
    }


def gen_color(color):
    return {
        "red": color[0],
        "green": color[1],
        "blue": color[2],
        "alpha": 255
    }


def gen_dimensions(dimensions, layout):
    return {
        "width": dimensions[0],
        "height": dimensions[1]
    }


def go_do():

    extension = '.png'
    images = []

    for i in range(len(military_phonetic_alphabet)):
    
        # number_of_images = random(0, colors.length-1)
    
        for j in range(len(colors)):
    
            image = {}

            image['filename'] = military_phonetic_alphabet[i] + '_' + str(j)

            image['extension'] = extension

            image['mode'] = 'RGBA'

            layout = layouts[random.randrange(0, len(layouts)-1)]
            image['layout'] = layout
            image['dimensions'] = gen_dimensions(dimensions[layout], layout)

            color = colors[j]  # colors[random.randrange(0, len(colors) - 1)]
            image['color'] = gen_color(rgbs[color])
            image['color'].update({'randomart':True})

            # make text a contrasting color
            image['text'] = {
                "font": 'Roboto-Regular.ttf',
                "size": 20,
                "color": gen_color(rgbs['white']),
                "content": military_phonetic_alphabet[i],
                "coordinates": gen_coordinates(0, 0)
            }

            # getThumbnail(filename, extension, layout)
            image['thumbnail'] = {
                "filename": image['filename'] + '_thumbnail',
                "extension": extension,
                "dimensions": gen_dimensions(dimensions[layout + '_thumbnail'], layout)
            }

            images.append(image)
        # // end for
    
    # end for
    
    return images


PRETTY_PRINT_JSON = True

print(get_now())

data = go_do()
with open('image_data.json', 'w') as outfile:
    if PRETTY_PRINT_JSON:
        json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        json.dump(data, outfile)
#print(len(data), ' images')
print(json.dumps(data))

print(get_now())