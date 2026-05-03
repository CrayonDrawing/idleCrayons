import random

TASKS_TO_TICKS = {
    "PLUNDERING": 1,
    "MINING": 2,
    "LEADING PARTY": 1,
    "HUNTING": 4
}

LOOT_TABLES = {
    "goblin": [
        ("gold", 70),
        ("rusty_dagger", 30),
    ],

    "skeleton": [
        ("bone", 60),
        ("gold", 30),
        ("ancient_coin", 10),
    ],

    "dragon": [
        ("gold", 40),
        ("gem", 40),
        ("dragon_scale", 20),
    ]
}

STOCKS = {
    "HolardCoin": {
        "price": 190,
        "volatility": 170,
        "ticks": 0,
        "ticks_to_update": 1
    },
    "CDRW": {
        "price": 520,
        "volatility": 75,
        "ticks": 0,
        "ticks_to_update": 5
    },
    "AppleBees": {
        "price": 125,
        "volatility": 11,
        "ticks": 0,
        "ticks_to_update": 5
        }
}