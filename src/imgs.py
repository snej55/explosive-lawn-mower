import pygame, math
from .utils import render_stack

class RotImg:
    img_cache = {}
    def __init__(self, name, img, accuracy=2, variant=0):
        self.img = img.copy()
        self.variant = variant
        self.name = name
        self.accuracy = accuracy
        self.img_copy = img.copy()
    
    def get_img(self, angle):
        key = ((math.floor(angle / self.accuracy) * self.accuracy)%360, self.name, self.variant)
        if not key in self.img_cache:
            self.img_cache[key] = pygame.transform.rotate(self.img, key[0])
            self.img_cache[key].convert_alpha()
            self.img_cache[key].set_colorkey((0, 0, 0))
        self.img_copy = self.img_cache[key]
        return self.img_copy, key
    
    def draw(self, pos, surf, angle, scroll=(0, 0)):
        self.get_img(angle)
        loc = (pos[0] + int(self.img.get_width() / 2) - int(self.img_copy.get_width() / 2) - scroll[0], pos[1] + int(self.img.get_height() / 2) - int(self.img_copy.get_height() / 2) - scroll[1])
        surf.blit(self.img_copy, loc)

class Cache:
    def __init__(self, app):
        self.cache = {}
        self.rots = {}
        self.shadows = {}
        self.done = set()
        self.rot_done = set()
        self.app = app
    
    def get_img(self, name, rotation, accuracy, variant=0):
        key = ((math.floor(rotation / accuracy) * accuracy)%360, name, variant)
        if key in self.cache:
            return self.cache[key]
    
    def get_shadow(self, name, rotation, accuracy, variant=0):
        key = ((math.floor(rotation / accuracy) * accuracy)%360, name, variant)
        if key in self.shadows:
            return self.shadows[key]
        
    '''def load_rot_cache(self, img, padding, accuracy, name):
        if not (name in self.rot_done):
            self.rot_done.add(name)
            for i in range(math.ceil(360 / accuracy)):
                key = ((i * accuracy)%360, name)
                if not (key in self.rot_cache):
                    surf = pygame.Surface((img.get_width() + padding * 2, img.get_height() + padding * 2))
                    '''
    
    def load_stack_cache(self, imgs, padding, accuracy, name, spread=1, variant=0):
        if not (name in self.done):
            self.done.add(name)
            for i in range(math.ceil(360 / accuracy)):
                key = ((i * accuracy)%360, name, variant)
                if not (key in self.cache):
                    img = pygame.Surface((imgs[0].get_width() + padding * 2, imgs[0].get_height() + padding * 2))
                    #img.fill((0, 255, 0))
                    render_stack(img, imgs, (img.get_width() * 0.5, img.get_height() * 0.5 - padding), (i * accuracy)%360, spread)
                    img.convert_alpha()
                    img.set_colorkey((0, 0, 0))
                    self.cache[key] = img
                    rot_imgs = [pygame.transform.rotate(img, (i * accuracy)%360) for img in imgs.copy()]
                    shadow = pygame.Surface(rot_imgs[0].get_size())
                    for rimg in rot_imgs:
                        shadow.blit(rimg, (0, 0))
                    shadow.set_colorkey((0, 0, 0))
                    shadow_mask = pygame.mask.from_surface(shadow)
                    shadow = shadow_mask.to_surface(setcolor=(1, 0, 0, 100), unsetcolor=(0, 0, 0, 0))
                    shadow.set_colorkey((0, 0, 0, 0))
                    self.shadows[key] = shadow