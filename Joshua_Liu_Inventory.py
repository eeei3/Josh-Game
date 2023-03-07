inventory_database = \
    {"Inv1":
        {
             "Bruh": "Bruhs",
             "Bruh1": "Bruhs louder",
             "Bruh2": "Louder Bruh",
             "Bruh3": "Loudest Bruh. Theoretically impossible"
         },
     "Inv2":
         {
             "Joe": "Just a average joe",
             "Bob": "Darnnit bobby",
             "Gilgamesh": ":gilgamesh:",
             "Jerma": "Unleash destruction upon your foes"
         }
     }

print("A savage snuffaluphagus confronts you! What will you do!?!?!")
choice = input("You can choose between Inventory 1 and Inventory 2 for actions")

if choice.capitalize() == "Inventory 1":
    print("You have the following tools at your disposal")
    for key in inventory_database["Inv1"]:  # Getting list of player's options
        print(f'{key} | Description: {inventory_database["Inv1"][key]}')
    print("Make your choice!")
    choice = input("")
    options = list(inventory_database["Inv1"].keys())  # Making a list of player's options
    for item in options:
        if item == choice.capitalize():
            print(f"You used {item}")
            # Seeing if the player lived
            if inventory_database["Inv1"][item] == "Louder Bruh" \
                    or inventory_database["Inv1"][item] == "Loudest Bruh. Theoretically impossible":
                print("You bruhhed away the snuffaluphagus!")
                quit()
            else:
                print("You died lmao")
                quit()

    print("You squandered your move! You died lmao")  # you gave bad input

elif choice.capitalize() == "Inventory 2":
    print("You have the following tools at your disposal")
    for key in inventory_database["Inv2"]:  # Getting list of player's options
        print(f'{key} | Description: {inventory_database["Inv2"][key]}')
    print("Make your choice!")
    choice = input("")
    options = list(inventory_database["Inv2"].keys())  # Making a list of the player's options
    for item in options:
        if item == choice.capitalize():
            print(f"You used {item}")
            # Seeing if the player lived
            if inventory_database["Inv2"][item] == ":gilgamesh:" \
                    or inventory_database["Inv2"][item] == "Unleash destruction upon your foes":
                print("You destroyed that snuffaluphagus!")
                quit()
            else:
                print("You died lmao")
                quit()

    print("You squandered your move! You died lmao")
