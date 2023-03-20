"""
Joshua
CS 30 Period 1
March 13, 2023
This is a simple game that generates a random map,
allows movement and has a system for enemies and
inventories alike.
"""
from random import *


# List of possible solutions
DIRECTION = ["forward", "right", "left", "back"]
# List of possible rooms
ROOM_LEGEND = [["Index", "Your starting location!"], ["Treasure Room", "A room with booty!"],
               ["Trap Room", "ITS A TRAP!"], ["Monster Room", "Run in circles! Your life depends on it!"],
               ["Regular Room", "Boring"], ["Boss", "R.I.P"], ["Exit", "Tataaa!"]]
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
        "Dmg": 90
    },
    "Jerma": {
        "Desc": "Unleash destruction upon your foes",
        "Dmg": 35
    },
    "Omega Energy Sword": {
        "Desc": "Super damage!",
        "Dmg": 20
    },
    "Gravity Coil": {
        "Desc": "boioioioioioioioioioioinnngggg dtdtdtddt",
    },
    "Speed Coil": {
        "Desc": "vrrrrrrrrrrrrooooooooooooooom",
    },
    "Key": {
        "Desc": "But what does it sayyyyyyy?!?!",
    }
}
BOSS = {
    "the FACE": {
        "HP": 7,
        "Actions": ["Bite", "Block", "Parry"],
        "Damage": 7
    },
    "the MOON": {
        "HP": 12,
        "Actions": ["Roll", "Block", "Parry"],
        "Damage": 3
    },
    "teh epix duck": {
        "HP": 25,
        "Actions": ["Qauck", "Block", "Parry"],
        "Damage": 6
    },
    "Telamon": {
        "HP": 20,
        "Actions": ["Stab", "Block", "Parry"],
        "Damage": 2
    }
}
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

character = {
    "Name": "",
    "HP": 5,
    "Inventory": [],
    "Bruh Power": 0,
    "Actions": ["Search", "Move", "Battle", "Almanac", "Check Inventory"]
}

cleared_rooms = []

length = randint(4, 6)  # Length of room
height = randint(4, 6)  # Width of room
player_pos = [0, 0]  # Player position

"""Function that creates the map"""


def generate_map():
    room = [  # Creating the room layout variable
        [randint(1, 5)]
    ]
    x = 0
    y = 0
    global player_pos
    while x < height:
        while y < length:
            room[x].append(randint(1, 5))  # Creating new row for more rooms
            y += 1
        room.append([randint(1, 5)])  # adding a new row
        y = 0  # reset y
        x += 1  # increment x
    room.pop(-1)  # delete superfluous room
    player_start = randint(0, length - 1)
    room[0][player_start] = 0  # creating a starting room
    room[x - 1][randint(0, length - 1)] = 6  # creating an exit room
    player_pos = [player_start, 0]
    return room


"""Player movement function. Moves player and determines valid input"""


def move():
    global player_pos
    x = 0
    # User input loop
    while x == 0:
        print("What do you want to do?")
        # Copy of DIRECTION list with only valid input
        temp = DIRECTION[::]
        if player_pos[0] == 0:
            temp.remove("left")
        if player_pos[0] == length - 1:
            temp.remove("right")
        if player_pos[1] == height - 1:
            temp.remove("forward")
        if player_pos[1] == 0:
            temp.remove("back")

        print("Your options are the following:")
        for direction in temp:
            print(direction)
        print("Enter 'quit' to exit this menu")
        print("What will you choose?")
        choice = input()
        if choice not in temp and not choice == "quit":  # check if choice is valid
            print("invalid choice")
        elif "quit" in choice:
            x = 1
        else:
            x = 1
            # Seeing what action user chose
            if choice == "forward":
                player_pos[1] += 1
            elif choice == "right":
                player_pos[0] += 1
            elif choice == "left":
                player_pos[0] -= 1
            elif choice == "back":
                player_pos[1] -= 1


"""Printing player actions function. Prints inventory"""


def act():
    print("Your available actions:")
    for item in ITEMS.keys():
        for thing in ITEMS[item].keys():
            print(f'{item}: {thing} {ITEMS[item][thing]}')


game_map = generate_map()  # generate the map
move()
# Game loop
while 1:
    print(f'You are now in a {ROOM_LEGEND[game_map[player_pos[1]][player_pos[0]]][0]} room')
    print(f"{ROOM_LEGEND[game_map[player_pos[1]][player_pos[0]]][1]}\n")
    print("What do you want to do?")
    for action in character["Actions"]:
        print(action)
    print("Enter quit to exit the game")
    choice = input()
    if choice.capitalize() == "Move":
        move()
    elif choice.capitalize() == "Search":
        act()
    elif choice.capitalize() == "Battle":
        act()
    elif choice.capitalize() == "Almanac":
        pass
    elif choice.title() == "Check Inventory":  # capitalize() wont work. Need title()
        act()
    elif choice.capitalize() == "Quit":
        quit()
    else:
        print("Bad input. Try that again.")
    print("\n")
