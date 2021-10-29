import pygame
from tkinter import messagebox
from tkinter import *
import entities
from buttons import Button
from random import randint, choices
from copy import deepcopy

GAME = 'MAOU'
WINDOW = (1280, 720)

BLACK = (0, 0, 0)
BROWN = (150, 75, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 0, 255)
GREY = (192, 192, 192)

ENEMY_ONE = (1000, 65, 100, 200)
ENEMY_TWO = (850, 65, 100, 200)
ENEMY_THREE = (700, 65, 100, 200)
BOSS = (700, 65, 400, 200)
PLAYER = (200, 65, 100, 200)

ENEMY_UNITS = (entities.Wolf(), entities.Slime(), entities.Zombie())
ENEMY_NUM = 3

BOSS_UNITS = (entities.Dragon(), entities.Dragon())
BOSS_NUM = 1

ROOMS = ['MINION', 'BOSS', 'CAMP']
WEIGHTS = [70, 10, 20]

CLOCK = pygame.time.Clock()
FPS = 60

ICON = pygame.image.load('resources/icon.png')
# https://www.nicepng.com/downpng/u2w7e6u2r5e6a9u2_pixilart-simple-by-lazergaming-pixel-sword/
MUSIC = 'resources/bensound-epic.mp3'
# https://www.bensound.com/royalty-free-music/track/epic
BATTLE_BACKGROUND = pygame.image.load('resources/background.png')
# https://craftpix.net/freebies/free-pixel-art-fantasy-2d-battlegrounds/
MINION_ICON = pygame.image.load('resources/vile-fluid.png')
# https://game-icons.net/1x1/lorc/vile-fluid.html#download
BOSS_ICON = pygame.image.load('resources/brute.png')
# https://game-icons.net/1x1/delapouite/brute.html#download
CAMP_ICON = pygame.image.load('resources/camping-tent.png')
# https://game-icons.net/1x1/delapouite/camping-tent.html#download

LEFT = pygame.image.load('resources/left.png')
RIGHT = pygame.image.load('resources/right.png')
PAUSE = pygame.image.load('resources/pause.png')
PLAY = pygame.image.load('resources/play.png')


def background(bg):
    screen.blit(bg, (0, 0))
    pygame.display.flip()


def draw_enemies(enemies):

    count = -1
    shape = [ENEMY_ONE, ENEMY_TWO, ENEMY_THREE]

    for unit in enemies:

        count += 1

        if unit.name == 'Slime':
            pygame.draw.rect(screen, YELLOW, pygame.Rect(shape[count]))
            pygame.display.flip()
        if unit.name == 'Wolf':
            pygame.draw.rect(screen, BROWN, pygame.Rect(shape[count]))
            pygame.display.flip()
        if unit.name == 'Zombie':
            pygame.draw.rect(screen, GREEN, pygame.Rect(shape[count]))
            pygame.display.flip()
        if unit.name == 'Dragon':
            pygame.draw.rect(screen, PINK, pygame.Rect(BOSS))
            pygame.display.flip()


def generate_enemies():

    units = []

    for num in range(3):
        units.append(deepcopy(ENEMY_UNITS[randint(0, ENEMY_NUM - 1)]))

    draw_enemies(units)

    return units


def generate_boss():

    units = []

    for num in range(1):
        units.append(deepcopy(BOSS_UNITS[randint(0, BOSS_NUM - 1)]))

    draw_enemies(units)

    return units


def generate_rooms():

    x, y = 75, 500
    rand_rooms = choices(ROOMS, weights=WEIGHTS, k=2)

    for name in rand_rooms:
        if name == 'CAMP':
            screen.blit(CAMP_ICON, (x, y))
        if name == 'BOSS':
            screen.blit(BOSS_ICON, (x, y))
        if name == 'MINION':
            screen.blit(MINION_ICON, (x, y))
        x += 200

    pygame.display.flip()

    return rand_rooms[0], rand_rooms[1]


def enter_room(room):

    if room == 'CAMP':
        player.cur_health = min(player.cur_health + 20, 50)
        hp_check()
        return False
    if room == 'MINION':
        return generate_enemies()
    if room == 'BOSS':
        return generate_boss()


def draw_combat_btns():

    left_btn = Button(65, 640, 111, 56)
    screen.blit(LEFT, (65, 640))

    right_btn = Button(275, 640, 111, 56)
    screen.blit(RIGHT, (275, 640))

    pause_btn = Button(890, 640, 111, 56)
    screen.blit(PAUSE, (890, 640))

    play_btn = Button(1100, 640, 111, 56)
    screen.blit(PLAY, (1100, 640))

    pygame.display.flip()

    return left_btn, right_btn, pause_btn, play_btn




def damage(units):

    for enemy in units:
        if enemy.health > 0:

            player.cur_health -= enemy.attack - player.defense
            enemy.health -= player.attack - enemy.defense

            effect = enemy.ability()
            if type(effect) is int:
                player.cur_health -= effect
            if type(effect) is str:
                player.debuffs.append(effect)

            if enemy.health <= 0:
                enemy.health == 0

    if player.cur_health <= 0:
        player.cur_health == 0


def hp_check(units=[]):

    x = 900
    y = 320

    pygame.draw.rect(screen, GREY, pygame.Rect(x, y, 300, 300))

    if player.cur_health <= 0:
        game_over()
        return True

    text = FONT.render('Maou: ' + str(player.cur_health) + '/' + str(player.max_health), False, BLACK)
    screen.blit(text, (x, y))
    y += 100

    for enemy in units:
        text = FONT.render(enemy.name + ': ' + str(enemy.health), False, BLACK)
        screen.blit(text, (x, y))
        y += 50

    pygame.display.flip()

    if all(enemy.health <= 0 for enemy in units):
        for enemy in units:
            player.score += enemy.value
        return False

    return True


def game_over():

    pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, 1280, 720))

    over = pygame.font.SysFont('Comic Sans MS', 70)
    text = over.render('GAME OVER', False, RED)
    screen.blit(text, (440, 250))

    score = pygame.font.SysFont('Comic Sans MS', 70)
    text = score.render('SCORE: ' + str(player.score), False, YELLOW)
    screen.blit(text, (470, 350))

    pygame.display.flip()


def wiki_scrape(units, language):
    Tk().wm_withdraw()
    messagebox.showinfo('Enemy Info', "This is where wiki scrape info on what enemies you're facing will go.\n"
                                      "Translation of all this text will be provided by another microservice. \n"
                                      "You will be able to pick your language at the home page.")

# ---- GAME STARTS HERE ---- #
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Comic Sans MS', 28)

screen = pygame.display.set_mode(WINDOW)
pygame.display.set_caption(GAME)
pygame.mixer.music.load(MUSIC)
pygame.display.set_icon(ICON)
pygame.mixer.music.play(-1, 0)
background(BATTLE_BACKGROUND)
timer = 0
battle = False
generated = False
enemies = None
pygame.draw.rect(screen, BLUE, pygame.Rect(PLAYER))
pygame.display.flip()
player = entities.Player()
hp_check()
left, right, pause, play = draw_combat_btns()





running = True
while running:

    ms = CLOCK.tick(FPS)
    timer += ms

    if timer > 1500 and battle:
        timer = 0
        damage(enemies)
        battle = hp_check(enemies)

    if not battle and not generated:
        left_room, right_room = generate_rooms()
        generated = True
        enemies = None

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and not battle:
            pos = pygame.mouse.get_pos()
            if left.over(pos):
                enemies = enter_room(left_room)
                generated = False
            if right.over(pos):
                enemies = enter_room(right_room)
                generated = False
        if event.type == pygame.MOUSEBUTTONDOWN and battle:
            pos = pygame.mouse.get_pos()
            if pause.over(pos):
                print('PAUSE')
            if play.over(pos):
                wiki_scrape(enemies, 'english')
        if enemies:
            battle = True
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
