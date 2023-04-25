"""
Joshua
CS 30 Period 1
March 30, 2023
This is file with functions for Joshua_Liu_Map.py
"""

from random import *
import pickle
import threading
import concurrent.futures


"""
Class containing general file I/O methods
"""


class GeneralModules:

    """
    Function to write to file in wb mode for pickling
    """

    @staticmethod
    def write_to_file(file, content):
        with open(file, "wb") as fd:
            pickle.dump(content, fd)  # serializing content
        return

    """
    Function to read from file in either r or rd mode
    to support reading pickled data
    """
    @staticmethod
    def read_to_file(file, mode):
        with open(file, "rb") as fd:
            if mode == "reload":
                fd.seek(0)
                # deserializing content
                content = pickle.load(fd)
            else:
                content = fd.read()
        return content

    """
    Function for appending to file and append
    extra new lines. Not used
    """

    @staticmethod
    def append_to_file(file, content):
        with open(file, "a") as fd:
            fd.write("\n\n/\n\n")
            fd.write(content)
        return


"""
Class containing methods and objects relating to the map
"""


class MapModules:
    length = randint(4, 6)  # Length of room
    height = randint(4, 6)  # Width of room
    room = [  # Creating the room layout variable
        [randint(1, 5)]
    ]

    """
    Function for creating a random map
    """

    @staticmethod
    def generate_map():
        x = 0  # x-coordinate for map
        y = 0  # y-coordinate for map
        # Populating the map with rooms
        while x < MapModules.height:
            while y < MapModules.length:
                # Creating new row for more rooms
                MapModules.room[x].append(randint(1, 5))
                y += 1
            MapModules.room.append([randint(1, 5)])  # adding a new row
            y = 0  # reset y
            x += 1  # increment x
        MapModules.room.pop(-1)  # delete superfluous room
        player_start = randint(0, MapModules.length - 1)  # create index cood
        MapModules.room[0][player_start] = 0  # creating a starting room
        # creating an exit room
        MapModules.room[x - 1][randint(0, MapModules.length - 1)] = 6
        GameModules.player_pos = [player_start, 0]
        data = [MapModules.room, GameModules.player_pos]
        return data


class Map(MapModules):
    def __init__(self, map):
        self.map = map
        self.enemies = {}



class EnemyMovement:

    def __init__(self):
        self.pool = []
        self.activated = False
        self.engaged = None
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.executor.submit(self.main)

    def main(self):
        while self.activated is False:
            self.counter()
        while self.activated is True:
            self.counter(self.engaged)



    def counter(self, eenemy=None):
        if eenemy == None:
            for enemy in self.pool:
                enemy.action()
        else:
            eenemy.action()

class Enemy:
    def __init__(self, stats, position):
        self.stats = stats
        self.position = position
        self.actions = ["Attack", "Defend", "Heal", "Move"]
        self.hp = stats["HP"]
        self.actions = stats["Actions"]
        self.Damage = stats["Damage"]
        self.activated = False

    def action(self):
        move = self.actions[randint(0, 4)]
        if move == "Attack":
            print("lol")
        elif move == "Defend":
            print("rofl")
        elif move == "Heal":
            print("lmao")
        elif move == "Move":
            print("XD")

    def move(self):
        return

    def heal(self):
        return

    def attack(self):
        return

class Boss(Enemy):
    def __init__(self, stats, position):
        super().__init__(stats, position)
        self.actions = ["Attack", "Super Attack", "Heal", "Defend", "Move"]
        self.hp = stats["HP"]
        self.actions = stats["Actions"]
        self.Damage = stats["Damage"]
        self.activated = False

    def action(self):
        move = self.actions[randint(0,5)]
        self.panic()
        if move == "Attack":
            print("lol")
        elif move == "Defend":
            print("lol")
        elif move == "Heal":
            print("lmao")
        elif move == "Move":
            print("XD")
        elif move == "Super Attack":
            print("Bruh")

    def super_attack(self):
        return

    def panic(self):
        if self.hp < 1:
            self.super_attack()
            self.move()
            self.heal()


"""
Class relating to methods and objects of the actual game
"""


class GameModules:

    class Item:
        def __init__(self, stats, iskey):
            self.stats = stats
            self.iskey = iskey

        def consumekey(self):
            if self.iskey == True:
                print("You escaped!")

    player_pos = None   # Variable for player position

    def __init__(self, character):
        GameModules.player_pos = [0, 0]  # Class variable for player position
        # Constant for directions
        self.DIRECTION = ["forward", "right", "left", "back"]
        # Constant for rooms
        self.ROOM_LEGEND = [["Index", "Your starting location!"],
                            ["Treasure Room", "A room with booty!"],
                            ["Trap Room", "ITS A TRAP!"], ["Monster Room", "Run in circles! Your life depends on it!"],
                            ["Regular Room", "Boring"], ["Boss", "R.I.P"],
                            ["Exit", "Tataaa!"]]
        # Constant for items available
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
                "Dmg": 90
            },
            "Jerma": {
                "Desc": "Unleash destruction upon your foes",
                "Dmg": 35
            },
            "Omega Energy Sword": {
                "Desc": "Super damage!",
                "Dmg": 20
            },
            "Gravity Coil": {
                "Desc": "boioioioioioioioioioioinnngggg dtdtdtddt",
            },
            "Speed Coil": {
                "Desc": "vrrrrrrrrrrrrooooooooooooooom",
            },
            "Key": {
                "Desc": "But what does it sayyyyyyy?!?!",
            }
        }
        # Constant for bosses
        self.BOSS = {
            "the FACE": {
                "HP": 7,
                "Actions": ["Bite", "Block", "Parry"],
                "Damage": 7
            },
            "the MOON": {
                "HP": 12,
                "Actions": ["Roll", "Block", "Parry"],
                "Damage": 3
            },
            "teh epix duck": {
                "HP": 25,
                "Actions": ["Qauck", "Block", "Parry"],
                "Damage": 6
            },
            "Telamon": {
                "HP": 20,
                "Actions": ["Stab", "Block", "Parry"],
                "Damage": 2
            }
        }
        # Constant for enemies
        self.ENEMIES = {
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
        self.ENEMIESLIST = ["Goblina", "talking ben", "Jesse", "Mr. White", "Anomaly"]
        # Player object
        self.character = character
        self.em = EnemyMovement()

    """Printing player actions function. Prints inventory"""
    def act(self):
        print("Your available actions:")
        for item in self.ITEMS.keys():
            for thing in self.ITEMS[item].keys():
                print(f'{item}: {thing} {self.ITEMS[item][thing]}')

    """Function for printing player inventory"""
    def check_inv(self):
        print(f"You have {len(self.character['Inventory'])} items in your inventory")
        if len(self.character["Inventory"]) != 0:
            for item in self.character["Inventory"]:
                print(f"You have a {item}")

    def room(self, room, pos):
        if room == "Monster Room":
            self.em.pool.append(Enemy(self.ENEMIES[self.ENEMIESLIST[randint(0, 5)]], pos))



    """Player movement function. Moves player and determines valid input"""
    def move(self):
        x = 0
        # User input loop
        while x == 0:
            print("What do you want to do?")
            # Copy of DIRECTION list with only valid input
            temp = self.DIRECTION[::]
            # Remove invalid dirctions
            if self.character.pos[0] == 0:
                temp.remove("left")
            if self.character.pos[0] == MapModules.length - 1:
                temp.remove("right")
            if self.character.pos[1] == MapModules.height - 1:
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
                x = 1  # does not exit game, brings user back to previous menu
            else:
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
