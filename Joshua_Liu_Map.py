"""
Joshua
CS 30 Period 1
March 13, 2023
This is a simple game that generates a random map,
allows movement and has a system for enemies and
inventories alike.
"""
from Joshua_Liu_Game_Functions import MapModules, GameModules

# Player
character = {
    "Name": "",
    "HP": 5,
    "Inventory": [],
    "Bruh Power": 0,
    "Actions": ["Search", "Move", "Battle", "Almanac", "Check Inventory"]
}

GameF = GameModules(character, [0, 0])

game_map = MapModules.generate_map()  # generate the map
GameModules.move(GameF)
# Game loop
while 1:
    print(f'You are now in a "{GameF.ROOM_LEGEND[game_map[GameF.player_pos[1]][GameF.player_pos[0]]][0]}" room')
    print(f"{GameF.ROOM_LEGEND[game_map[GameF.player_pos[1]][GameF.player_pos[0]]][1]}\n")

    print("What do you want to do?")
    for action in GameF.character["Actions"]:
        print(action)
    print("Enter quit to exit the game")
    choice = input()
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
        quit()
    else:
        print("Bad input. Try that again.")
    print("\n")
