"""
Joshua
CS 30 Period 1
April 24, 2023
This is a text-based game that is programmed with OOP.
"""
import random
from Joshua_Liu_Game_Functions import MapModules, GameModules, \
    GeneralModules, EnemyMovement


engage = False

"""
Class for the game
"""


class Game:
    def __init__(self):
        self.map = []  # list for simple map (no room objects)
        self.world = []  # list for map with room objects
        self.GameF = None  # Variable for object
        self.em = None
        # Start the game
        self.start()

    """
    Method for handling the player quiting the game
    """
    def game_quit(self, player):
        gdata = [player.name, player.hp, player.inventory,
                 player.pos, player.room, self.em.engaged]
        gmap = [self.world, self.map]
        # Write map to file
        GeneralModules.write_to_file("prevmap", gmap)
        # Write character state to file
        GeneralModules.write_to_file("previnv", gdata)
        quit()

    """
    Method for handling player movement
    """

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
                # does not exit game, brings user back to previous menu
                x = 1
            else:
                self.world[self.GameF.character.pos[1]]\
                    [self.GameF.character.pos[0]].leave()
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
        # Trigger room enter events
        self.world[self.GameF.character.pos[1]]\
            [self.GameF.character.pos[0]].enter()
        # Set player's current room as this room
        self.GameF.character.room = \
            self.world[self.GameF.character.pos[1]]\
                [self.GameF.character.pos[0]]

    """
    Method for handling combat
    """

    def battle(self):
        # Checking if player has won
        if GameModules.win:
            quit()
        # Check if player can enter combat
        if EnemyMovement.engage is False:
            print("\nNothing to battle!")
            return
        index = 1  # number for listing items in inventory
        loop = True  # Make sure player can make legal move
        # Giving player their options
        print("\nYou chose to fight back!")
        print("These are the options that you have:")
        for item in self.GameF.character.inventory:
            if "Dmg" in self.GameF.ITEMS[item]:
                print(f"{index}:  {item}\n"
                      f"{self.GameF.ITEMS[item]['Desc']}")
                index += 1
        if "Shield" in self.GameF.character.inventory:
            print(f"{index}:  Shield\n"
                  f"{self.GameF.ITEMS['Shield']['Desc']}")
        print("Make your choice!")
        # Giving player chance to act
        while loop:
            choice = input()  # Get player input
            item = choice.title()
            # Checking if input is valid or not
            if item in self.GameF.character.inventory:
                if item == "Shield":
                    self.GameF.character.blocking = True
                else:
                    # Inflicting damage on enemy
                    EnemyMovement.engaged.take_dmg(
                        self.GameF.ITEMS[item]["Dmg"])
                    print(f"You did {self.GameF.ITEMS[item]['Dmg']} "
                          f"DMG to {EnemyMovement.engaged.name}")
                    if EnemyMovement.engaged.hp <= 0:
                        print(f"{EnemyMovement.engaged.name} "
                              f"has been defeated")
                        if EnemyMovement.engaged.boss:
                            self.GameF.character.room.items.append(
                                "Key")
                        EnemyMovement.engage = False
                        EnemyMovement.engaged = None
                    # Checking if player used Gilgamesh
                    if item == "Gilgamesh":
                        print("Gilgamesh is too powerful!")
                        # Player takes damage
                        self.GameF.character.take_damage(1)
                loop = False  # Exiting loop
            else:
                print("Bad input! Try again.\n\n")

    """
    Method for handling the start of the game
    """

    def start(self):
        x = True  # Setting start up loop as true
        print("Do you want to load a previous session?")
        print("If you want to, enter previous, "
              "or enter new to make a new game")
        self.em = EnemyMovement()
        while x:  # Start up loop
            choice = input()  # See what the user wants to do
            if choice.capitalize() == "Previous":
                try:
                    # Get previous map
                    gmap = \
                        GeneralModules.read_to_file("prevmap", "reload")
                    self.map = gmap[1]
                    self.world = gmap[0]
                    # Get previous character state
                    prevcharacter = \
                        GeneralModules.read_to_file("previnv", "reload")
                except FileNotFoundError:
                    print("Previous save does not exist! Try again")
                    continue
                except Exception as e:
                    print("A fatal exception has occured!")
                    print(e)
                    quit()
                else:
                    player = Player(prevcharacter[0], prevcharacter[1],
                                    prevcharacter[3],
                                    inventory=prevcharacter[2])
                    player.room = prevcharacter[4]
                    self.em.engaged = prevcharacter[5]
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
                self.world = mapmaker.create_rooms()
                self.GameF = GameModules(player)
                self.world[self.GameF.character.pos[1]]\
                    [self.GameF.character.pos[0]].enter()
                player.room = self.world[self.GameF.character.pos[1]]\
                    [self.GameF.character.pos[0]]
            else:
                print("Bad input. Try again")
        self.main()  # Initial movement
        while True:
            # Is player in combat, if so, use combat routine
            if EnemyMovement.engaged:
                self.main()
                self.em.main()
            # Player is not in combat, proceed as normal
            else:
                self.main()

    """
    Method for handling player loop
    """

    def main(self):
        # Setting main loop as false so the player
        # To account for player inaction
        loop = False
        if EnemyMovement.engage:
            print("\nPlayer has engaged in battle!")
        while not loop:
            # Print available actions
            print("\nWhat do you want to do?")
            for action in self.GameF.character.actions:
                print(action)
            print("Enter quit to exit the game")
            choice = input()  # get user choice
            # Checking if user input is valid
            if choice.capitalize() == "Move":
                self.em.engaged = False
                # loop = True
                self.move()
                loop = True
            elif choice.capitalize() == "Search":
                self.GameF.character.search()
                loop = True
            elif choice.capitalize() == "Battle":
                self.battle()
                loop = True
            # capitalize() wont work. Need title()
            elif choice.title() == "Check Inventory":
                self.GameF.character.check_inv()
            elif choice.title() == "Checkup":
                print(f"HP:{self.GameF.character.hp}")
            elif choice.title() == "Leave Dungeon":
                if choice.title() in self.GameF.character.actions:
                    self.GameF.character.room.exitgame()
            # End Placeholder functions
            elif choice.capitalize() == "Quit":
                self.game_quit(self.GameF.character)
            else:
                print("Bad input. Try that again.")


"""
Class for the player
"""


class Player:
    def __init__(self, name, hp, pos, inventory=None):
        self.name = name  # Name of player
        self.hp = hp  # Player health
        self.inventory = ["Fists", "Shield", "Key"]  # Initial inventory
        # List of actions player can take
        self.actions = ["Search", "Move", "Battle",
                        "Check Inventory", "Checkup"]
        # Player position
        self.pos = pos
        # Room that player is currently in
        # Also gives player object access to room object
        self.room = None
        self.blocking = False
        # Checking if Player class was passed an argument for inventory
        # During initialization
        if inventory is None:
            pass
        else:
            self.inventory = inventory

    """
    Method for handling player taking damage
    """
    def take_damage(self, dmg):
        # Checking if the player is blocking or not
        if not self.blocking:
            self.hp -= dmg
        else:
            print("You blocked the attack!")
            self.blocking = False
        # Checking if the player has died or not
        if self.hp <= 0:
            print("You died!")
            quit()

    """
    Method for handling checking player inventory
    """
    def check_inv(self):
        print(f"You have {len(self.inventory)} items in your inventory")
        for item in self.inventory:
            print(f"You have a {item}")

    """
    Method for handling searching rooms for treasure
    """
    def search(self):
        # Checking if room has any items at all
        if len(self.room.items) != 0:
            # Dice roll to see if player finds anything
            if random.randint(1, 5) == random.randint(1, 5):  # Success
                # Index for item that player found
                itemnum = random.randint(0, len(self.room.items) - 1)
                # Print item that player found
                print(f"You found an {self.room.items[itemnum]}")
                print(f"Desc: "
                      f"{self.room.ITEMS[self.room.items[itemnum]]['Desc']}")
                # Append item to player inventory
                self.inventory.append(self.room.items[itemnum])
                self.room.items.pop(itemnum)  # Remove item from room
            else:  # Player found nothing
                print("You found nothing. Better next time chump!")
        else:  # No items in room
            print("You scour the ground, "
                  "but there isn't even a dust speck to pick up!")


fungame = Game()  # start the game!
