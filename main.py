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

        if not game.active:
            return end_loop()

        if not game.battle and not game.active_rooms[0]:
            game.generate_rooms()

        for event in pygame.event.get():

            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN and not game.battle:
                print(pos)
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
                if game.buttons['pause'].over(pos):
                    game.pause = True
                    pause_loop()
                if game.buttons['wiki'].over(pos):
                    game.wiki_scrape()
                if game.buttons['cast_1'].over(pos) and len(game.spells) > 0:
                    game.cast_spell(0)
                if game.buttons['cast_2'].over(pos) and len(game.spells) > 1:
                    game.cast_spell(1)
                if game.buttons['cast_3'].over(pos) and len(game.spells) > 2:
                    game.cast_spell(2)
                if game.buttons['cast_4'].over(pos) and len(game.spells) > 3:
                    game.cast_spell(3)

            if event.type == pygame.MOUSEBUTTONDOWN and game.shop and len(game.spells) < 4:
                if game.buttons['buy_1'].over(pos):
                    game.buy_spell(0)
                if game.buttons['buy_2'].over(pos):
                    game.buy_spell(1)
                if game.buttons['buy_3'].over(pos):
                    game.buy_spell(2)
                if game.buttons['buy_4'].over(pos):
                    game.buy_spell(3)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.buttons['info'].over(pos):
                    game.draw_tutorial()

            if event.type == pygame.QUIT:
                return pygame.quit()

    return pygame.quit()


def pause_loop():

    while game.pause:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if game.buttons['play'].over(pos):
                    game.pause = False

            if event.type == pygame.QUIT:
                pygame.quit()


def end_loop():
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


if __name__ == '__main__':
    game = maou.MaouGame()
    start_loop()
