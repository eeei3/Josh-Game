from random import *

length = randint(4, 6)
height = randint(4, 6)

room_legend = ["Index", "Treasure Room", "Trap Room", "Monster Room", "Regular Room", "Exit", "Boss"]


def generate_map():
    room = [
        [0]
    ]
    x = 0
    y = 0
    while x < height:
        while y < length:
            if y == 0:
                room[x][y] = randint(0, 5)
            else:
                room[x].append(randint(0, 5))
            y += 1
        room.append([0])
        y = 0
        x += 1
    return room


game_map = generate_map()
print(game_map)
print(length)
print(height)