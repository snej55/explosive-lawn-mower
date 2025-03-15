import pygame, math
from .stacked_sprite import SpriteStack
from .bip import TILE_SIZE

class ObjectChunks:
    def __init__(self, objects, chunk_size, app):
        self.app = app
        self.objects = objects
        self.chunk_size = chunk_size
        self.chunks = self.load_chunks(objects, chunk_size)
    
    @staticmethod
    def load_chunks(objects, chunk_size) -> dict:
        chunks = {}
        for obj in objects:
            loc = str(math.floor(obj.pos[0] / chunk_size[0] / TILE_SIZE)) + ';' + str(math.floor(obj.pos[1] / chunk_size[1] / TILE_SIZE))
            if not (loc in chunks):
                chunks[loc] = []
            chunks[loc].append(obj)
        return chunks

    def add_obj(self, obj):
        loc = str(math.floor(obj.pos[0] / self.chunk_size[0] / TILE_SIZE)) + ';' + str(math.floor(obj.pos[1] / self.chunk_size[1] / TILE_SIZE))
        if not (loc in self.chunks):
            self.chunks[loc] = []
        self.objects.append(obj)
        self.chunks[loc].append(obj)
    
    def get_objects_around(self, pos):
        loc = (math.floor(pos[0] / self.chunk_size[0] / TILE_SIZE), math.floor(pos[1] / self.chunk_size[1] / TILE_SIZE))
        for y in range(3):
            for x in range(3):
                aloc = (loc[0] - 1 + x, loc[1] - 1 + y)
                key = f'{aloc[0]};{aloc[1]}'
                if key in self.chunks:
                    for obj in self.chunks[key]:
                        yield obj
    
    def draw(self, surf, scroll):
        for y in range(math.ceil(surf.get_height() / (self.chunk_size[1] * TILE_SIZE)) + 1):
            for x in range(math.ceil(surf.get_width() / (self.chunk_size[0] * TILE_SIZE)) + 1):
                target_x = x - 1 + math.ceil(scroll.x / (self.chunk_size[0] * TILE_SIZE))
                target_y = y - 1 + math.ceil(scroll.y / (self.chunk_size[1] * TILE_SIZE))
                target_chunk = f'{target_x};{target_y}'
                if target_chunk in self.chunks:
                    for obj in self.chunks[target_chunk]:
                        obj.update()
                        obj.draw(surf, scroll)

class Object(SpriteStack):
    def __init__(self, name, app, pos, dim, spread=1, accuracy=2, padding=13, angle=0, variant=0):
        super().__init__(app, pos, app.assets[name][variant], dim, name, spread, accuracy, padding, variant=variant)
        self.angle = angle
        self.variant = variant
        self.offset = pygame.Vector2(self.padding, self.padding)
        self.shadow_offset = pygame.Vector2(-self.padding * 0.72, -self.padding * 2)
        self.rot_offset = pygame.Vector2(0, 0)
    
    def collide(self, point):
        if (point[1] - self.pos[1]) ** 2 + (point[0] - self.pos[1]) ** 2 < 3:
            return 1
    
    def transform(self, scroll: pygame.Vector2):
        pos = self.pos - self.app.player.pos
        pos -= self.rot_offset
        pos.rotate_ip(self.app.camera_angle)
        pos += self.rot_offset
        pos += self.app.player.pos # self.layers
        return pos - scroll
    
    def update(self):
        pass

    def draw(self, surf, scroll, loc=None):
        if loc:
            self.pos = pygame.Vector2(loc)
        pos = self.transform(scroll)
        shadow = self.get_shadow(self.angle - self.app.camera_angle)
        surf.blit(shadow, (pos[0] - shadow.get_width() // 2 - self.shadow_offset[0], pos[1] - shadow.get_height() // 2 - self.shadow_offset[1]))
        surf.blit(self.get_img(self.angle - self.app.camera_angle), (pos[0] - self.offset[0], pos[1] - self.offset[1]))
        #surf.set_at((self.app.player.pos - scroll), (0, 0, 255))
        #surf.set_at(pos - self.rot_offset, (0, 0, 255))

class Tree(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = pygame.Vector2(self.padding, self.padding)
        self.shadow_offset = pygame.Vector2(-self.padding * 0.72, -self.padding * 2)
        self.rot_offset = pygame.Vector2(-10, -32)

class Box(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = pygame.Vector2(self.padding, self.padding)
        self.shadow_offset = pygame.Vector2(-4, -4)
        self.rot_offset = pygame.Vector2(-5, -5)

        self.body = None
        self.shape = None
    
    def update(self):
        super().update()
        # self.shape.body.apply_impulse_at_local_point(0.5 * -self.shape.body.velocity, (0, 0))
        self.pos = pygame.Vector2(list(self.shape.body.position)) + pygame.Vector2(-6, -5)
        self.angle = -math.degrees(self.shape.body.angle)