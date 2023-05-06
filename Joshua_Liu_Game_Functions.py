"""
Joshua
CS 30 Period 1
March 30, 2023
This is file with functions for Joshua_Liu_Game.py
"""

from random import *
import pickle
import threading

# Variable checking if enemy is engaged in combat or not
engage = False
# Constant for all possible rooms
ROOM_LEGEND = [["Index", "Your starting location!"],
                            ["Treasure Room", "A room with booty!"],
                            ["Trap Room", "ITS A TRAP!"], ["Monster Room", "Run in circles! Your life depends on it!"],
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
            "Gravity Coil": {
                "Desc": "boioioioioioioioioioioinnngggg dtdtdtddt",
            },
            "Speed Coil": {
                "Desc": "vrrrrrrrrrrrrooooooooooooooom",
            },
            "Key": {
                "Desc": "But what does it sayyyyyyy?!?!",
            },
            "Fists":
                {
                    "Desc": "Good ol fist cuffs",
                    "Dmg": 2
                },
        }


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
Class containing methods and objects relating to the map
"""


class MapModules:
    length = randint(4, 6)  # Length of room
    height = randint(4, 6)  # Width of room
    room = [  # Creating the room layout variable
        [randint(1, 5)]
    ]
    ROOM_LEGEND = ROOM_LEGEND  # List of rooms

    def __init__(self, character):
        self.character = character  # Giving object access to player object

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

    """
    Method for creating map but with room objects
    rather than integers representing rooms
    """
    def create_rooms(self, lock, event):
        x = 0
        y = 0
        worlb = []
        worlbcpy = [[None]]
        while y < MapModules.height:
            while x < MapModules.length:
                # map[y].append(None)
                # map[y][x] = Room(MapModules.ROOM_LEGEND[MapModules.room[y][x]], [x, y])
                worlb.append(Room(MapModules.ROOM_LEGEND[MapModules.room[y][x]], [x, y], lock, event, self.character))
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


"""
Class for rooms
"""


class Room:
    def __init__(self, roomtype, pos, lock, event, character):
        self.roomtype = roomtype  # The type of room
        self.first = True  # Is this the first time the player has been in the room?
        self.enemie = None  # Enemy in room
        self.pos = pos  # Where is the room on the map?
        self.inroom = True  # Is the player currently in the room?
        self.lock = lock
        self.event = event
        self.items = []  # What items are in the room?
        self.character = character  # Access to character object
        self.ITEMS = ITEMS  # A list of possible items

    """
    Method for handling leaving room
    """
    def leave(self):
        self.inroom = False  # Setting room as exited
        EnemyMovement.engaged = None  # Player no longer engaged
        EnemyMovement.engage = False  # Player is no longer engaged
        # Player no longer satisfies win condition
        self.character.actions.remove("Leave Dungeon")


    """
    Method for handling traps
    """
    def trap(self):
        if randint(1, 7) == randint(1, 7):  # Dice roll for trap
            print("You got hit by a trap!")
            self.character.take_damage(randint(1, 2))
    """
    Method for handling win condition
    """
    def exitgame(self):
        if "Key" in self.character.inventory:
            print("Congratulations! You won!!!")
            print("Now get outta here")

    """
    Method handling for when entering room
    """
    def enter(self):
        self.inroom = True  # Setting player as in room
        if self.first:  # Is this the first time player has entered room?
            self.first = False  # No longer first time
            print("You have discovered a new room")
            print(f"You are now in a {self.roomtype[0]}")
            # Events for Monster Room
            if self.roomtype[0] == "Monster Room":
                # Create random enemy object
                enemyname = GameModules.ENEMIESLIST[randint(0, 4)]
                enemy = Enemy(enemyname, GameModules.ENEMIES[enemyname], [self.pos[1], self.pos[0]], self.character, EnemyMovement.number)
                print(f"You have encountered a {enemy}")
                # Setting player as engaged against enemy
                EnemyMovement.engaged = enemy
                # Setting player as engaged
                EnemyMovement.engage = True
                # Adding enemy to movement pool
                EnemyMovement.pool[EnemyMovement.number] = enemy
                # Incremented amount of enemies in map
                EnemyMovement.number += 1
                # Setting enemy in room as this enemy
                self.enemie = enemy
            # Events for Boss Room
            elif self.roomtype[0] == "Boss Room":
                print("Entering boss room")
                # Create random boss object
                enemyname = GameModules.BOSSLIST[randint(0, 3)]
                enemy = Boss(enemyname, GameModules.BOSS[enemyname], [self.pos[1], self.pos[0]], self.character, EnemyMovement.number)
                print(f"You have encountered a {enemy}")
                # Setting player as engaged against boss
                EnemyMovement.engaged = enemy
                # Setting player as engaged
                EnemyMovement.engage = True
                # Adding boss to movement pool
                EnemyMovement.pool[EnemyMovement.number] = enemy
                # Incrementing amount of enemies in game
                EnemyMovement.number += 1
                # Setting enemy in room as this boss
                self.enemie = enemy
            # Events for Trap Room
            elif self.roomtype[0] == "Trap Room":
                self.trap()  # Triggering trap
            # Events for Regular and Index Room
            elif self.roomtype[0] == "Regular Room" or self.roomtype == "Index Room":
                return
            # Events for Treasure Room
            elif self.roomtype[0] == "Treasure Room":
                # Spawning treasure
                treasure = randint(0, 8)
                itemlist = []
                for key in self.ITEMS:
                    itemlist.append(key)
                self.items.append(itemlist[treasure])
                # Chance for a second treasure to spawn in
                if randint(0, 4) == randint(0, 4):
                    treasure = randint(0, 8)
                    itemlist = []
                    for key in self.ITEMS:
                        itemlist.append(key)
                    self.items.append(itemlist[treasure])
            # Events for Exit
            elif self.roomtype[0] == "Exit":
                print("You feel a need to be here")
                self.character.actions.append("Leave Dungeon")
                return
        # This is NOT the first time player has been in room
        else:
            print(f"You are now in a {self.roomtype[0]}")
            # Events for Monster Room
            if self.roomtype[0] == "Monster Room":
                if self.enemie is not None:  # Is there still an enemy here?
                    # Is the enemy dead?
                    if self.enemie.hp > 0:  # No
                        print(self.enemie.hp)
                        print(f"You have encountered a {self.enemie}")
                        EnemyMovement.engaged = self.enemie
                        EnemyMovement.engage = True
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
                        print(f"You have encountered a {self.enemie}")
                        EnemyMovement.engaged = self.enemie
                        EnemyMovement.engage = True
                    else:  # Yes
                        del self.enemie  # Deleting boss object
                        self.enemie = None
                        if randint(1, 4) == 1:
                            self.items.append(self.ITEMS["Key"])
            # Events for Trap Room
            elif self.roomtype[0] == "Trap Room":
                self.trap()
            # Events for Regular and Index Room
            elif self.roomtype[0] == "Regular Room" or self.roomtype == "Index Room":
                return
            # Events for Treasure Room
            elif self.roomtype[0] == "Treasure Room":
                return
            # Events for Exit Room
            elif self.roomtype[0] == "Exit":
                self.character.actions.append("Leave Dungeon")
                return
            else:
                return


"""
Class for Enemy movement
"""


class EnemyMovement:
    pool = []  # List containing all enemy objects
    engaged = None  # Enemy currently engaged in combat with player
    number = 0
    engage = False  # Is the player currently engaged with the enemy?

    def __init__(self, lock, event, event1):
        for i in range(0, 60):  # Populating list
            EnemyMovement.pool.append(None)
        # self.activated = False
        # self.engaged = None
        self.ticks = 0
        self.playeraction = False  # Is it the player's turn to move?
        self.lock = lock
        self.event = event
        self.event1 = event1
        self.t1 = threading.Thread(target=self.main)  # Enemy thread
        self.t1.start()

    def main(self):
        while True:
            while EnemyMovement.engage is True:
                self.event.wait()
                print("Player has engaged in battle!")
                self.counter(EnemyMovement.engaged)
                self.event.clear()

    def counter(self, eenemy=None):
        if eenemy is None:
            print(EnemyMovement.pool)
            pass
        else:
            if eenemy.hp >= 0:
                eenemy.baction()
            else:
                print(f"{eenemy} has been defeated")
                EnemyMovement.pool[self.number] = None
                EnemyMovement.engage = False


"""
Class for Enemies
"""


class Enemy:
    def __init__(self, name, stats, position, target, number):
        self.name = name  # Enemy name
        self.stats = stats  # Enemy stats
        self.position = position  # Enemy position on map
        self.hp = stats["HP"]  # Enemy HP
        self.action = stats["Actions"]  # Enemy attack
        self.Damage = stats["Damage"]  # Enemy damage
        self.activated = True  # Is the enemy currently active?
        self.target = target  # Enemy access to player object
        self.number = number

    def __str__(self):
        return '{self.name}'.format(self=self)

    """
    Method that handles enemy actions
    """
    def baction(self):
        if randint(1, 5) == randint(1, 5):  # Dice roll for enemy attack
            print(f"{Enemy} used {self.action}!")
            print(f"You took {self.Damage} damage!")
            self.target.take_damage(self.Damage)  # Subtract player health
        else:
            print(f"{Enemy} failed to attack! Your move!")

        if randint(1, 40) == randint(1, 20):  # Dice roll for enemy healing
            print(f"{Enemy} is healing!")
            self.heal(randint(1, 3))  # Heal random amount for enemy

    """
    Method that handles enemy healing
    """
    def heal(self, amount):
        self.hp += amount
        return

    """
    Method that handles enemy taking damage
    """
    def take_dmg(self, dmg):
        self.hp -= dmg


class Boss(Enemy):
    def __init__(self, name,  stats, position, target, number):
        super().__init__(name, stats, position, target, number)
        # List of enemy actions options
        self.actions = ["Attack", "Super Attack", "Heal", "Defend", "Move"]
        self.activated = True  # Is the boss active?
        self.blocking = False  # Is the boss blocking attacks?
        self.superattacked = False  # Has the boss super attacked?
        self.DIRECTION = ["forward", "right", "left", "back"]

    """
    Method handling boss actions
    """

    def baction(self):
        self.panic()
        if randint(1, 3) == randint(1, 3):
            choice = self.actions[randint(0, 4)]
            if choice == "Attack":
                self.attack()
            elif choice == "Defend":
                self.blocking = True
            elif choice == "Heal":
                self.heal(randint(4, 6))
            elif choice == "Move":
                # self.roommove()
                return
            elif choice == "Super Attack":
                self.super_attack()
        else:
            print("BOSS failed move! Strike back!")

    """
    Boss handling enemy attack
    """

    def attack(self):
        if randint(1, 3) == randint(1, 3):  # Dice roll to attack
            print(f"{Enemy} used {self.action}!")
            print(f"You took {self.Damage} damage!")
            if self.superattacked:
                self.target.take_damage(self.Damage//2)
            else:
                self.target.take_damage(self.Damage)
        else:
            print(f"{Enemy} failed to attack! Your move!")
        return

    """
    Method handling boss movement
    """

    def roommove(self):
        temp = self.DIRECTION[::]
        if self.position[0] == 0:
            temp.remove("left")
        if self.position[0] == MapModules.length - 1:
            temp.remove("right")
        if self.position[1] == MapModules.height - 1:
            temp.remove("forward")
        if self.position[1] == 0:
            temp.remove("back")

        choice = temp[randint(0, len(temp)-1)]

        if choice == "forward":
            self.position[1] += 1
        elif choice == "right":
            self.position[0] += 1
        elif choice == "left":
            self.position[0] -= 1
        elif choice == "back":
            self.position[1] -= 1

    def super_attack(self):
        if self.superattacked:  # Checking if the boss has super attacked or not
            if randint(1, 9) == randint(1, 9):  # Dice roll to super attack
                print("BOSS is amping up his attack!")
                print(f"{Enemy} used {self.action}!")
                print(f"You took {self.Damage} damage!")
                self.target.take_damage(self.Damage * 2)
                self.superattacked = True
            else:
                print(f"{Enemy} failed to attack! Your move!")
        else:
            if randint(1, 2) == randint(1, 2):  # Dice roll to super attack
                print("BOSS is amping up his attack!")
                print(f"{Enemy} used {self.action}!")
                print(f"You took {self.Damage} damage!")
                self.target.take_damage(self.Damage)
            else:
                print(f"{Enemy} failed to attack! Your move!")

    def panic(self):
        if 1 > self.hp > 0:  # Checking panic conditions
            print("The BOSS is unleashing its fury!")
            self.super_attack()
            self.baction()
            self.heal(8)


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
            "Actions": ["Bite", "Parry"],
            "Damage": 7
        },
        "the MOON": {
            "HP": 12,
            "Actions": ["Roll", "Parry"],
            "Damage": 3
        },
        "teh epix duck": {
            "HP": 25,
            "Actions": ["Quack", "Parry"],
            "Damage": 6
        },
        "Telamon": {
            "HP": 20,
            "Actions": ["Stab", "Parry"],
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
    EACTIONS = {
        "Cook": 1,
        "Scream": 2,
        "Talk": 3,
        "Swing": 4,
        "Stab": 5,
        "Parry": 6,
        "Bite": 7,
        "Block": 8,
        "Roll": 9,
        "Quack": 10
    }

    def __init__(self, character):
        GameModules.player_pos = [0, 0]  # Class variable for player position
        # Constant for directions
        self.DIRECTION = ["forward", "right", "left", "back"]
        # Constant for rooms
        self.ROOM_LEGEND = ROOM_LEGEND
        # Constant for items available
        self.ITEMS = ITEMS
        # Player object
        self.character = character

    """Printing player actions function. Prints inventory"""
    def act(self):
        print("Your available actions:")
        for item in self.ITEMS.keys():
            for thing in self.ITEMS[item].keys():
                print(f'{item}: {thing} {self.ITEMS[item][thing]}')

    """Function for printing player inventory"""
    def check_inv(self):
        print(f"You have {len(self.character.inventory)} items in your inventory")
        if len(self.character.inventory) != 0:
            for item in self.character.inventory:
                print(f"You have a {item}")
