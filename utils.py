import random

from constants import TASKS_TO_TICKS, LOOT_TABLES

# --------------------
# UTILS
# --------------------
def xp_needed(level):
    return level * 10

def roll_loot(enemy):
    table = LOOT_TABLES[enemy]
    if not table:
        return None

    total = sum(weight for item, weight in table)
    roll = random.randint(1, total)

    for item, weight in table:
        roll -= weight
        if roll <= 0:
            return item

