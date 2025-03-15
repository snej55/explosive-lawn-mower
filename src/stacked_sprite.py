import pygame, math

from .utils import snip

class SpriteStack:
    layers = {}
    def __init__(self, app, pos, sheet, dim, name, spread, accuracy, padding, variant=0):
        self.pos = pygame.Vector2(pos)
        self.app = app
        self.dim = dim
        self.padding = padding
        self.name = name
        self.sheet = sheet
        self.spread = spread
        self.accuracy = accuracy
        self.variant = variant
        if not (self.name in self.layers):
            self.layers[self.name] = self.load_layers()
        self.shadow = pygame.Surface(self.layers[self.name][0].get_size())
        self.shadow.set_colorkey((0, 0, 0))
        for layer in self.layers[self.name]:
            self.shadow.blit(layer, (0, 0))
        shadow_mask = pygame.mask.from_surface(self.shadow)
        self.shadow = shadow_mask.to_surface(setcolor=(1, 0, 0, 100), unsetcolor=(0, 0, 0, 0))
        self.shadow.set_colorkey((0, 0, 0, 0))
        self.app.cache.load_stack_cache(self.layers[self.name], padding, accuracy, name, spread=spread, variant=variant)
    
    def load_layers(self):
        img = self.sheet
        y = 0
        imgs = []
        for _ in range(max(1, int(self.sheet.get_height() / self.dim[1]))):
            imgs.append(snip(img, [0, y], self.dim))
            y += self.dim[1]
        return imgs
    
    def get_img(self, rotation):
        return self.app.cache.get_img(self.name, rotation, self.accuracy, self.variant)

    def get_shadow(self, rotation):
        return self.app.cache.get_shadow(self.name, rotation, self.accuracy, self.variant)