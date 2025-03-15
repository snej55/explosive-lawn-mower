import math, pygame, random, time

from .bip import TILE_SIZE
from .utils import snip

from copy import deepcopy

DENSITY = 3
PADDING = 16
ACCURACY = 1
THRESHOLD = 30 # distance from which cached values are used

class Grass:
    img_cache = {}
    def __init__(self, img, pos, tension, variant):
        self.img = img.copy()
        self.img.convert()
        self.img.set_colorkey((0, 0, 0))
        self.img_copy = img.copy()
        self.pos = list(pos)
        self.angle = 0
        self.target_angle = 0
        self.angle_offset = math.sin(self.pos[0] * 0.2 + self.pos[1] * 0.1) * 20#math.sin(self.pos[0] * 5 + self.pos[1]) * 20
        self.tension = tension
        self.variant = variant
        self.rect = pygame.Rect([self.pos[0] + 8.5, self.pos[1] + 2], [2, 7])
    
    def update_img(self, offset=1):
        key = (int(self.angle + self.angle_offset * offset), self.variant)
        if not key in self.img_cache:
            self.img_cache[key] = pygame.transform.rotate(self.img, key[0])
            filt = pygame.Surface(self.img_cache[key].get_size())
            filt.fill((0, 0, 0))
            try:
                filt.set_alpha(max(0, min(240, int(abs(key[0]) / 90 * 240))) + 15)
            except ZeroDivisionError:
                filt.set_alpha(15)
            self.img_cache[key].blit(filt, (0, 0))
            self.img_cache[key].convert()
            self.img_cache[key].set_colorkey((0, 0, 0))
        self.img_copy = self.img_cache[key]
        return self.img_copy

    def update_img_at_angle(self, angle):
        key = (int(angle), self.variant)
        if not key in self.img_cache:
            self.img_cache[key] = pygame.transform.rotate(self.img, key[0])
            self.img_cache[key].convert()
            self.img_cache[key].set_colorkey((0, 0, 0))
        self.img_copy = self.img_cache[key]
        return self.img_copy
    
    def update(self, rect, dt, offset):
        self.target_angle = offset
        if self.rect.colliderect(rect):
            distance = (rect.x - self.pos[0]) ** 2 + (rect.y - self.pos[1]) ** 2
            hd = rect.centerx - self.rect.centerx
            if distance < 1600:
                temp_target = 0
                if hd <= 0:
                    temp_target = -70 - hd * 3.5
                if hd > 0:
                    temp_target = 70 - hd * 3.5
                self.target_angle = min(self.target_angle + temp_target, 90)
                self.target_angle = max(self.target_angle, -90)
        self.angle += (self.target_angle - self.angle) / self.tension * dt
        self.angle = max(-90, min(self.angle, 90))
        self.update_img()
    
    def draw(self, surf, scroll=(0, 0)):
        loc = (self.pos[0] + int(self.img.get_width() / 2) - int(self.img_copy.get_width() / 2) - scroll[0], self.pos[1] + int(self.img.get_height() / 2) - int(self.img_copy.get_height() / 2) - scroll[1])
        surf.blit(self.img_copy, loc)
    
    def draw_at_pos(self, surf, pos):
        loc = (pos[0] + int(self.img.get_width() / 2) - int(self.img_copy.get_width() / 2), pos[1] + int(self.img.get_height() / 2) - int(self.img_copy.get_height() / 2))
        surf.blit(self.img_copy, loc)

class GrassTile:
    # loc = relative
    def __init__(self, loc, grass_img):
        self.img_cache = {}
        self.pos = pygame.Vector2(loc[0] * TILE_SIZE, loc[1] * TILE_SIZE)
        self.grass = []
        self.angle_offset = random.random() * 1000
        self.gen_grass(grass_img)
        self.offset = 0
    
    def get_random_img(self, grass_img, dim):
        return snip(grass_img, (random.randint(0, 6) * dim[0]), dim)

    def gen_grass(self, grass_img):
        for x in range(TILE_SIZE // DENSITY):
            for y in range(TILE_SIZE // DENSITY):
                idx = random.randint(0, 5)
                self.grass.append(Grass(snip(grass_img, (idx * 18, 0), (18, 18)), pygame.Vector2(self.pos.x + x * DENSITY, self.pos.y + y * DENSITY), 8, idx))
    
    def render_raw(self, rect, dt, surf, scroll):
        self.offset = math.sin(time.time() + self.pos[0] * 0.02 + self.pos[1] * 0.02 + self.angle_offset) * 10
        for blade in self.grass:
            blade.update(rect, dt, self.offset)
            blade.draw(surf, scroll)
    
    def render(self, rect, dt, surf, scroll):
        self.offset = math.sin(time.time() + self.pos[0] * 0.02 + self.pos[1] * 0.02 + self.angle_offset) * 10
        if abs(rect.x - self.pos.x) + abs(rect.y - self.pos.y) > THRESHOLD:
            # pygame.draw.rect(surf, (255, 0, 0), (self.pos.x - scroll[0], self.pos.y - scroll[1], TILE_SIZE, TILE_SIZE))
            surf.blit(self.get_offset_cache(self.offset), (self.pos.x - PADDING - scroll[0], self.pos.y - PADDING - scroll[1]))
        else:
            self.render_raw(rect, dt, surf, scroll)
    
    def cache_offset(self, offset):
        img = pygame.Surface((TILE_SIZE + PADDING * 2, TILE_SIZE + PADDING * 2))
        img.fill((0, 0, 0))
        for blade in self.grass:
            blade.update(pygame.Rect(10000, 10000, 1, 1), 1, offset)
            blade.update_img()
            blade.draw_at_pos(img, (blade.pos[0] - self.pos.x + PADDING, blade.pos[1] - self.pos.y + PADDING))
        img.set_colorkey((0, 0, 0))
        key = str(math.floor(offset / ACCURACY) * ACCURACY)
        self.img_cache[key] = deepcopy(img)
    
    def get_offset_cache(self, offset):
        key = str(math.floor(offset / ACCURACY) * ACCURACY)
        if not key in self.img_cache:
            self.cache_offset(offset)
        return self.img_cache[key]

class GrassManager:
    def __init__(self, locs, grass_img):
        self.grass_tiles = {}
        self.gen_grass(locs, grass_img)
    
    def clear(self):
        for loc in self.grass_tiles:
            del self.grass_tiles[loc]
    
    def gen_grass(self, locs, grass_img):
        for loc in locs:
            pos = [int(l) for l in loc.split(';')]
            self.grass_tiles[loc] = GrassTile(pos, grass_img)
    
    def render(self, rect, dt, screen, scroll):
        for y in range(math.ceil(screen.get_height() / TILE_SIZE) + 3):
            for x in range(math.ceil(screen.get_width() / TILE_SIZE) + 3):
                target_x = x - 2 + math.ceil(scroll.x / TILE_SIZE)
                target_y = y - 2 + math.ceil(scroll.y / TILE_SIZE)
                target_tile = f'{target_x};{target_y}'
                if target_tile in self.grass_tiles:
                    self.grass_tiles[target_tile].render(rect, dt, screen, scroll)