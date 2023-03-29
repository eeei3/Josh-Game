"""
Joshua
CS 30 Period 1
March 13, 2023
This is a simple game that generates a random map,
allows movement and has a system for enemies and
inventories alike.
"""
from Joshua_Liu_Game_Functions import MapModules, GameModules, GeneralModules
import datetime


def game_quit():
    GeneralModules.write_to_file("prevmap", game_map)
    GeneralModules.write_to_file("previnv", GameF.character)
    print(GameF.character["player_pos"])
    quit()


# Player
character = {
    "Name": "",
    "HP": 5,
    "Inventory": [],
    "Bruh Power": 0,
    "Actions": ["Search", "Move", "Battle", "Almanac", "Check Inventory"],
    "player_pos": [0, 0]
}

GameF = GameModules(character)  # Create GameF object
x = True
prev_game = False  # Check if game is new


print("Do you want to load a previous session?")
print("If you want to, enter previous, or enter new to make a new game")
while x:
    choice = input()
    if choice.capitalize() == "Previous":
        try:
            game_map = GeneralModules.read_to_file("prevmap", "reload")
            GameF.character = GeneralModules.read_to_file("previnv", "reload")
            character = GameF.character
            MapModules.length = len(game_map[0])
            MapModules.height = len(game_map)
            x = False
        except FileNotFoundError as e:
            print("Previous save does not exist!")
            continue
        except Exception as e:
            x = False
            continue
    else:
        x = False
        game_map = MapModules.generate_map()  # generate the map
        GameF.character["player_pos"] = GameModules.player_pos
        print("Input your character's name:")
        GameF.character["Name"] = input()
        GameModules.move(GameF)  # Give player initial movement


# Game loop
while 1:
    print(f'You are now in a "{GameF.ROOM_LEGEND[game_map[GameF.character["player_pos"][1]][GameF.character["player_pos"][0]]][0]}" room')
    print(f"{GameF.ROOM_LEGEND[game_map[GameF.character['player_pos'][1]][GameF.character['player_pos'][0]]][1]}\n")
    # Print available actions
    print("What do you want to do?")
    for action in GameF.character["Actions"]:
        print(action)
    print("Enter quit to exit the game")
    choice = input()  # get user choice
    if choice.capitalize() == "Move":
        GameModules.move(GameF)
    elif choice.capitalize() == "Search":
        GameModules.act(GameF)
    elif choice.capitalize() == "Battle":
        GameModules.act(GameF)
    elif choice.capitalize() == "Almanac":
        pass
    elif choice.title() == "Check Inventory":  # capitalize() wont work. Need title()
        GameModules.check_inv(GameF)
    elif choice.capitalize() == "Quit":
        game_quit()
    else:
        print("Bad input. Try that again.")
    print("\n")
