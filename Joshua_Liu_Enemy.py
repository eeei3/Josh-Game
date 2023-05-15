"""
Joshua
CS 30 Period 1
May 14, 2023
This file contains the module for enemies in
"""
from random import *


class EnemyActions:
    """Class for Enemy actions"""

    def __init__(self):
        self.playeraction = False  # Is it the player's turn to move?
        self.engaged = None
        self.number = 0
        self.engage = False

    def counter(self, eenemy=None):
        """Function in charge of executing enemy action"""
        if eenemy is not None:
            eenemy.baction()


class Enemy:
    """Class for Enemies"""

    def __init__(self, name, stats, position, target):
        self.name = name  # Enemy name
        self.stats = stats  # Enemy stats
        self.position = position  # Enemy position on map
        self.hp = stats["HP"]  # Enemy HP
        self.action = stats["Actions"]  # Enemy attack
        self.Damage = stats["Damage"]  # Enemy damage
        self.boss = False  # Easier knowledge if enemy is boss or not
        self.target = target  # Enemy access to player object

    def baction(self):
        """Method that handles enemy actions"""
        # Dice roll for enemy attack
        if randint(1, 5) == randint(1, 5):
            print(f"{self.name} used {self.action[0]}!")
            print(f"You took {self.Damage} damage!")
            # Subtract player health
            self.target.take_damage(self.Damage)
        else:
            print(f"{self.name} failed to attack! Your move!")
        # Dice roll for enemy healing
        if randint(1, 40) == randint(1, 20):
            print(f"{self.name} is healing!")
            self.heal(randint(1, 3))  # Heal random amount for enemy

    def heal(self, amount):
        """Method that handles enemy healing"""
        self.hp += amount
        return

    def take_dmg(self, dmg):
        """Method that handles enemy taking damage"""
        self.hp -= dmg


class Boss(Enemy):
    """Class for Bosses"""
    def __init__(self, name,  stats, position, target):
        super().__init__(name, stats, position, target)
        # List of enemy actions options
        self.actions = ["Attack", "Super Attack", "Heal", "Defend"]
        self.activated = True  # Is the boss active?
        self.blocking = False  # Is the boss blocking attacks?
        self.boss = True
        self.superattacked = False  # Has the boss super attacked?

    def take_dmg(self, dmg):
        """Method that handles enemy taking damage"""
        if not self.blocking:
            self.hp -= dmg
        else:
            print("Boss blocked your attack!")
            self.blocking = False

    def baction(self):
        """Method handling boss actions"""
        self.panic()
        if randint(1, 2) == randint(1, 2):
            choice = self.actions[randint(0, 3)]
            if choice == "Attack":
                self.attack()
            elif choice == "Defend":
                print("\nBoss is hunkering down!")
                self.blocking = True
            elif choice == "Heal":
                print("\nBoss is rapidly recovering!")
                self.heal(randint(4, 6))
            elif choice == "Super Attack":
                self.super_attack()
        else:
            print("BOSS failed move! Strike back!")

    def attack(self):
        """Method handling boss attack"""
        print(f"\n{self.name} used {self.action[0]}!")
        print(f"You took {self.Damage} damage!")
        if self.superattacked:
            self.target.take_damage(self.Damage//2)
        else:
            self.target.take_damage(self.Damage)

    def super_attack(self):
        """Method handling boss super attack"""
        # Checking if the boss has super attacked
        if self.superattacked:
            # Dice roll to super attack
            if randint(1, 9) == randint(1, 9):
                print("\nBOSS is amping up his attack!")
                print(f"{self.name} used {self.action[0]}!")
                print(f"You took {self.Damage*2} damage!")
                self.target.take_damage(self.Damage * 2)
                self.superattacked = True
            else:
                print(f"{self.name} failed to attack! Your move!")
        else:
            # Dice roll to super attack
            if randint(1, 2) == randint(1, 2):
                print("\nBOSS is amping up his attack!")
                print(f"{self.name} used {self.action[0]}!")
                print(f"You took {self.Damage} damage!")
                self.target.take_damage(self.Damage)
            else:
                print(f"{self.name} failed to attack! Your move!")

    def panic(self):
        """Method handling boss panic functionality"""
        if 3 > self.hp > 0:  # Checking panic conditions
            print("\nThe BOSS is unleashing its fury!")
            self.super_attack()
            self.baction()
            self.heal(8)
