#!/usr/bin/env python

""" TODO make explanation here """

import sys
import os

__author__ = "Lukas Rønsholt"
__credits__ = []
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Lukas Rønsholt"
__email__ = "lukasronsholt@gmail.com"
__status__ = "Development"


def print_download_complete(name):
    msg = 'Torrent: ' + name + ' finished downloaded!'
    os.system('wall ' + msg)


def move_file(src, dst):
    os.system('ln -s ' + src + ' ' + dst)


def main(argv):
    new_location = None
    file_name = argv[0]
    category = argv[1]
    location = argv[2]
    movie_location = argv[3]
    show_location = argv[4]

    if category == 'Movie':
        new_location = movie_location + file_name
    elif category == 'Show':
        new_location = show_location + file_name

    if new_location is not None:
        move_file(location, new_location)
        print_download_complete(file_name)


if __name__ == '__main__':
    main(sys.argv[1:])
