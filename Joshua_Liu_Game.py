"""
Joshua
CS 30 Period 1
April 24, 2023
This is a text-based game that is programmed with OOP.
"""
import Joshua_Liu_Enemy
from Joshua_Liu_Game_Functions import GeneralModules
import Joshua_Liu_Player
import Joshua_Liu_Map


class Game:
    """Class for the game"""

    def __init__(self):
        self.map = []  # list for simple map (no room objects)
        self.world = []  # list for map with room objects
        # self.em = EnemyMovement()  # Variable for enemy movement object
        self.em = None
        self.game_map = None
        self.character = None
        # Start the game
        self.start()

    def game_quit(self, player):
        """Method for handling the player quiting the game"""
        # Data relating to player
        gdata = [self.character.name, self.character.hp,
                 self.character.inventory, self.character.pos,
                 self.character.room, self.em.engaged]
        # Data relating to the map
        mdata = [self.game_map.roommap,
                 self.game_map.layoutmap,
                 self.game_map.initpos]
        # Write map to file
        GeneralModules.write_to_file("prevmap", mdata)
        # Write character state to file
        GeneralModules.write_to_file("previnv", gdata)
        quit()

    def battle(self):
        """Method for handling combat"""
        # Check if player can enter combat
        if self.em.engage is False:
            print("\nNothing to battle!")
            return
        index = 1  # number for listing items in inventory
        loop = True  # Make sure player can make legal move
        # Giving player their options
        print("\nYou chose to fight back!")
        print("These are the options that you have:")
        for item in self.character.inventory:
            if "Dmg" in self.game_map.ITEMS[item]:
                print(f"{index}:  {item}\n"
                      f"{self.game_map.ITEMS[item]['Desc']}")
                index += 1
        if "Shield" in self.character.inventory:
            print(f"{index}:  Shield\n"
                  f"{self.game_map.ITEMS['Shield']['Desc']}")
        print("Make your choice!")
        # Giving player chance to act
        while loop:
            choice = input()  # Get player input
            item = choice.title()
            # Checking if input is valid or not
            if item in self.character.inventory:
                if item == "Shield":
                    self.character.blocking = True
                else:
                    # Inflicting damage on enemy
                    self.em.engaged.take_dmg(
                        self.game_map.ITEMS[item]["Dmg"])
                    print(f"You did {self.game_map.ITEMS[item]['Dmg']} "
                          f"DMG to {self.em.engaged.name}")
                    if self.em.engaged.hp <= 0:
                        print(f"{self.em.engaged.name} "
                              f"has been defeated")
                        if self.em.engaged.boss:
                            self.character.room.items.append(
                                "Key")
                        self.em.engage = False
                        self.em.engaged = None
                    # Checking if player used Gilgamesh
                    if item == "Gilgamesh":
                        print("Gilgamesh is too powerful!")
                        # Player takes damage
                        self.character.take_damage(1)
                loop = False  # Exiting loop
            else:
                print("Bad input! Try again.\n\n")

    def start(self):
        """Method for handling the start of the game"""
        x = True  # Setting start up loop as true
        print("Do you want to load a previous session?")
        print("If you want to, enter previous, "
              "or enter new to make a new game")
        while x:  # Start up loop
            choice = input()  # See what the user wants to do
            if choice.capitalize() == "Previous":
                try:
                    # Get previous map
                    gmap = \
                        GeneralModules.read_to_file("prevmap", "reload")
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
                    self.character = Joshua_Liu_Player.Player(
                        prevcharacter[0],
                        prevcharacter[1],
                        prevcharacter[3],
                        inventory=prevcharacter[2])
                    self.em = Joshua_Liu_Enemy.EnemyActions()
                    self.game_map = Joshua_Liu_Map.GameMap(
                        self.character, self.em)
                    self.game_map.roommap = gmap[0]
                    self.game_map.layoutmap = gmap[1]
                    self.game_map.initpos = gmap[2]
                    self.character.room = prevcharacter[4]
                    self.em.engaged = prevcharacter[5]
                    # Getting map length
                    self.game_map.length = len(
                        self.game_map.layoutmap[0])
                    # Getting map height
                    self.game_map.height = len(self.game_map.layoutmap)
                    print(self.character.pos[1])
                    self.game_map.roommap[self.character.pos[1]] \
                        [self.character.pos[0]].enter()
                    self.character.room = self.game_map.roommap[
                        self.character.pos[1]] \
                        [self.character.pos[0]]
                    x = False  # stop loop
                finally:
                    pass
            elif choice.capitalize() == "New":
                x = False  # stop loop
                print("Input your character's name:")  # Get player name
                name = input()
                # Player object
                self.character = Joshua_Liu_Player.Player(name, 5, [])
                self.em = Joshua_Liu_Enemy.EnemyActions()
                self.game_map = Joshua_Liu_Map.GameMap(
                    self.character, self.em)
                # Player spawn point
                self.character.pos = self.game_map.initpos
                # Player has entered room thus triggering
                # Entered function
                self.game_map.roommap[self.character.pos[1]]\
                    [self.character.pos[0]].enter()
                # Setting player current room as this room
                self.character.room = self.game_map.roommap[
                    self.character.pos[1]]\
                    [self.character.pos[0]]
            else:
                print("Bad input. Try again")
        self.main()  # Initial movement
        while True:
            # Is player in combat, if so, use combat routine
            if self.em.engaged:
                self.main()
                self.em.counter(self.em.engaged)
            # Player is not in combat, proceed as normal
            else:
                self.main()

    def main(self):
        """
        Method for handling player loop
        """
        # Setting main loop as false so the player
        # To account for player inaction
        loop = False
        if self.em.engage:
            print("\nPlayer has engaged in battle!")
        while not loop:
            # Print available actions
            print("\nWhat do you want to do?")
            for action in self.character.actions:
                print(action)
            print("Enter quit to exit the game")
            choice = input()  # get user choice
            # Checking if user input is valid
            if choice.capitalize() == "Move":
                self.em.engaged = None
                self.em.engage = False
                # loop = True
                self.game_map.move()
                loop = True
            elif choice.capitalize() == "Search":
                self.character.search()
                loop = True
            elif choice.capitalize() == "Battle":
                self.battle()
                loop = True
            # capitalize() wont work. Need title()
            elif choice.title() == "Check Inventory":
                self.character.inventory.check_inv()
            elif choice.title() == "Checkup":
                # Checking how much health player has
                print(f"HP: {self.character.hp}")
            # Player attempting to trigger win condition
            elif choice.title() == "Leave Dungeon":
                if choice.title() in self.character.actions:
                    self.game_map.exitgame()
            # End Placeholder functions
            elif choice.capitalize() == "Quit":
                self.game_quit(self.character)
            else:
                print("Bad input. Try that again.")


fungame = Game()  # start the game!
