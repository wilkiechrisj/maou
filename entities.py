from dataclasses import dataclass
from random import random
from copy import deepcopy

BLACK = (0, 0, 0)
BROWN = (150, 75, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


@dataclass
class Player:

    name: str
    rep: tuple
    attack: int
    defense: int
    speed: int
    max_health: int
    cur_health: int
    debuffs: list
    buffs: list
    score: int

    def __init__(self):
        self.name = 'Maou'
        self.type = 'PLAYER'
        self.attack = 2
        self.defense = 0
        self.speed = 1
        self.max_health = 50
        self.cur_health = 50
        self.debuffs = []
        self.buffs = []
        self.score = 0
        self.gold = 0
        self.rooms = 1


@dataclass
class Rat:

    name: str
    attack: int
    defense: int
    speed: int
    health: int
    value: int

    def __init__(self):
        self.name = 'Rat'
        self.type = 'ENEMY'
        self.attack = 0
        self.defense = 0
        self.speed = 1
        self.health = 2
        self.value = 1

    def ability(self):
        if self.health < 5:
            self.health += 1
        return None


@dataclass
class Zombie:

    name: str
    attack: int
    defense: int
    speed: int
    health: int
    value: int

    def __init__(self):
        self.name = 'Zombie'
        self.type = 'ENEMY'
        self.attack = 1
        self.defense = 0
        self.speed = 1
        self.health = 5
        self.effect = 'ROT'
        self.value = 2

    def ability(self):
        chance = random()
        if chance >= 0.8:
            return self.effect


@dataclass
class Wolf:

    name: str
    attack: int
    defense: int
    speed: int
    health: int
    value: int

    def __init__(self):
        self.name = 'Wolf'
        self.type = 'ENEMY'
        self.attack = 1
        self.defense = 1
        self.speed = 1
        self.health = 8
        self.value = 3

    def ability(self):
        chance = random()
        if chance >= 0.7:
            self.speed = 2
        return


@dataclass
class Dragon:

    name: str
    attack: int
    defense: int
    speed: int
    health: int
    value: int

    def __init__(self):
        self.name = 'Dragon'
        self.type = 'BOSS'
        self.attack = 3
        self.defense = 1
        self.speed = 1
        self.health = 20
        self.value = 5
        self.turn = 0

    def ability(self):

        self.turn += 1

        if self.turn % 2 == 0:
            return self.attack - 1


if __name__ == "__main__":
    x = Dragon()
    y = deepcopy(x)
    y.cur_health = 1
    print(x, y)
