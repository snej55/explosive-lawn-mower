import math, pygame

from .stacked_sprite import SpriteStack

class Tree:
    def __init__(self, app, pos):
        self.app = app
        self.pos = pygame.Vector2(pos)
        # self.tree = SpriteStack(app, pos, self.app.assets[])