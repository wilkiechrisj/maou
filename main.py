import pygame
import maou
from time import sleep


def start_loop():
    main_loop()


def main_loop():

    while game.active:
        ms = game.clock.tick(game.fps)
        game.timer += ms

        if game.timer > 1500 and game.battle:
            game.timer = 0
            game.damage_calc()
            game.hp_check()

        if not game.battle and not game.active_rooms[0]:
            game.generate_rooms()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN and not game.battle:
                pos = pygame.mouse.get_pos()
                if game.buttons['left'].over(pos):
                    game.enter_room(game.active_rooms[0])
                    if game.enemies:
                        game.hp_check()
                    sleep(1)
                if game.buttons['right'].over(pos):
                    game.enter_room(game.active_rooms[1])
                    if game.enemies:
                        game.hp_check()
                    sleep(1)

            if event.type == pygame.MOUSEBUTTONDOWN and game.battle:
                pos = pygame.mouse.get_pos()
                if game.buttons['pause'].over(pos):
                    print('PAUSE')
                if game.buttons['play'].over(pos):
                    game.wiki_scrape()
            if event.type == pygame.QUIT:
                game.active = False


def end_loop():
    pass


if __name__ == '__main__':
    game = maou.MaouGame()
    start_loop()
