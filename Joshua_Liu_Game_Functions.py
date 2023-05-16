"""
Joshua
CS 30 Period 1
March 30, 2023
This is file with functions for Joshua_Liu_Game.py
"""

import pickle


class GeneralModules:
    """Class containing general file I/O methods"""

    @staticmethod
    def write_to_file(file, content):
        """Function to write to file in wb mode for pickling"""
        with open(file, "wb") as fd:
            pickle.dump(content, fd)  # serializing content
        return

    @staticmethod
    def read_to_file(file):
        """
        Function to read from file in either r or rd mode
        to support reading pickled data
        """
        with open(file, "rb") as fd:
            content = pickle.load(fd)  # deserializing content
        return content
