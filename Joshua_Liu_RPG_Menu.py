# Joshua
# CS 30 Period 1
# March 9, 2023
# This is a simple RPG menu
while True:
    # Give the user their options
    print("What do you want to do?")
    print("1. Bruh\n2. Snuffaluphagus\n3. Die\n4. Run\n5. Quit")
    # Get the user's input
    choice = input("Please input the number for the action")
    # Check if the user input anything other than a number
    if not choice.isnumeric():
        print("U are stoopid! Try again!\n\n")
    else:
        # Check the user's input if it corresponds with an action
        if int(choice) == 1:
            print("You bruhhed so hard you were reduced to atoms")
        elif int(choice) == 2:
            print("You have been raptured")
        elif int(choice) == 3:
            print("You died")
        elif int(choice) == 4:
            print("You didnt tie your shoelace and tripped and died")
        elif int(choice) == 5:
            quit()
        else:
            print("Bad input!\n\n")