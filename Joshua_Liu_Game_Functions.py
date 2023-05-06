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


class MapModules:
    """
    Class containing methods and objects relating to the map
    """
    length = randint(4, 6)  # Length of room
    height = randint(4, 6)  # Width of room
    room = [  # Creating the room layout variable
        [randint(1, 5)]
    ]
    ROOM_LEGEND = ROOM_LEGEND  # List of rooms

    def __init__(self, character):
        # Giving object access to player object
        self.character = character

    def generate_map(self):
        """
        Function for creating a random map
        """
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
        # create index cood
        player_start = randint(0, MapModules.length - 1)
        MapModules.room[0][player_start] = 0  # creating a starting room
        # creating an exit room
        MapModules.room[x - 1][randint(0, MapModules.length - 1)] = 6
        GameModules.player_pos = [player_start, 0]
        data = [MapModules.room, GameModules.player_pos]
        return data

    def create_rooms(self):
        """
        Method for creating map but with room objects
        rather than integers representing rooms
        """
        x = 0
        y = 0
        worlb = []
        worlbcpy = [[None]]
        while y < MapModules.height:
            while x < MapModules.length:
                worlb.append(Room(
                    MapModules.ROOM_LEGEND[MapModules.room[y][x]],
                    [x, y], self.character))
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
    """
    Class for rooms
    """
    def __init__(self, roomtype, pos, character):
        self.roomtype = roomtype  # The type of room
        # Is this the first time the player has been in the room?
        self.first = True
        self.enemie = None  # Enemy in room
        self.pos = pos  # Where is the room on the map?
        self.inroom = True  # Is the player currently in the room?
        self.items = []  # What items are in the room?
        self.character = character  # Access to character object
        self.ITEMS = ITEMS  # A list of possible items

    def leave(self):
        """
        Method for handling leaving room
        """
        self.inroom = False  # Setting room as exited
        EnemyMovement.engaged = None  # Player no longer engaged
        EnemyMovement.engage = False  # Player is no longer engaged
        # Player no longer satisfies win condition
        if "Leave Dungeon" in self.character.actions:
            self.character.actions.remove("Leave Dungeon")

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

    def enter(self):
        """
        Method handling for when entering room
        """
        self.inroom = True  # Setting player as in room
        # Is this the first time player has entered room?
        if self.first:
            self.first = False  # No longer first time
            print("\nYou have discovered a new room")
            print(f"You are now in a {self.roomtype[0]}")
            # Events for Monster Room
            if self.roomtype[0] == "Monster Room":
                # Create random enemy object
                enemyname = GameModules.ENEMIESLIST[randint(0, 4)]
                enemy = Enemy(enemyname, GameModules.ENEMIES[enemyname],
                              [self.pos[1], self.pos[0]],
                              self.character)
                print(f"You have encountered a {enemy.name}")
                # Setting player as engaged against enemy
                EnemyMovement.engaged = enemy
                # Setting player as engaged
                EnemyMovement.engage = True
                # Setting enemy in room as this enemy
                self.enemie = enemy
            # Events for Boss Room
            elif self.roomtype[0] == "Boss Room":
                print("Entering boss room")
                # Create random boss object
                enemyname = GameModules.BOSSLIST[randint(0, 3)]
                enemy = Boss(enemyname, GameModules.BOSS[enemyname],
                             [self.pos[1], self.pos[0]], self.character)
                print(f"You have encountered a {enemy.name}")
                # Setting player as engaged against boss
                EnemyMovement.engaged = enemy
                # Setting player as engaged
                EnemyMovement.engage = True
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
                        print(f"\nYou have encountered a "
                              f"{self.enemie.name}")
                        EnemyMovement.engaged = self.enemie
                        EnemyMovement.engage = True
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
            else:
                return


class EnemyMovement:
    """
    Class for Enemy movement
    """
    engaged = None  # Enemy currently engaged in combat with player
    number = 0
    engage = False  # Is the player currently engaged with the enemy?

    def __init__(self):
        self.playeraction = False  # Is it the player's turn to move?

    def counter(self, eenemy=None):
        """Function in charge of executing enemy action"""
        if eenemy is not None:
            eenemy.baction()


class Enemy:
    """
    Class for Enemies
    """

    def __init__(self, name, stats, position, target):
        self.name = name  # Enemy name
        self.stats = stats  # Enemy stats
        self.position = position  # Enemy position on map
        self.hp = stats["HP"]  # Enemy HP
        self.action = stats["Actions"]  # Enemy attack
        self.Damage = stats["Damage"]  # Enemy damage
        self.boss = False  # Easier knowledge if enemy is boss or not
        self.target = target  # Enemy access to player object

    def baction(self):
        """
        Method that handles enemy actions
        """
        # Dice roll for enemy attack
        if randint(1, 5) == randint(1, 5):
            print(f"{self.name} used {self.action[0]}!")
            print(f"You took {self.Damage} damage!")
            # Subtract player health
            self.target.take_damage(self.Damage)
        else:
            print(f"{self.name} failed to attack! Your move!")
        # Dice roll for enemy healing
        if randint(1, 40) == randint(1, 20):
            print(f"{self.name} is healing!")
            self.heal(randint(1, 3))  # Heal random amount for enemy

    def heal(self, amount):
        """
        Method that handles enemy healing
        """
        self.hp += amount
        return

    def take_dmg(self, dmg):
        """
        Method that handles enemy taking damage
        """
        self.hp -= dmg


class Boss(Enemy):
    """
    Class for Bosses
    """
    def __init__(self, name,  stats, position, target):
        super().__init__(name, stats, position, target)
        # List of enemy actions options
        self.actions = ["Attack", "Super Attack", "Heal", "Defend"]
        self.activated = True  # Is the boss active?
        self.blocking = False  # Is the boss blocking attacks?
        self.boss = True
        self.superattacked = False  # Has the boss super attacked?

    def take_dmg(self, dmg):
        """
        Method that handles enemy taking damage
        """
        if not self.blocking:
            self.hp -= dmg
        else:
            print("Boss blocked your attack!")
            self.blocking = False

    def baction(self):
        """
        Method handling boss actions
        """
        self.panic()
        if randint(1, 2) == randint(1, 2):
            choice = self.actions[randint(0, 3)]
            if choice == "Attack":
                self.attack()
            elif choice == "Defend":
                print("\nBoss is hunkering down!")
                self.blocking = True
            elif choice == "Heal":
                print("\nBoss is rapidly recovering!")
                self.heal(randint(4, 6))
            elif choice == "Super Attack":
                self.super_attack()
        else:
            print("BOSS failed move! Strike back!")

    def attack(self):
        """
        Method handling boss attack
        """
        print(f"\n{self.name} used {self.action[0]}!")
        print(f"You took {self.Damage} damage!")
        if self.superattacked:
            self.target.take_damage(self.Damage//2)
        else:
            self.target.take_damage(self.Damage)

    def super_attack(self):
        """
        Method handling boss super attack
        """
        # Checking if the boss has super attacked
        if self.superattacked:
            # Dice roll to super attack
            if randint(1, 9) == randint(1, 9):
                print("\nBOSS is amping up his attack!")
                print(f"{self.name} used {self.action[0]}!")
                print(f"You took {self.Damage*2} damage!")
                self.target.take_damage(self.Damage * 2)
                self.superattacked = True
            else:
                print(f"{self.name} failed to attack! Your move!")
        else:
            # Dice roll to super attack
            if randint(1, 2) == randint(1, 2):
                print("\nBOSS is amping up his attack!")
                print(f"{self.name} used {self.action[0]}!")
                print(f"You took {self.Damage} damage!")
                self.target.take_damage(self.Damage)
            else:
                print(f"{self.name} failed to attack! Your move!")

    def panic(self):
        """
        Method handling boss panic functionality
        """
        if 3 > self.hp > 0:  # Checking panic conditions
            print("\nThe BOSS is unleashing its fury!")
            self.super_attack()
            self.baction()
            self.heal(8)


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
