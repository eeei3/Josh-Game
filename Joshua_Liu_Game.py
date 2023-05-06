"""
Joshua
CS 30 Period 1
April 24, 2023
This is a text-based game that is programmed with OOP.
"""
import random

from Joshua_Liu_Game_Functions import MapModules, GameModules, GeneralModules, EnemyMovement
import threading
import Joshua_Liu_Message_Queue
import time

engage = False


class Game:
    def __init__(self):
        self.map = []
        self.world = []
        self.GameF = None
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.event1 = threading.Event()
        self.event2 = threading.Event()
        self.event3 = threading.Event()
        self.start()
        self.em = None

    def game_quit(self, player):
        gdata = [player.name, player.hp, player.inventory, player.bruh_power, player.pos, self.world]
        # Write map to file
        GeneralModules.write_to_file("prevmap", self.map)
        # Write character state to file
        GeneralModules.write_to_file("previnv", gdata)
        quit()


    def timer(self):
        while True:
            self.main()
            # print("Player has finished movement")
            self.event.set()
            self.event.clear()
            self.event1.set()
            self.event1.clear()
            self.event2.set()
            self.event2.clear()
            self.event3.set()
            self.event3.clear()

    """Player movement function. Moves player and determines valid input"""

    def move(self):
        x = 0
        # User input loop
        while x == 0:
            print("What do you want to do?")
            # Copy of DIRECTION list with only valid input
            temp = self.GameF.DIRECTION[::]
            # Remove invalid dirctions
            if self.GameF.character.pos[0] == 0:
                temp.remove("left")
            if self.GameF.character.pos[0] == MapModules.length - 1:
                temp.remove("right")
            if self.GameF.character.pos[1] == MapModules.height - 1:
                temp.remove("forward")
            if self.GameF.character.pos[1] == 0:
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
                self.world[self.GameF.character.pos[1]][self.GameF.character.pos[0]].leave()
                x = 1  # breaking loop this way
                # Seeing what action user chose
                if choice == "forward":
                    self.GameF.character.pos[1] += 1
                elif choice == "right":
                    self.GameF.character.pos[0] += 1
                elif choice == "left":
                    self.GameF.character.pos[0] -= 1
                elif choice == "back":
                    self.GameF.character.pos[1] -= 1
        self.world[self.GameF.character.pos[1]][self.GameF.character.pos[0]].enter()
        self.main()

    def battle(self):
        if EnemyMovement.engage == False:
            print("Nothing to battle!")
            return
        index = 1
        loop = True
        print("You chose to fight back!")
        print("These are the options that you have:")
        for item in self.GameF.character.inventory:
            if "Dmg" in self.GameF.ITEMS[item]:
                print(f"{index}:  {item}\n{self.GameF.ITEMS[item]['Desc']}")
                index += 1
        print("Make your choice!")
        while loop:
            choice = input()
            item = choice.title()
            if item in self.GameF.character.inventory:
                EnemyMovement.engaged.take_dmg(self.GameF.ITEMS[item]["Dmg"])
                print(f"You did {self.GameF.ITEMS[item]['Dmg']} to {EnemyMovement.engaged}")
                loop = False
                continue
            else:
                print("Bad input! Try again.\n\n")


    def start(self):
        x = True
        print("Do you want to load a previous session?")
        print("If you want to, enter previous, or enter new to make a new game")
        while x:  # Start up loop
            choice = input()  # See what the user wants to do
            if choice.capitalize() == "Previous":
                try:
                    # Get previous map
                    self.map = GeneralModules.read_to_file("prevmap", "reload")
                    # Get previous character state
                    prevcharacter = GeneralModules.read_to_file("previnv", "reload")
                    self.world = prevcharacter[5]
                except FileNotFoundError:
                    print("Previous save does not exist! Try again")
                    continue
                except Exception as e:
                    print("A fatal exception has occured!")
                    print(e)
                    quit()
                else:
                    player = Player(prevcharacter[0], prevcharacter[1], prevcharacter[3],
                                    inventory=prevcharacter[2])
                    MapModules.length = len(self.map[0])  # Getting map length
                    MapModules.height = len(self.map)  # Getting map height
                    self.GameF = GameModules(player)
                    x = False  # stop loop
                finally:
                    pass
            elif choice.capitalize() == "New":
                x = False  # stop loop
                print("Input your character's name:")  # Get player name
                name = input()
                player = Player(name, 5, [])
                mapmaker = MapModules(player)
                data = mapmaker.generate_map()  # generate the map
                self.map = data[0]
                player.pos = data[1]
                print(type(self.world))
                self.world = mapmaker.create_rooms(self.lock, self.event)
                print(type(self.world))
                # Set previous coordinates as current
                # GameF.character["player_pos"] = GameModules.player_pos
                self.GameF = GameModules(player)
                # player.pos = GameModules.player_pos
                # GameF.character["Name"] = input()
                # self.move()  # Give player initial movement
            else:
                print("Bad input. Try again")
        self.em = EnemyMovement(self.lock, self.event, self.event1)
        while True:
            self.timer()

    def main(self):
        loop = False
        print("\n")
        # Print available actions
        print("What do you want to do?")
        for action in self.GameF.character.actions:
            print(action)
        print("Enter quit to exit the game")
        while not loop:
            choice = input()  # get user choice
            if choice.capitalize() == "Move":
                self.em.engaged = False
                loop = True
                self.move()
            # Placeholder functions
            elif choice.capitalize() == "Search":
                GameModules.act(self.GameF)
            elif choice.capitalize() == "Battle":
                self.battle()
                loop = True
            elif choice.capitalize() == "Almanac":
                pass
            # capitalize() wont work. Need title()
            elif choice.title() == "Check Inventory":
                self.GameF.character.check_inv()
            elif choice.title() == "Checkup":
                print(f"HP:{self.GameF.character.hp}")
            # End Placeholder functions
            elif choice.capitalize() == "Quit":
                self.game_quit(self.GameF)
            else:
                print("Bad input. Try that again.")
        # self.event.set()
        # print("Exitting!")


class Player:
    def __init__(self, name, hp, pos, inventory=None):
        self.name = name
        self.hp = hp
        self.inventory = ["Fists"]
        self.actions = ["Search", "Move", "Battle", "Almanac", "Check Inventory", "Checkup"]
        self.pos = pos
        self.room = None
        if inventory is None:
            pass
        else:
            self.inventory = inventory

    def take_damage(self, dmg):
        self.hp -= dmg

    def add_item(self):
        return

    def check_inv(self):
        print(f"You have {len(self.inventory)} items in your inventory")
        if len(self.inventory) != 0:
            for item in self.inventory:
                print(f"You have a {item}")

    def search(self):
        if len(self.room.items) is not 0:
            if random.randint(1, 5) == random.randint(1, 5):
                itemnum = random.randint(0, len(self.room.items))
                print(f"You found an {self.room.items[itemnum]}")
                self.inventory.append(self.room.items[itemnum])

#
# t1 = threading.Thread(target=)
# t1.start()


fungame = Game()
