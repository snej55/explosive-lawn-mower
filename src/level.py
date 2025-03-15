import math
import pygame

from .utils import snip

class LevelLoader:
    def __init__(self, app, chunk_size):
        self.app = app
        self.levels = {}
        self.chunk_size = list(chunk_size)
    
    def load_level(self, img, name):
        level_img = img.convert()
        level_data = {}
        filt = pygame.Surface(self.chunk_size)
        filt.fill((0, 0, 0))
        filt.set_alpha(0)
        for y in range(math.ceil(level_img.get_height() / self.chunk_size[1])):
            for x in range(math.ceil(level_img.get_width() / self.chunk_size[0])):
                key = f'{x};{y}'
                level_data[key] = snip(level_img, [x * self.chunk_size[0], y * self.chunk_size[1]], self.chunk_size)
                level_data[key].blit(filt, (0, 0))
                level_data[key].set_colorkey((0, 0, 0))
        self.levels[name] = level_data
        return level_data

    def draw(self, surf, scroll, camera_angle, name):
        for y in range(math.ceil(surf.get_height() / (self.chunk_size[1])) + 4):
            for x in range(math.ceil(surf.get_width() / (self.chunk_size[0])) + 4):
                target_x = x - 2 + math.ceil(scroll.x / (self.chunk_size[0]))
                target_y = y - 2 + math.ceil(scroll.y / (self.chunk_size[1]))
                target_chunk = f'{target_x};{target_y}'
                if target_chunk in self.levels[name]:
                    img = self.levels[name][target_chunk]
                    pos = pygame.Vector2(target_x * (self.chunk_size[0] - 2), target_y * (self.chunk_size[1] - 2)) - self.app.player.pos
                    rot_offset = -pygame.Vector2(img.get_width() * 0.5, img.get_height() * 0.5)
                    pos -= rot_offset
                    pos.rotate_ip(camera_angle)
                    pos += rot_offset
                    pos += self.app.player.pos
                    pos -= scroll
                    #print(camera_angle)
                    rot_img = pygame.transform.rotate(img, -camera_angle)
                    surf.blit(rot_img, (pos[0] + img.get_width() * 0.5 - rot_img.get_width() * 0.5, pos[1] + img.get_height() * 0.5 - rot_img.get_height() * 0.5))
                    