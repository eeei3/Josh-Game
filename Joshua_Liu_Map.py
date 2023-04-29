"""
Joshua
CS 30 Period 1
April 24, 2023
This is a text-based game that is programmed with OOP.
"""
from Joshua_Liu_Game_Functions import MapModules, GameModules, GeneralModules


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

    def start(self):
        x = True
        print("Do you want to load a previous session?")
        print("If you want to, enter previous, or enter new to make a new game")
        while x:  # Start up loop
            choice = input()  # See what the user wants to do
            if choice.capitalize() == "Previous":
                try:
                    # Get previous map
                    game_map = GeneralModules.read_to_file("prevmap", "reload")
                    # Get previous character state
                    prevcharacter = GeneralModules.read_to_file("previnv", "reload")
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
                    MapModules.length = len(game_map[0])  # Getting map length
                    MapModules.height = len(game_map)  # Getting map height
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
                self.world = mapmaker.create_rooms()
                # Set previous coordinates as current
                # GameF.character["player_pos"] = GameModules.player_pos
                self.GameF = GameModules(player)
                # player.pos = GameModules.player_pos
                # GameF.character["Name"] = input()
                GameModules.move(self.GameF)  # Give player initial movement
            else:
                print("Bad input. Try again")

    def main(self):
        # room = self.GameF.ROOM_LEGEND[self.map[self.GameF.character.pos[1]][self.GameF.character.pos[0]]][0]
        print(
            f'You are now in a "' + f'{self.GameF.ROOM_LEGEND[self.map[self.GameF.character.pos[1]][self.GameF.character.pos[0]]][0]}"'
            + f' room')
        # print(f'You are now in a "' + f'{GameF.ROOM_LEGEND[game_map[player.pos[1]][player.pos[0]]][0]}"' + f' room')
        print(f"{self.GameF.ROOM_LEGEND[self.map[self.GameF.character.pos[1]][GameF.character.pos[0]]][1]}\n")
        # print(f"{GameF.ROOM_LEGEND[game_map[player.pos[1]][player.pos[0]]][1]}\n")

        # Print available actions
        print("What do you want to do?")
        for action in self.GameF.character.actions:
            print(action)
        print("Enter quit to exit the game")
        choice = input()  # get user choice
        if choice.capitalize() == "Move":
            GameModules.move(self.GameF)
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
