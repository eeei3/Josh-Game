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

GameF = GameModules(character, [0, 0])  # Create GameF object


print("Do you want to load a previous session?")
print("If you want to, enter previous, or enter new to make a new game")
x = True
while x:
    choice = input()
    if choice.capitalize() != "New":
        try:
            game_map = GeneralModules.read_to_file("prevmap", "reload")
            character = GeneralModules.read_to_file("previnv", "reload")
            x = False
        except FileNotFoundError as e:
            print("Previous save does not exist!")
        except:
            print(game_map)
            print(character)
            x = False
            continue
    else:
        game_map = MapModules.generate_map()  # generate the map
        print(GameModules.player_pos)
        x = False


print(game_map)
GameF.character["player_pos"] = GameModules.player_pos
print(GameModules.player_pos)
print(GameF.character)
GameModules.move(GameF)  # Give player initial movement
# Game loop
while 1:
    print(GameF.character)
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
