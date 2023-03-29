from random import *
import datetime
import pickle


class GeneralModules:
    @staticmethod
    def write_to_file(file, content):
        with open(file, "wb") as fd:
            pickle.dump(content, fd)
        return

    @staticmethod
    def read_to_file(file, mode):
        with open(file, "rb") as fd:
            if mode == "reload":
                fd.seek(0)
                content = pickle.load(fd)
            else:
                content = fd.read()
        return content

    @staticmethod
    def append_to_file(file, content):
        with open(file, "a") as fd:
            fd.write("\n\n/\n\n")
            fd.write(content)
        return


class MapModules:

    length = randint(4, 6)  # Length of room
    height = randint(4, 6)  # Width of room
    room = [  # Creating the room layout variable
        [randint(1, 5)]
    ]

    def __init__(self, height, length, room):
        MapModules.length = length  # Length of room
        MapModules.height = height  # Width of room
        MapModules.room = room  # The game map

    @staticmethod
    def generate_map():
        x = 0
        y = 0
        while x < MapModules.height:
            while y < MapModules.length:
                MapModules.room[x].append(randint(1, 5))  # Creating new row for more rooms
                y += 1
            MapModules.room.append([randint(1, 5)])  # adding a new row
            y = 0  # reset y
            x += 1  # increment x
        MapModules.room.pop(-1)  # delete superfluous room
        player_start = randint(0, MapModules.length - 1) # create index cood
        MapModules.room[0][player_start] = 0  # creating a starting room
        MapModules.room[x - 1][randint(0, MapModules.length - 1)] = 6  # creating an exit room
        GameModules.player_pos = [player_start, 0]
        return MapModules.room


class GameModules:

    def __init__(self, character):
        GameModules.player_pos = [0, 0]  # Player position
        self.DIRECTION = ["forward", "right", "left", "back"]
        # List of possible rooms
        self.ROOM_LEGEND = [["Index", "Your starting location!"], ["Treasure Room", "A room with booty!"],
                       ["Trap Room", "ITS A TRAP!"], ["Monster Room", "Run in circles! Your life depends on it!"],
                       ["Regular Room", "Boring"], ["Boss", "R.I.P"], ["Exit", "Tataaa!"]]
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
        # Player
        self.character = character

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

    """Player movement function. Moves player and determines valid input"""
    def move(self):
        x = 0
        # User input loop
        while x == 0:
            print("What do you want to do?")
            # Copy of DIRECTION list with only valid input
            temp = self.DIRECTION[::]
            if self.character["player_pos"][0] == 0:
                temp.remove("left")
            if self.character["player_pos"][0] == MapModules.length - 1:
                temp.remove("right")
            if self.character["player_pos"][1] == MapModules.height - 1:
                temp.remove("forward")
            if self.character["player_pos"][1] == 0:
                temp.remove("back")

            print("Your options are the following:")
            for direction in temp:
                print(direction)
            print("Enter 'quit' to exit this menu")
            print("What will you choose?")
            choice = input()
            if choice not in temp and not choice == "quit":  # check if choice is valid
                print("invalid choice")
            elif "quit" in choice:
                x = 1
            else:
                x = 1
                # Seeing what action user chose
                if choice == "forward":
                    self.character["player_pos"][1] += 1
                elif choice == "right":
                    self.character["player_pos"][0] += 1
                elif choice == "left":
                    self.character["player_pos"][0] -= 1
                elif choice == "back":
                    self.character["player_pos"][1] -= 1

