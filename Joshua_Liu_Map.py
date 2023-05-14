"""
Joshua
CS 30 Period 1
May 14, 2023
This file contains the module for the Game map
"""
from Joshua_Liu_Game_Functions import GameModules
from Joshua_Liu_Enemy import Enemy, Boss
from random import *


class GameMap:
    def __init__(self):
        return

    def enter(self):
        """
        Method handling for when entering room
        """
        self.inroom = True  # Setting player as in room
        # Is this the first time player has entered room?
        if self.first:
            self.first = False  # No longer first time
            print("\nYou have discovered a new room")
            print(f"You are now in a {self.roomtype[0]}")
            # Events for Monster Room
            if self.roomtype[0] == "Monster Room":
                # Create random enemy object
                enemyname = GameModules.ENEMIESLIST[randint(0, 4)]
                enemy = Enemy(enemyname, GameModules.ENEMIES[enemyname],
                              [self.pos[1], self.pos[0]],
                              self.character)
                print(f"You have encountered a {enemy.name}")
                # Setting player as engaged against enemy
                EnemyMovement.engaged = enemy
                # Setting player as engaged
                EnemyMovement.engage = True
                # Setting enemy in room as this enemy
                self.enemie = enemy
            # Events for Boss Room
            elif self.roomtype[0] == "Boss Room":
                print("Entering boss room")
                # Create random boss object
                enemyname = GameModules.BOSSLIST[randint(0, 3)]
                enemy = Boss(enemyname, GameModules.BOSS[enemyname],
                             [self.pos[1], self.pos[0]], self.character)
                print(f"You have encountered a {enemy.name}")
                # Setting player as engaged against boss
                EnemyMovement.engaged = enemy
                # Setting player as engaged
                EnemyMovement.engage = True
                # Setting enemy in room as this boss
                self.enemie = enemy
            # Events for Trap Room
            elif self.roomtype[0] == "Trap Room":
                self.trap()  # Triggering trap
            # Events for Regular and Index Room
            elif self.roomtype[0] == "Regular Room" or\
                    self.roomtype == "Index Room":
                return
            # Events for Treasure Room
            elif self.roomtype[0] == "Treasure Room":
                # Spawning treasure
                treasure = randint(0, 4)  # index in list
                itemlist = []  # list of spawnable items
                for key in self.ITEMS:
                    itemlist.append(key)
                self.items.append(itemlist[treasure])
                # Chance for a second treasure to spawn in
                if randint(0, 4) == 1:
                    treasure = randint(0, 4) # index in list
                    itemlist = [] # list of spawnable items
                    for key in self.ITEMS:
                        itemlist.append(key)
                    self.items.append(itemlist[treasure])
            # Events for Exit
            elif self.roomtype[0] == "Exit Room":
                print("\nYou feel a need to be here")
                self.character.actions.append("Leave Dungeon")
                return
        # This is NOT the first time player has been in room
        else:
            print(f"You are now in a {self.roomtype[0]}")
            # Events for Monster Room
            if self.roomtype[0] == "Monster Room":
                # Is there still an enemy here?
                if self.enemie is not None:
                    # Is the enemy dead?
                    if self.enemie.hp > 0:  # No
                        print(self.enemie.hp)
                        print(f"\nYou have encountered a "
                              f"{self.enemie.name}")
                        EnemyMovement.engaged = self.enemie
                        EnemyMovement.engage = True
                    else:  # Yes
                        del self.enemie  # Deleting enemy object
                        self.enemie = None
                else:
                    pass
            # Events for Boss Room
            elif self.roomtype[0] == "Boss Room":
                print("Entering boss room")
                if self.enemie is not None:
                    # Has the boss in the room died?
                    if self.enemie.hp > 0:  # No
                        print(self.enemie.hp)
                        print(f"\nYou have encountered a "
                              f"{self.enemie.name}")
                        EnemyMovement.engaged = self.enemie
                        EnemyMovement.engage = True
                    else:  # Yes
                        del self.enemie  # Deleting boss object
                        self.enemie = None
            # Events for Trap Room
            elif self.roomtype[0] == "Trap Room":
                self.trap()
            # Events for Regular and Index Room
            elif self.roomtype[0] == "Regular Room" or \
                    self.roomtype == "Index Room":
                return
            # Events for Treasure Room
            elif self.roomtype[0] == "Treasure Room":
                return
            # Events for Exit Room
            elif self.roomtype[0] == "Exit":
                self.character.actions.append("Leave Dungeon")
                return
            else:
                return