"""
Joshua
CS 30 Period 1
May 14, 2023
This file contains the module for enemy movement
"""


class EnemyActions:
    """Class for Enemy actions"""

    def __init__(self):
        self.playeraction = False  # Is it the player's turn to move?
        self.engaged = None
        self.number = 0
        self.engage = False

    def counter(self, eenemy=None):
        """Function in charge of executing enemy action"""
        if eenemy is not None:
            eenemy.baction()