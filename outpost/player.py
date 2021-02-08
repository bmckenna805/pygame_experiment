import pygame
import sprites


class Player(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        sprites.Sprite.__init__(self, pos)
        self.hp = 100
        self.name = 'fred johnson'
        self.cash = 10
