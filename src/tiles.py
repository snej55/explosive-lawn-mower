import json, math, pygame
from .objects import Object, ObjectChunks, Tree
from .bip import *
from .imgs import RotImg

AUTO_TILE_MAP = {'0011': 1, '1011': 2, '1001': 3, '0001': 4, '0111': 5, '1111': 6, '1101': 7, '0101': 8, 
                '0110': 9, '1110': 10, '1100': 11, '0100': 12, '0010': 13, '1010': 14, '1000': 15, '0000': 16}
AUTO_TILE_TYPES = {"snow"}

class Chunker:
    def __init__(self, tiles, chunk_size, app):
        self.app = app
        self.tiles = tiles
        self.chunk_size = chunk_size
        self.chunks, self.tile_map = self.load_chunks(tiles, chunk_size)
    
    @staticmethod
    def load_chunks(tiles, chunk_size) -> dict:
        chunks = {}
        tile_map = {}
        for tile in tiles:
            loc = str(math.floor(tile.pos[0] / chunk_size[0] / TILE_SIZE)) + ';' + str(math.floor(tile.pos[1] / chunk_size[1] / TILE_SIZE))
            if not (loc in chunks):
                chunks[loc] = []
            chunks[loc].append(tile)
            loc = str(math.floor(tile.pos[0] / TILE_SIZE)) + ';' + str(math.floor(tile.pos[1] / TILE_SIZE))
            tile_map[loc] = tile
        return chunks, tile_map

    def add_tile(self, tile):
        loc = str(math.floor(tile.pos[0] / self.chunk_size[0] / TILE_SIZE)) + ';' + str(math.floor(tile.pos[1] / self.chunk_size[1] / TILE_SIZE))
        if not (loc in self.chunks):
            self.chunks[loc] = []
        self.tiles.append(tile)
        self.chunks[loc].append(tile)
        loc = str(math.floor(tile.pos[0] / TILE_SIZE)) + ';' + str(math.floor(tile.pos[1] / TILE_SIZE))
        self.tile_map[loc] = tile
    
    def auto_tile(self):
        for key in self.chunks:
            for tile in self.chunks[key]:
                aloc = ''
                for shift in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                    check_loc = str(math.floor(tile.pos[0] / TILE_SIZE) + shift[0]) + ';' + str(math.floor(tile.pos[1] / TILE_SIZE) + shift[1])
                    if check_loc in self.tile_map:
                        if self.tile_map[check_loc].name == tile.name:
                            aloc += '1'
                        else:
                            aloc += '0'
                    else:
                        aloc += '0'
                if tile.name in AUTO_TILE_TYPES:
                    tile.variant = AUTO_TILE_MAP[aloc] - 1
                    tile.img.variant = tile.variant
                    tile.img.img = self.app.assets[tile.name][tile.variant]
                    print(tile.img.get_img(0)[1])
    
    def get_tiles_around(self, pos):
        loc = (math.floor(pos[0] / self.chunk_size[0] / TILE_SIZE), math.floor(pos[1] / self.chunk_size[1] / TILE_SIZE))
        for y in range(3):
            for x in range(3):
                aloc = (loc[0] - 1 + x, loc[1] - 1 + y)
                key = f'{aloc[0]};{aloc[1]}'
                if key in self.chunks:
                    for tile in self.chunks[key]:
                        yield tile
    
    def draw(self, surf, scroll):
        for y in range(math.ceil(surf.get_height() / (self.chunk_size[1] * TILE_SIZE)) + 1):
            for x in range(math.ceil(surf.get_width() / (self.chunk_size[0] * TILE_SIZE)) + 1):
                target_x = x - 1 + math.ceil(scroll.x / (self.chunk_size[0] * TILE_SIZE))
                target_y = y - 1 + math.ceil(scroll.y / (self.chunk_size[1] * TILE_SIZE))
                target_chunk = f'{target_x};{target_y}'
                if target_chunk in self.chunks:
                    for tile in self.chunks[target_chunk]:
                        tile.draw(surf, scroll)

class Tile:
    def __init__(self, name, app, img, pos, angle, variant):
        self.variant = variant
        self.img = RotImg(name, img, variant=variant)
        self.angle = angle
        self.pos = pygame.Vector2(pos)
        self.name = name
        self.app = app
        self.rot_offset = -pygame.Vector2(img.get_width() * 0.5, img.get_height() * 0.5)
    
    def transform(self, scroll: pygame.Vector2):
        pos = self.pos - self.app.player.pos
        pos -= self.rot_offset
        pos.rotate_ip(self.app.camera_angle)
        pos += self.rot_offset
        pos += self.app.player.pos # self.layers
        return pos - scroll
    
    def draw(self, surf, scroll, loc=None):
        if loc:
            self.pos = list(loc)
        pos = self.transform(scroll)
        self.img.draw(pos, surf, self.angle - self.app.camera_angle)

class TileMap:
    def __init__(self, app):
        self.app = app
        self.tiles, self.objects = [], []
        self.load_chunks()
    
    def load_chunks(self):
        self.tile_chunker = Chunker(self.tiles, TILE_CHUNK_SIZE, self.app)
        self.object_chunker = ObjectChunks(self.objects, OBJ_CHUNK_SIZE, self.app)
    
    def load_object(self, obj):
        item = Object(obj['name'], self.app, obj['pos'], obj['dim'], obj['spread'], obj['accuracy'], obj['padding'], obj['angle'], obj['variant'])
        if obj['name'] == 'tree_0':
            item = Tree(obj['name'], self.app, obj['pos'], obj['dim'], obj['spread'], obj['accuracy'], obj['padding'], obj['angle'], obj['variant'])
        return item
    
    def load_tile(self, tile):
        return Tile(tile['name'], self.app, self.app.assets[tile['name']][tile['variant']], tile['pos'], tile['angle'], tile['variant'])
    
    def load(self, path):
        tiles = []
        objects = []
        with open(path, 'r') as f:
            map_data = json.load(f)
            for tile in map_data['tiles'].copy():
                tiles.append(self.load_tile(tile))
            for obj in map_data['objects'].copy():
                objects.append(self.load_object(obj))
        self.tiles, self.objects = tiles, objects
        self.load_chunks()
        return tiles, objects
    
    def draw(self, surf, scroll):
        self.tile_chunker.draw(surf, scroll)
        self.object_chunker.draw(surf, scroll)