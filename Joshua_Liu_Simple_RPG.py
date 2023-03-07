import random
from ctypes import *

rooms = [{c_char_p("Room00"): "Index", "Right": "", "Left": "", "Forward": "", "Back": "NULL"}]
player = {"HP": 5, "Inventory": [], "CurrentRoom": pointer(rooms[0]["Room00"])}

while True:
    print("You are in a brick maze, what do you do?")
    action = input("Your options are 'move' and 'search' and 'quit'")
    if action.capitalize() == "move":
        print("Which direction do you want to? Forward, Right, Left, Back")
        direction = input("")
        if direction == "Forward":
            print("You forge ahead!")
        elif direction == "Right":
            print()
        elif direction == "Left":
            print()
        elif direction == "Back":
            print()
        else:
            print("Are you retarded?")
    if action.capitalize() == "search":
        print("Searching the nearby area.")
        print("Choose a number between 1-25 inclusive")
        usernum = input()
        while not usernum.isnumeric():
            print("Bad input! Try again")
            usernum = input()
        if int(usernum) == random.randrange(1, 25):
            print("You found an item!")
            if "Key" in player["Inventory"]:
                item_found = random.randrange(1, 4)
            else:
                item_found = random.randrange(1, 5)
            if item_found == 1:
                print("You found a 1up!")
                player["HP"] += 1
            elif item_found == 2:
                print("You found a magic staff!")
                player["Inventory"].append("Magic Staff")
            elif item_found == 3:
                print("You found a shield!")
                player["Inventory"].append("Shield")
            elif item_found == 4:
                print("You found a iron sword!")
                player["Inventory"].append("Iron Sword")
            elif item_found == 5:
                print("You found the key!")
                player["Inventory"].append("Key")
            else:
                print("This should be impossible! You found the super heroin")
                print("You overdosed and died")
                quit()
    elif action.capitalize() == "Quit":
        quit()

    else:
        print("Do you enjoy being a professional thumb twiddler?")
