"""
Joshua
CS 30 Period 1
March 30, 2023
This is file with functions for Joshua_Liu_Map.py
"""

from random import *
import pickle
import time
import threading


engage = False


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
    ROOM_LEGEND = [["Index", "Your starting location!"],
                            ["Treasure Room", "A room with booty!"],
                            ["Trap Room", "ITS A TRAP!"], ["Monster Room", "Run in circles! Your life depends on it!"],
                            ["Regular Room", "Boring"], ["Boss", "R.I.P"],
                            ["Exit", "Tataaa!"]]

    """
    Function for creating a random map
    """

    def generate_map(self):
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

    def create_rooms(self):
        x = 0
        y = 0
        worlb = []
        worlbcpy = [[None]]
        while y < MapModules.height:
            while x < MapModules.length:
                # map[y].append(None)
                # map[y][x] = Room(MapModules.ROOM_LEGEND[MapModules.room[y][x]], [x, y])
                worlb.append(Room(MapModules.ROOM_LEGEND[MapModules.room[y][x]], [x, y]))
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


class Room:
    def __init__(self, roomtype, pos):
        self.roomtype = roomtype
        self.first = True
        self.enemie = 0
        self.enemylist = []
        self.pos = pos
        self.inroom = True

    def leave(self):
        self.inroom = False

    def enter(self):
        self.inroom = True
        print("Bruh")
        print(self.roomtype)
        global engage
        if self.first is True:
            if self.roomtype[0] == "Monster Room":
                print("Entering monster room")
                EnemyMovement.pool.append(Enemy(GameModules.ENEMIES[GameModules.ENEMIESLIST[randint(0, 4)]], [self.pos[1], self.pos[0]]))
                engage = True
            elif self.roomtype[0] == "Boss Room":
                print("Entering boss room")
                EnemyMovement.pool.append(Enemy(GameModules.BOSS[GameModules.BOSSLIST[randint(0, 3)]], [self.pos[1], self.pos[0]]))
                engage = True
            elif self.roomtype[0] == "Trap Room":
                return
            elif self.roomtype[0] == "Regular Room" or self.roomtype == "Index Room":
                return
            elif self.roomtype[0] == "Treasure Room":
                return
            elif self.roomtype[0] == "Exit":
                return
            else:
                return
        else:
            return

class EnemyMovement:
    pool = []

    def __init__(self):
        EnemyMovement.pool = []
        # self.activated = False
        self.engaged = None
        self.ticks = 0
        threading.Thread(target=self.main).start()

    def main(self):
        global engage
        while True:
            while engage is False:
                time.sleep(3)
                self.counter()
            while engage is True:
                self.counter(self.engaged)

    def counter(self, eenemy=None):
        if eenemy is None:
            if len(EnemyMovement.pool) == 0:
                pass
            else:
                EnemyMovement.pool[self.ticks].action()
                self.ticks += 1
        else:
            eenemy.action()

class Enemy:
    def __init__(self, stats, position):
        self.stats = stats
        print(type(self.stats))
        self.position = position
        self.actions = ["Attack", "Defend", "Heal", "Move"]
        self.hp = stats["HP"]
        self.actions = stats["Actions"]
        self.Damage = stats["Damage"]
        self.activated = True

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
        print(type(self.stats))
        self.actions = ["Attack", "Super Attack", "Heal", "Defend", "Move"]
        # self.hp = stats["HP"]
        # self.actions = stats["Actions"]
        # self.Damage = stats["Damage"]
        self.activated = True

    def action(self):
        move = self.actions[randint(0, 5)]
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
    ENEMIESLIST = ["Goblina", "talking ben", "Jesse", "Mr. White", "Anomaly"]
    BOSSLIST = ["the Face", "the MOON", "teh epix duck", "Telamon"]
    # Constant for bosses
    BOSS = {
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
#        GameModules.ENEMIESLIST = ["Goblina", "talking ben", "Jesse", "Mr. White", "Anomaly"]
#        GameModules.BOSSLIST = ["the Face", "the MOON", "teh epix duck", "Telamon"]
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