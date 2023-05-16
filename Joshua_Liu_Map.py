"""
Joshua
CS 30 Period 1
May 14, 2023
This file contains the module for the game map
and the method for movement
"""
from Joshua_Liu_Enemy import Enemy, Boss
import Joshua_Liu_Enemy
from random import *


class GameMap:
    def __init__(self, character, enemymovement):
        self.character = character
        self.DIRECTION = ["forward", "right", "left", "back"]
        self.length = randint(4, 6)
        self.height = randint(4, 6)
        self.data = self.generate_map()
        self.layoutmap = self.data[0]
        self.initpos = self.data[1]
        self.enemymovement = enemymovement
        self.roommap = self.create_rooms()
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

    def generate_map(self):
        """Function for creating a random map"""
        x = 0  # x-coordinate for map
        y = 0  # y-coordinate for map
        room = [  # Creating the room layout variable
            [randint(1, 5)]
        ]
        # Populating the map with rooms
        while x < self.height:
            while y < self.length:
                # Creating new row for more rooms
                room[x].append(randint(1, 5))
                y += 1
            room.append([randint(1, 5)])  # adding a new row
            y = 0  # reset y
            x += 1  # increment x
        room.pop(-1)  # delete superfluous room
        # create index cood
        player_start = randint(0, self.length - 1)
        room[0][player_start] = 0  # creating a starting room
        # creating an exit room
        room[x - 1][randint(0, self.length - 1)] = 6
        self.character.pos = [player_start, 0]
        data = [room, self.character.pos]
        return data

    def create_rooms(self):
        """
        Method for creating map but with room objects
        rather than integers representing rooms
        """
        ROOM_LEGEND = [
            ["Index", "Your starting location!"],
            ["Treasure Room", "A room with booty!"],
            ["Trap Room", "ITS A TRAP!"],
            ["Monster Room", "Run in circles! Your life depends on it!"],
            ["Regular Room", "Boring"], ["Boss Room", "R.I.P"],
            ["Exit Room", "Tataaa!"]]
        x = 0
        y = 0
        worlb = []
        worlbcpy = [[None]]
        while y < self.height:
            while x < self.length:
                worlb.append(Rooms(
                    ROOM_LEGEND[self.layoutmap[y][x]],
                    [x, y], self.character, self.enemymovement))
                x += 1
            if y == 0:
                worlbcpy[0] = worlb
            else:
                worlbcpy.append(None)
                worlbcpy[y] = worlb
            worlb = []
            y += 1
            x = 0
        type(worlb)
        return worlbcpy

    def move(self):
        """Method for handling player movement"""
        x = 0  # Variable for loop
        # User input loop
        while x == 0:
            print("What do you want to do?")
            # Copy of DIRECTION list with only valid input
            temp = self.DIRECTION[::]
            # Remove invalid dirctions
            if self.character.pos[0] == 0:
                temp.remove("left")
            if self.character.pos[0] == self.length - 1:
                temp.remove("right")
            if self.character.pos[1] == self.height - 1:
                temp.remove("forward")
            if self.character.pos[1] == 0:
                temp.remove("back")
            # Getting user input on direction
            print("Your options are the following:")
            for direction in temp:
                print(direction)
            print("Enter 'quit' to exit this menu")
            print("What will you choose?")
            choice = input()
            # check if choice is valid
            if choice not in temp and not choice == "quit":
                print("invalid choice")
            elif "quit" in choice:
                # does not exit game, brings user back to previous menu
                x = 1
            else:
                self.roommap[self.character.pos[1]]\
                    [self.character.pos[0]].leave()
                x = 1  # breaking loop this way
                # Seeing what action user chose
                if choice == "forward":
                    self.character.pos[1] += 1
                elif choice == "right":
                    self.character.pos[0] += 1
                elif choice == "left":
                    self.character.pos[0] -= 1
                elif choice == "back":
                    self.character.pos[1] -= 1
        # Trigger room enter events
        self.roommap[self.character.pos[1]]\
            [self.character.pos[0]].enter()
        # Set player's current room as this room
        self.character.room = \
            self.roommap[self.character.pos[1]]\
            [self.character.pos[0]]

    def trap(self):
        """
        Method for handling traps
        """
        if randint(1, 7) == randint(1, 7):  # Dice roll for trap
            print("You got hit by a trap!")
            self.character.take_damage(randint(1, 2))

    def exitgame(self):
        """
        Method for handling win condition
        """
        if "Key" in self.character.inventory:
            print("Congratulations! You won!!!")
            print("Now get outta here")
            quit()
        else:
            print("You are missing something. Now go look for it.")


class Rooms:
    def __init__(self, roomtype, pos, character, enemymovement):
        self.first = True
        self.roomtype = roomtype
        self.pos = pos
        self.items = []
        self.character = character
        self.inroom = False
        self.enemymovement = enemymovement
        self.enemie = None  # Enemy in room
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
        """
        Method for handling traps
        """
        if randint(1, 7) == randint(1, 7):  # Dice roll for trap
            print("You got hit by a trap!")
            self.character.take_damage(randint(1, 2))

    def exitgame(self):
        """
        Method for handling win condition
        """
        if "Key" in self.character.inventory:
            print("Congratulations! You won!!!")
            print("Now get outta here")
            quit()
        else:
            print("You are missing something. Now go look for it.")

    def leave(self):
        """
        Method for handling leaving room
        """
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
                    treasure = randint(0, 4)  # index in list
                    itemlist = []  # list of spawnable items
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
