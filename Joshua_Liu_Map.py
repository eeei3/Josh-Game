# Joshua
# CS 30 Period 1
# March 13, 2023
# This is a simple game that generates a random map and allows movement
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
    },
    "Shield": {
    "Desc": "Simple wood",
    },
    "Gilgamesh": {
        "Desc": ":gilgamesh:",
    },
    "Jerma": {
        "Desc": "Unleash destruction upon your foes",
    },
    "Omega Energy Sword": {
        "Desc": "Super damage!",
    },
    "Gravity Coil": {
        "Desc": "boioioioioioioioioioioinnngggg dtdtdtddt",
    },
    "Speed Coil": {
        "Desc": "vrrrrrrrrrrrrooooooooooooooom",
    }
}
BOSS = {
    "the FACE": {
        "HP": 7,
        "Actions": [],
        "Damage": 7
    },
    "the MOON": {
        "HP": 12,
        "Actions": [],
        "Damage": 3
    },
    "teh epix duck": {
        "HP": 25,
        "Actions": [],
        "Damage": 6
    },
    "Telamon": {
        "HP": 20,
        "Actions": [],
        "Damage": 2
    }
}
ENEMIES = {
    "Goblina": {
        "HP": 3,
        "Actions": [],
        "Damage": 2
    },
    "talking ben": {
        "HP": 1,
        "Actions": [],
        "Damage": 2
    },
    "Jesse": {
        "HP": 5,
        "Actions": [],
        "Damage": 3
    },
    "Mr. White": {
        "HP": 6,
        "Actions": [],
        "Damage": 1
    },
    "Anomaly": {
        "HP": 3,
        "Actions": [],
        "Damage": 5
    }
}
ACTIONS = {

}

character = {
    "Name": "",
    "HP": 5,
    "Inventory": [],
    "Bruh Power": 0
}

length = randint(4, 6)  # Length of room
height = randint(4, 6)  # Width of room\
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
    room[0][randint(0, length - 1)] = 0  # creating a starting room
    room[x -1][randint(0, length - 1)] = 6  # creating an exit room
    player_pos = [player_start, 0]
    return room


game_map = generate_map()  # generate the map
# Game loop
while 1:
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
        print("Enter 'quit' to exit the game")
        print("What will you choose?")
        choice = input()
        if choice not in temp and not choice == "quit":  # check if choice is valid
            print("invalid choice")
        if "quit" in choice:
            quit()
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
    # Print the player's current status
    print(player_pos)
    print(game_map[player_pos[0]][player_pos[1]])
    print(f'You are now in a {ROOM_LEGEND[game_map[player_pos[1]][player_pos[0]]][0]} room')
    print(ROOM_LEGEND[game_map[player_pos[1]][player_pos[0]]][1])
