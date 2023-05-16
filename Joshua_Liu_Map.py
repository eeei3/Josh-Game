"""
Joshua
CS 30 Period 1
May 14, 2023
This file contains the module for the Game map
"""
from Joshua_Liu_Rooms import *
from random import *


class GameMap:
    """ Class for handling game map and movement"""

    def __init__(self, character, enemymovement):
        # Object for the player
        self.character = character
        # Constant for list of possible movement directions
        self.DIRECTION = ["forward", "right", "left", "back"]
        # Length of map
        self.length = randint(4, 6)
        # Height of map
        self.height = randint(4, 6)
        # Map Data
        self.data = self.generate_map()
        # Map with numbers representing rooms
        self.layoutmap = self.data[0]
        # Player initial position
        self.initpos = self.data[1]
        # Object for enemy movement
        self.enemymovement = enemymovement
        # Map with objects representing rooms
        self.roommap = self.create_rooms()
        # Constant for items
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
        # Setting character spawn point
        self.character.pos = [player_start, 0]
        # Putting all important data into a nice list
        data = [room, self.character.pos]
        return data

    def create_rooms(self):
        """
        Method for creating map but with room objects
        rather than integers representing rooms
        """
        # Constant for list of Rooms
        ROOM_LEGEND = [
            ["Index", "Your starting location!"],
            ["Treasure Room", "A room with booty!"],
            ["Trap Room", "ITS A TRAP!"],
            ["Monster Room", "Run in circles! Your life depends on it!"],
            ["Regular Room", "Boring"], ["Boss Room", "R.I.P"],
            ["Exit Room", "Tataaa!"]]
        # x-y coordinates
        x = 0
        y = 0
        # A list for a row of rooms
        worlb = []
        # A list for all the rooms
        worlbcpy = [[None]]
        while y < self.height:
            while x < self.length:
                # Adding room to row
                worlb.append(Rooms(
                    ROOM_LEGEND[self.layoutmap[y][x]],
                    [x, y], self.character, self.enemymovement))
                x += 1
            if y == 0:
                # Setting index value as row
                worlbcpy[0] = worlb
            else:
                # Adding row to world
                worlbcpy.append(None)
                worlbcpy[y] = worlb
            # Emptying worlb
            worlb = []
            y += 1
            x = 0
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
        """Method for handling traps"""
        if randint(1, 7) == randint(1, 7):  # Dice roll for trap
            print("You got hit by a trap!")
            self.character.take_damage(randint(1, 2))

    def exitgame(self):
        """Method for handling win condition"""
        if "Key" in self.character.inventory.inventory:
            print("Congratulations! You won!!!")
            print("Now get outta here")
            quit()
        else:
            print("You are missing something. Now go look for it.")
