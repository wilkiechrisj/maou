import pygame
from tkinter import messagebox
from tkinter import *
import entities
from buttons import Button
from random import randint, choices
from copy import deepcopy
import micros


class MaouGame:

    def __init__(self):

        pygame.init()
        pygame.font.init()

        self.units = {
            'ENEMY_1': (1000, 90),
            'ENEMY_2': (850, 90),
            'ENEMY_3': (700, 90),
            'BOSS': (700, 90),
            'PLAYER': (200, 90)
        }

        self.buttons = {
            'left': Button(65, 640, 111, 56),
            'right': Button(275, 640, 111, 56),
            'pause': Button(890, 640, 111, 56),
            'play': Button(1100, 640, 111, 56),
            'info': None,
            'wiki': None,
            'buy_1': None,
            'buy_2': None,
            'buy_3': None,
            'buy_4': None,
            'cast_1': None,
            'cast_2': None,
            'cast_3': None,
            'cast_4': None
        }

        self.name = 'MAOU'
        self.screen = pygame.display.set_mode((1280, 720))
        self.font = pygame.font.SysFont('Comic Sans MS', 28)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.timer = 0

        self.active = True
        self.battle = False
        self.camp = True
        self.shop = False

        self.player = entities.Player()
        self.enemies = []

        self.rooms = ['CAMP', 'SHOP', 'MINION', 'BOSS']
        self.room_weight = [25, 25, 40, 10]
        self.active_rooms = [None, None]

        self.enemy_pool = [entities.Wolf(), entities.Rat(), entities.Zombie()]
        self.boss_pool = [entities.Dragon()]

        self.music_mp4 = 'resources/bensound-epic.mp3'

        self.icon_img = pygame.image.load('resources/icon.png')
        self.bg_img = pygame.image.load('resources/background.png')
        self.minion_img = pygame.image.load('resources/vile-fluid.png')
        self.boss_img = pygame.image.load('resources/brute.png')
        self.camp_img = pygame.image.load('resources/camping-tent.png')
        self.shop_img = pygame.image.load('resources/play.png')  # HELP

        self.player_img = pygame.image.load('resources/maou.png')
        self.rat_img = pygame.image.load('resources/rat.png')
        self.zombie_img = pygame.image.load('resources/zombie.png')
        self.wolf_img = pygame.image.load('resources/wolf.png')
        self.dragon_img = pygame.image.load('resources/dragon.png')

        self.left_btn = pygame.image.load('resources/left.png')
        self.right_btn = pygame.image.load('resources/right.png')
        self.pause_btn = pygame.image.load('resources/pause.png')
        self.play_btn = pygame.image.load('resources/play.png')
        self.info_btn = pygame.image.load('resources/play.png')  # HELP
        self.wiki_btn = pygame.image.load('resources/play.png')  # HELP
        self.dmg_spell_btn = pygame.image.load('resources/play.png')  # HELP
        self.heal_spell_btn = pygame.image.load('resources/play.png')  # HELP

        self.img_lib = {
            'Maou': self.player_img,
            'Rat': self.rat_img,
            'Zombie': self.zombie_img,
            'Wolf': self.wolf_img,
            'Dragon': self.dragon_img
        }

        pygame.display.set_caption(self.name)
        pygame.mixer.music.load(self.music_mp4)
        pygame.display.set_icon(self.icon_img)
        pygame.mixer.music.play(-1, 0)
        self.draw_background(self.bg_img)
        self.draw_buttons()
        self.draw_spells()
        self.hp_check()

    def draw_background(self, img):

        self.screen.blit(img, (0, 0))
        pygame.display.flip()

    def draw_units(self):

        self.screen.blit(self.player_img, self.units['PLAYER'])

        if len(self.enemies) == 3:
            for index in range(0, len(self.enemies)):
                location = self.enemies[index].type + '_' + str(index + 1)
                self.screen.blit(self.img_lib[self.enemies[index].name], self.units[location])
        if len(self.enemies) == 1:
            location = self.enemies[0].type
            self.screen.blit(self.img_lib[self.enemies[0].name], self.units[location])

        pygame.display.flip()

    def draw_rooms(self):

        x, y = 75, 500

        for room in self.active_rooms:
            if room == 'CAMP':
                self.screen.blit(self.camp_img, (x, y))
            if room == 'SHOP':
                self.screen.blit(self.shop_img, (x, y))
            if room == 'BOSS':
                self.screen.blit(self.boss_img, (x, y))
            if room == 'MINION':
                self.screen.blit(self.minion_img, (x, y))

            x += 200

        pygame.display.flip()

    def draw_buttons(self):

        self.screen.blit(self.left_btn, (65, 640))
        self.screen.blit(self.right_btn, (275, 640))
        self.screen.blit(self.pause_btn, (890, 640))
        self.screen.blit(self.play_btn, (1100, 640))
        self.screen.blit(self.info_btn, (0, 0))  # HELP
        self.screen.blit(self.wiki_btn, (0, 0))  # HELP
        pygame.display.flip()

    def draw_shop(self):
        pass

    def draw_spells(self):
        pass

    def generate_enemies(self, boss):

        self.enemies = []

        if boss:
            self.enemies.append(deepcopy(self.boss_pool[randint(0, len(self.boss_pool) - 1)]))
        else:
            for num in range(3):
                self.enemies.append(deepcopy(self.enemy_pool[randint(0, len(self.enemy_pool) - 1)]))

        self.draw_units()

    def generate_rooms(self):

        while self.active_rooms[0] == self.active_rooms[1]:
            self.active_rooms = choices(self.rooms, weights=self.room_weight, k=2)

        self.draw_rooms()

    def enter_room(self, room):

        self.draw_background(self.bg_img)
        self.draw_buttons()

        if room == 'CAMP':
            self.enter_camp()
            self.player.cur_health = min(self.player.cur_health + 20, 50)
            self.hp_check()
        if room == 'SHOP':
            self.enter_shop()
        if room == 'MINION':
            self.enter_battle()
            self.generate_enemies(False)
        if room == 'BOSS':
            self.enter_battle()
            self.generate_enemies(True)

        self.active_rooms = [None, None]

    def enter_camp(self):

        self.camp = True
        self.shop = False
        self.battle = False

    def enter_shop(self):

        self.camp = False
        self.shop = True
        self.battle = False

    def enter_battle(self):

        self.camp = False
        self.shop = False
        self.battle = True

    def damage_calc(self):

        for enemy in self.enemies:
            if enemy.health > 0:

                self.player.cur_health -= enemy.attack - self.player.defense
                enemy.health -= self.player.attack - enemy.defense

                effect = enemy.ability()
                if type(effect) is int:
                    self.player.cur_health -= effect
                if type(effect) is str:
                    self.player.debuffs.append(effect)

                if enemy.health <= 0:
                    enemy.health = 0

        if self.player.cur_health <= 0:
            self.player.cur_health == 0

    def hp_check(self):

        x, y = 900, 320

        pygame.draw.rect(self.screen, (192, 192, 192), pygame.Rect(x, y, 300, 300))

        if self.player.cur_health <= 0:
            self.game_over()
            return

        text = self.font.render('Maou: ' + str(self.player.cur_health) + '/' +
                                str(self.player.max_health), False, (0, 0, 0))
        self.screen.blit(text, (x, y))
        y += 100

        for enemy in self.enemies:
            text = self.font.render(enemy.name + ': ' + str(enemy.health), False, (0, 0, 0))
            self.screen.blit(text, (x, y))
            y += 50

        pygame.display.flip()

        if all(enemy.health <= 0 for enemy in self.enemies):
            self.battle = False
            for enemy in self.enemies:
                self.player.score += enemy.value
                self.player.gold += enemy.value

    def game_over(self):

        self.active = False
        self.battle = False
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 0, 1280, 720))

        over = pygame.font.SysFont('Comic Sans MS', 70)
        text = over.render('GAME OVER', False, (255, 0, 0))
        self.screen.blit(text, (440, 250))

        score = pygame.font.SysFont('Comic Sans MS', 70)
        text = score.render('SCORE: ' + str(self.player.score), False, (255, 255, 0))
        self.screen.blit(text, (470, 350))

        pygame.display.flip()

    def wiki_scrape(self):

        names = []

        for unit in self.enemies:
            if unit.name not in names:
                names.append(unit.name)

        Tk().wm_withdraw()

        res = messagebox.askquestion('Language', '¿Necesitas en Español?')
        if res == 'yes':
            data = micros.wiki_scrape_translate(names, 'es')
        else:
            data = micros.wiki_scrape_translate(names)

        messagebox.showinfo('ENEMY INFO', data)