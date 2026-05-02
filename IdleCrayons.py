import pygame
import sys

from game_objects import Unit, GameState, Item
from constants import TASKS_TO_TICKS, LOOT_TABLES
from utils import xp_needed

pygame.init()

# --------------------
# CONFIG
# --------------------
WIDTH, HEIGHT = 1024, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IdleCrayons")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

TICK_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TICK_EVENT, 1000)


# --------------------
# ITEM ICONS
# --------------------

ITEM_ICONS = {
    "rusty_dagger": pygame.image.load("dagger.png").convert_alpha(),
    "bone": pygame.image.load("bone.png").convert_alpha(),
    "ancient_coin": pygame.image.load("coin.png").convert_alpha(),
    "dragon_scale": pygame.image.load("scale.png").convert_alpha(),
}



game_state = GameState()

# --------------------
# BUTTON SYSTEM
# --------------------
class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

    def draw(self):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        txt = font.render(self.text, True, (255, 255, 255))
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()


buttons = []

def add_button(x, y, w, h, text, callback):
    buttons.append(Button((x, y, w, h), text, callback))

# --------------------
# GAME ACTIONS
# --------------------
def assign_plunder():
    u = game_state.selected_unit()
    u.task = "PLUNDERING"
    u.task_timer = 0

def assign_mining():
    u = game_state.selected_unit()
    u.task = "MINING"
    u.task_timer = 0

def assign_party():
    u = game_state.selected_unit()
    u.task = "LEADING PARTY"
    u.task_timer = 0

def assign_hunt():
    u = game_state.selected_unit()
    u.task = "HUNTING"
    u.task_timer = 0

def buy_unit():
    if game_state.gold >= 50:
        game_state.gold -= 50
        game_state.units.append(Unit())

def upgrade_mining():
    print("Mining upgrade (not implemented)")

def upgrade_plunder():
    print("Plunder upgrade (not implemented)")

def open_shop():
    game_state.screen = "SHOP"
    setup_shop_buttons()

def close_shop():
    game_state.screen = "GAME"
    setup_game_buttons()

def open_inventory():
    game_state.screen = "INVENTORY"
    setup_inventory_buttons()

def close_inventory():
    game_state.screen = "GAME"
    setup_game_buttons()

def open_enemy_screen():
    game_state.screen = "ENEMIES"
    setup_enemy_buttons()

def close_enemy_screen():
    game_state.screen = "GAME"
    setup_game_buttons()

def select_enemy(enemy):
    game_state.selected_enemy = enemy
    game_state.screen = "GAME"
    setup_game_buttons()

    # auto-start hunting
    u = game_state.selected_unit()
    u.task = "HUNTING"
    u.task_timer = 0

# --------------------
# BUTTON SETUP
# --------------------
def setup_game_buttons():
    buttons.clear()

    add_button(20, 280, 180, 50, "PLUNDER", assign_plunder)
    add_button(20, 340, 180, 50, "MINING", assign_mining)
    add_button(20, 400, 180, 50, "PARTY", assign_party)
    add_button(20, 460, 180, 50, "HUNT", open_enemy_screen)
    add_button(20, 520, 180, 50, "SHOP", open_shop)
    add_button(20, 580, 180, 50, "INVENTORY", open_inventory)

def setup_shop_buttons():
    buttons.clear()

    add_button(350, 220, 300, 50, "Buy Unit (50g)", buy_unit)
    add_button(350, 300, 300, 50, "Upgrade Mining", upgrade_mining)
    add_button(350, 380, 300, 50, "Upgrade Plunder", upgrade_plunder)
    add_button(350, 460, 300, 50, "BACK", close_shop)

def setup_inventory_buttons():
    buttons.clear()
    add_button(400, 520, 180, 50, "BACK", close_inventory)

def setup_enemy_buttons():
    buttons.clear()

    y = 200

    for enemy in game_state.enemies:
        add_button(400, y, 200, 40, "FIGHT " + enemy, lambda e=enemy: select_enemy(e))
        y += 60

    add_button(400, 520, 200, 50, "BACK", close_enemy_screen)

setup_game_buttons()

# --------------------
# DRAW FUNCTIONS
# --------------------
def draw_bar(x, y, width, fraction):
    fraction = max(0, min(1, fraction))
    pygame.draw.rect(screen, (80, 80, 80), (x, y, width, 5))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, width * fraction, 5))

def draw_resources():
    screen.blit(font.render(f"Gold: {game_state.gold}", True, (255,255,255)), (20, 20))
    screen.blit(font.render(f"Ore: {game_state.ore}", True, (255,255,255)), (20, 50))
    screen.blit(font.render(f"Gems: {game_state.gems}", True, (255,255,255)), (20, 80))

def draw_units():
    for i, u in enumerate(game_state.units):
        x = 300 + i * 140

        pygame.draw.rect(screen, (200, 200, 200), (x-20, 280, 40, 40))

        if i == game_state.selected_unit_idx:
            pygame.draw.rect(screen, (255, 0, 0), (x-22, 278, 44, 44), 2)

        screen.blit(font.render(u.task, True, (255,255,255)), (x-30, 330))
        screen.blit(font.render(f"Lvl {u.level}", True, (255,255,255)), (x-30, 360))

        xp = f"{u.xp} / {xp_needed(u.level)}"
        screen.blit(font.render(xp, True, (255,255,255)), (x-30, 380))

        if u.task in TASKS_TO_TICKS:
            prog = u.task_timer / TASKS_TO_TICKS[u.task]
            draw_bar(x-20, 400, 40, prog)

def draw_shop():
    screen.blit(font.render("SHOP", True, (255,255,255)), (450, 100))

def draw_inventory():
    screen.fill((15, 15, 15))

    # Title
    screen.blit(font.render("INVENTORY", True, (255, 255, 255)), (430, 40))

    # Grid settings
    start_x = 350
    start_y = 120
    size = 64
    cols = 4
    padding = 12

    # Draw slots
    for i, slot in enumerate(game_state.inventory):
        x = start_x + (i % cols) * (size + padding)
        y = start_y + (i // cols) * (size + padding)

        pygame.draw.rect(screen, (40, 40, 40), (x, y, size, size))
        pygame.draw.rect(screen, (120, 120, 120), (x, y, size, size), 2)

        if slot:
            icon = ITEM_ICONS[slot.name]

            if icon:
                icon_scaled = pygame.transform.scale(icon, (40, 40))
                screen.blit(icon_scaled, (x + 12, y + 10))

            # badge background
            pygame.draw.circle(screen, (0, 0, 0), (x + size - 10, y + size - 10), 10)

            count_text = font.render(str(slot.count), True, (255, 255, 255))
            screen.blit(count_text, (x + size - 16, y + size - 18))

    screen.blit(font.render("BACK", True, (255, 255, 255)), (470, 520))

def draw_enemies():
    screen.blit(font.render("ENEMIES", True, (255,255,255)), (450, 80))

    y = 200
    for enemy in game_state.enemies:
        color = (0, 255, 0) if enemy == game_state.selected_enemy else (255, 255, 255)
        screen.blit(font.render(enemy, True, color), (420, y))
        y += 60

# --------------------
# INPUT
# --------------------
def handle_click(pos):
    for b in buttons:
        b.handle_click(pos)

    if game_state.screen == "GAME":
        for i, u in enumerate(game_state.units):
            x = 300 + i * 140
            if x-20 <= pos[0] <= x+20 and 280 <= pos[1] <= 320:
                game_state.selected_unit_idx = i

# --------------------
# MAIN LOOP
# --------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

        elif event.type == TICK_EVENT:
            for u in game_state.units:
                u.process_tick(game_state)

    screen.fill((0, 0, 0))

    if game_state.screen == "GAME":
        draw_resources()
        draw_units()

    elif game_state.screen == "SHOP":
        draw_shop()

    elif game_state.screen == "INVENTORY":
        draw_inventory()

    elif game_state.screen == "ENEMIES":
        draw_enemies()

    for b in buttons:
        b.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
