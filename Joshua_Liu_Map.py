"""
Joshua
CS 30 Period 1
April 24, 2023
This is a text-based game that is programmed with OOP.
"""
from Joshua_Liu_Game_Functions import MapModules, GameModules, GeneralModules, Room

engage = False


class Game:
    def __init__(self):
        self.map = []
        self.world = []
        self.GameF = None
        self.start()

    def game_quit(self, player):
        gdata = [player.name, player.hp, player.inventory, player.bruh_power, player.pos, self.world]
        # Write map to file
        GeneralModules.write_to_file("prevmap", self.map)
        # Write character state to file
        GeneralModules.write_to_file("previnv", gdata)
        quit()

    """Player movement function. Moves player and determines valid input"""

    def move(self):
        x = 0
        # User input loop
        print(self.world)
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
        print(self.world)
        self.world[self.GameF.character.pos[1]][self.GameF.character.pos[0]].enter()

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
                    player = Player(prevcharacter[0], prevcharacter[1],
                                    prevcharacter[2], prevcharacter[3],
                                    prevcharacter[4])
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
                player = Player(name, 5, [], 0, [])
                mapmaker = MapModules()
                data = mapmaker.generate_map()  # generate the map
                self.map = data[0]
                player.pos = data[1]
                print(type(self.world))
                self.world = mapmaker.create_rooms()
                print(type(self.world))
                # Set previous coordinates as current
                # GameF.character["player_pos"] = GameModules.player_pos
                self.GameF = GameModules(player)
                # player.pos = GameModules.player_pos
                # GameF.character["Name"] = input()
                self.move()  # Give player initial movement
            else:
                print("Bad input. Try again")

    def main(self):
        # room = self.GameF.ROOM_LEGEND[self.map[self.GameF.character.pos[1]][self.GameF.character.pos[0]]][0]
        print(
            f'You are now in a "' + f'{self.GameF.ROOM_LEGEND[self.map[self.GameF.character.pos[1]][self.GameF.character.pos[0]]][0]}"'
            + f' room')
        # print(f'You are now in a "' + f'{GameF.ROOM_LEGEND[game_map[player.pos[1]][player.pos[0]]][0]}"' + f' room')
        print(f"{self.GameF.ROOM_LEGEND[self.map[self.GameF.character.pos[1]][self.GameF.character.pos[0]]][1]}\n")
        # print(f"{GameF.ROOM_LEGEND[game_map[player.pos[1]][player.pos[0]]][1]}\n")

        # Print available actions
        print("What do you want to do?")
        for action in self.GameF.character.actions:
            print(action)
        print("Enter quit to exit the game")
        choice = input()  # get user choice
        if choice.capitalize() == "Move":
            self.move()
        # Placeholder functions
        elif choice.capitalize() == "Search":
            GameModules.act(self.GameF)
        elif choice.capitalize() == "Battle":
            GameModules.act(self.GameF)
        elif choice.capitalize() == "Almanac":
            pass
        # capitalize() wont work. Need title()
        elif choice.title() == "Check Inventory":
            GameModules.check_inv(self.GameF)
        # End Placeholder functions
        elif choice.capitalize() == "Quit":
            self.game_quit(self.GameF)
        else:
            print("Bad input. Try that again.")
        print("\n")


class Player:
    def __init__(self, name, hp, inventory, bruh_power, pos):
        self.name = name
        self.hp = hp
        self.inventory = inventory
        self.bruh_power = bruh_power
        self.actions = ["Search", "Move", "Battle", "Almanac", "Check Inventory"]
        self.pos = pos


fungame = Game()
