"""
Joshua
CS 30 Period 1
March 30, 2023
This is file with functions for Joshua_Liu_Game.py
"""

from random import *
import pickle

# Variable checking if enemy is engaged in combat or not
engage = False
# Constant for all possible rooms
ROOM_LEGEND = [
    ["Index", "Your starting location!"],
    ["Treasure Room", "A room with booty!"],
    ["Trap Room", "ITS A TRAP!"],
    ["Monster Room", "Run in circles! Your life depends on it!"],
    ["Regular Room", "Boring"], ["Boss Room", "R.I.P"],
    ["Exit Room", "Tataaa!"]]
# Constant for all possible items
ITEMS = {
            "Regular Sword": {
                "Desc": "Simple steel",
                "Dmg": 3
            },
            "Shield": {
                "Desc": "Simple wood",
            },
            "Gilgamesh": {
                "Desc": ":gilgamesh:",
                "Dmg": 40
            },
            "Jerma": {
                "Desc": "Unleash destruction upon your foes",
                "Dmg": 15
            },
            "Omega Energy Sword": {
                "Desc": "Super damage!",
                "Dmg": 10
            },
            "Key": {
                "Desc": "But what does it sayyyyyyy?!?!",
            },
            "Fists": {
                    "Desc": "Good ol fist cuffs",
                    "Dmg": 2
                },
        }


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


class GameModules:
    """
    Class for giving Joshua_Liu_Game_Functions access to some
    of the main file's objects.
    """

    player_pos = None   # Variable for player position
    # Constant list of enemies
    ENEMIESLIST = ["Goblina", "talking ben", "Jesse",
                   "Mr. White", "Anomaly"]
    # Constant list of bosses
    BOSSLIST = ["the FACE", "the MOON", "teh epix duck", "Telamon"]
    # Constant for bosses
    BOSS = {
        "the FACE": {
            "HP": 7,
            "Actions": ["Bite"],
            "Damage": 7
        },
        "the MOON": {
            "HP": 12,
            "Actions": ["Roll"],
            "Damage": 3
        },
        "teh epix duck": {
            "HP": 25,
            "Actions": ["Quack"],
            "Damage": 6
        },
        "Telamon": {
            "HP": 20,
            "Actions": ["Stab"],
            "Damage": 2
        }
    }
    # Constant for enemies
    ENEMIES = {
        "Goblina": {
            "HP": 3,
            "Actions": ["Swing"],
            "Damage": 2
        },
        "talking ben": {
            "HP": 1,
            "Actions": ["Talk"],
            "Damage": 2
        },
        "Jesse": {
            "HP": 5,
            "Actions": ["Cook"],
            "Damage": 3
        },
        "Mr. White": {
            "HP": 6,
            "Actions": ["Cook"],
            "Damage": 1
        },
        "Anomaly": {
            "HP": 3,
            "Actions": ["Scream"],
            "Damage": 5
        }
    }

    def __init__(self, character):
        # Class variable for player position
        GameModules.player_pos = [0, 0]
        # Constant for directions
        self.DIRECTION = ["forward", "right", "left", "back"]
        # Constant for rooms
        self.ROOM_LEGEND = ROOM_LEGEND
        # Constant for items available
        self.ITEMS = ITEMS
        # Player object
        self.character = character

    def check_inv(self):
        """Function for printing player inventory"""
        print(f"You have {len(self.character.inventory)} "
              f"items in your inventory")
        if len(self.character.inventory) != 0:
            for item in self.character.inventory:
                print(f"You have a {item}")
