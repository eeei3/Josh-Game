"""
Joshua
CS 30 Period 1
March 30, 2023
This is file with functions for Joshua_Liu_Game.py
"""

from random import *
import pickle


class GeneralModules:
    """
    Class containing general file I/O methods
    """

    @staticmethod
    def write_to_file(file, content):
        """
        Function to write to file in wb mode for pickling
        """
        with open(file, "wb") as fd:
            pickle.dump(content, fd)  # serializing content
        return

    @staticmethod
    def read_to_file(file, mode):
        """
        Function to read from file in either r or rd mode
        to support reading pickled data
        """
        with open(file, "rb") as fd:
            if mode == "reload":
                fd.seek(0)
                # deserializing content
                content = pickle.load(fd)
            else:
                content = fd.read()
        return content
