import random
import pygame

from constants import STOCKS, TASKS_TO_TICKS
from utils import xp_needed, roll_loot


# --------------------
# GAME OBJECTS
# --------------------
class Unit:
    def __init__(self):
        self.task = "NONE"
        self.task_timer = 0
        self.level = 1
        self.xp = 0

    def complete_task(self, game_state):
        if self.task == "PLUNDERING":
            game_state.gold += 5

        elif self.task == "MINING":
            game_state.ore += 2

        elif self.task == "LEADING PARTY":
            self.xp += 1

            loot = random.choice(["gold", "ore", "gems"])
            if loot == "gold":
                game_state.gold += 7
            elif loot == "ore":
                game_state.ore += 1
            elif loot == "gems":
                game_state.gems += 1

            if self.xp >= xp_needed(self.level):
                self.xp -= xp_needed(self.level)
                self.level += 1
        elif self.task == "HUNTING":
            enemy = game_state.selected_enemy

            if enemy is None:
                return

            self.xp += 1

            loot = roll_loot(enemy)

            # safety check
            if loot is None:
                return

            if loot == "gold":
                game_state.gold += 7
            else:
                game_state.add_to_inventory(loot)

    def process_tick(self, game_state):
        if self.task == "NONE":
            return

        self.task_timer += 1

        if self.task_timer >= TASKS_TO_TICKS[self.task]:
            self.task_timer = 0
            self.complete_task(game_state)

class Item:
    def __init__(self, name, rarity="common"):
        self.name = name
        self.rarity = rarity
        self.count = 1


class GameState:
    def __init__(self):
        self.screen = "GAME"
        self.gold = 50
        self.ore = 0
        self.gems = 0
        self.stocks ={name: 0 for name in STOCKS}
        self.units = [Unit()]
        self.selected_unit_idx = 0
        self.inventory_size = 16  # 4x4 grid
        self.inventory = [None] * self.inventory_size

        self.enemies = ["goblin", "skeleton", "dragon"]
        self.selected_enemy = None

    def selected_unit(self):
        return self.units[self.selected_unit_idx]


    def add_to_inventory(self, item_name):
        # stack items
        for slot in self.inventory:
            if slot is not None and slot.name == item_name:
                slot.count += 1
                return

        # empty slot
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                self.inventory[i] = Item(item_name)
                return
    

