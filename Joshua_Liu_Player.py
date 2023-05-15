"""
Joshua
CS 30 Period 1
May 14, 2023
This file contains the module for the player in the game
"""
import random
import Joshua_Liu_Inventory


class Player:
    """Class for the player"""
    def __init__(self, name, hp, pos, inventory=None):
        self.name = name  # Name of player
        self.hp = hp  # Player health
        # Initial inventory
        self.inventory = Joshua_Liu_Inventory.Inventory()
        # List of actions player can take
        self.actions = ["Search", "Move", "Battle",
                        "Check Inventory", "Checkup"]
        # Player position
        self.pos = pos
        # Room that player is currently in
        # Also gives player object access to room object
        self.room = None
        self.blocking = False
        # Checking if Player class was passed an argument for inventory
        # During initialization
        if inventory is None:
            pass
        else:
            self.inventory = inventory

    def take_damage(self, dmg):
        """Method for handling player taking damage"""
        # Checking if the player is blocking or not
        if not self.blocking:
            self.hp -= dmg
        else:
            print("You blocked the attack!")
            self.blocking = False
        # Checking if the player has died or not
        if self.hp <= 0:
            print("You died!")
            quit()

    def search(self):
        """Method for handling searching rooms for treasure"""
        # Checking if room has any items at all
        if len(self.room.items) != 0:
            # Dice roll to see if player finds anything
            if random.randint(1, 5) == random.randint(1, 5):  # Success
                # Index for item that player found
                itemnum = random.randint(0, len(self.room.items) - 1)
                # Print item that player found
                print(f"You found an {self.room.items[itemnum]}")
                print(f"Desc: "
                      f"{self.room.ITEMS[self.room.items[itemnum]]['Desc']}")
                # Append item to player inventory
                self.inventory.add_inv(self.room.items[itemnum])
                self.room.items.pop(itemnum)  # Remove item from room
            else:  # Player found nothing
                print("You found nothing. Better next time chump!")
        else:  # No items in room
            print("You scour the ground, "
                  "but there isn't even a dust speck to pick up!")
