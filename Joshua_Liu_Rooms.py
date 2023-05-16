"""
Joshua
CS 30 Period 1
May 15, 2023
This file contains the module for the game rooms
"""
from Joshua_Liu_Enemy import Enemy, Boss
import Joshua_Liu_Enemy
from random import *


class Rooms:
    """Class for handling rooms inside of the map"""

    def __init__(self, roomtype, pos, character, enemymovement):
        # Checking if this is the first time player has been
        # in this room
        self.first = True
        self.roomtype = roomtype  # Type of room
        self.pos = pos  # Position of the room in the map
        self.items = []  # List of items in the room
        self.character = character  # Object for the character
        self.inroom = False  # Checking if the player is in the room
        # Object for enemy actions
        self.enemymovement = enemymovement
        self.enemie = None  # Enemy in room
        # Dictionary for all items in game
        self.ITEMS = {
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

    def trap(self):
        """Method for handling traps"""
        if randint(1, 7) == randint(1, 7):  # Dice roll for trap
            print("You got hit by a trap!")
            self.character.take_damage(randint(1, 2))

    def exitgame(self):
        """Method for handling win condition"""
        if "Key" in self.character.inventory:
            print("Congratulations! You won!!!")
            print("Now get outta here")
            quit()
        else:
            print("You are missing something. Now go look for it.")

    def leave(self):
        """Method for handling leaving room"""
        self.inroom = False  # Setting room as exited
        self.enemymovement.engaged = None  # Player no longer engaged
        self.enemymovement.engage = False  # Player is no longer engaged
        # Player no longer satisfies win condition
        if "Leave Dungeon" in self.character.actions:
            self.character.actions.remove("Leave Dungeon")

    def enter(self):
        """Method handling for when entering room"""
        self.inroom = True  # Setting player as in room
        # Is this the first time player has entered room?
        if self.first:
            self.first = False  # No longer first time
            print("\nYou have discovered a new room")
            print(f"You are now in a {self.roomtype[0]}")
            # Events for Monster Room
            if self.roomtype[0] == "Monster Room":
                # Create random enemy object
                enemyname = Joshua_Liu_Enemy.ENEMIESLIST[randint(0, 4)]
                enemy = Enemy(enemyname,
                              Joshua_Liu_Enemy.ENEMIES[enemyname],
                              [self.pos[1], self.pos[0]],
                              self.character)
                print(f"You have encountered a {enemy.name}")
                # Setting player as engaged against enemy
                self.enemymovement.engaged = enemy
                # Setting player as engaged
                self.enemymovement.engage = True
                # Setting enemy in room as this enemy
                self.enemie = enemy
            # Events for Boss Room
            elif self.roomtype[0] == "Boss Room":
                # Create random boss object
                enemyname = Joshua_Liu_Enemy.BOSSLIST[randint(0, 3)]
                enemy = Boss(enemyname,
                             Joshua_Liu_Enemy.BOSS[enemyname],
                             [self.pos[1], self.pos[0]],
                             self.character)
                print(f"You have encountered a {enemy.name}")
                # Setting player as engaged against boss
                self.enemymovement.engaged = enemy
                # Setting player as engaged
                self.enemymovement.engage = True
                # Setting enemy in room as this boss
                self.enemie = enemy
            # Events for Trap Room
            elif self.roomtype[0] == "Trap Room":
                self.trap()  # Triggering trap
            # Events for Regular and Index Room
            elif self.roomtype[0] == "Regular Room" or\
                    self.roomtype == "Index Room":
                return
            # Events for Treasure Room
            elif self.roomtype[0] == "Treasure Room":
                # Spawning treasure
                treasure = randint(0, 4)  # index in list
                itemlist = []  # list of spawnable items
                for key in self.ITEMS:
                    itemlist.append(key)
                self.items.append(itemlist[treasure])
                # Chance for a second treasure to spawn in
                if randint(0, 4) == 1:
                    treasure = randint(0, 4) # index in list
                    itemlist = [] # list of spawnable items
                    for key in self.ITEMS:
                        itemlist.append(key)
                    self.items.append(itemlist[treasure])
            # Events for Exit
            elif self.roomtype[0] == "Exit Room":
                print("\nYou feel a need to be here")
                self.character.actions.append("Leave Dungeon")
                return
        # This is NOT the first time player has been in room
        else:
            print(f"You are now in a {self.roomtype[0]}")
            # Events for Monster Room
            if self.roomtype[0] == "Monster Room":
                # Is there still an enemy here?
                if self.enemie is not None:
                    # Is the enemy dead?
                    if self.enemie.hp > 0:  # No
                        print(self.enemie.hp)
                        print(f"\nYou have encountered a "
                              f"{self.enemie.name}")
                        self.enemymovement.engaged = self.enemie
                        self.enemymovement.engage = True
                    else:  # Yes
                        del self.enemie  # Deleting enemy object
                        self.enemie = None
                else:
                    pass
            # Events for Boss Room
            elif self.roomtype[0] == "Boss Room":
                print("Entering boss room")
                if self.enemie is not None:
                    # Has the boss in the room died?
                    if self.enemie.hp > 0:  # No
                        print(self.enemie.hp)
                        print(f"\nYou have encountered a "
                              f"{self.enemie.name}")
                        self.enemymovement.engaged = self.enemie
                        self.enemymovement.engage = True
                    else:  # Yes
                        del self.enemie  # Deleting boss object
                        self.enemie = None
            # Events for Trap Room
            elif self.roomtype[0] == "Trap Room":
                self.trap()
            # Events for Regular and Index Room
            elif self.roomtype[0] == "Regular Room" or \
                    self.roomtype == "Index Room":
                return
            # Events for Treasure Room
            elif self.roomtype[0] == "Treasure Room":
                return
            # Events for Exit Room
            elif self.roomtype[0] == "Exit":
                self.character.actions.append("Leave Dungeon")
                return
