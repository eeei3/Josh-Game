"""
Joshua
CS 30 Period 1
May 14, 2023
This file contains the module for the player's inventory
"""


class Inventory:
    """Class for the player inventory"""

    def __init__(self):
        self.inventory = ["Fists", "Shield"]
        return

    def check_inv(self):
        """Method for printing player inventory"""
        print(f"You have {len(self.inventory)} "
              f"items in your inventory")
        if len(self.inventory) != 0:
            for item in self.inventory:
                print(f"You have a {item}")

    def add_inv(self, item):
        """Method for adding items to player's inventory"""
        self.inventory.append(item)
