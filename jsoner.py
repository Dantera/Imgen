#!usr/bin/py

"""

"""

import json


def load_from_file(file):

    """

    Args:
        file ():

    Returns:
        (Dictionary): the data from the file

    """
    with open(file) as json_data:
        return json.load(json_data)


def save_to_file(data, file, pretty_print=False):
    """

    Args:
        data (Dictionary): the JSON data to save to file
        file (String): name of file to save
        pretty_print (boolean): whether to pretty print data to file or single

    Returns:
        None

    """
    with open(file, 'w') as output:
        if pretty_print:
            json.dump(data, output, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            json.dump(data, output)
