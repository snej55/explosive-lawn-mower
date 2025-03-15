import pygame, math, os, json

BASE_IMG_PATH = 'data/images'
BASE_AUDIO_PATH = 'data/audio'

def load_img(path, scale=(1, 1)):
    img = pygame.transform.scale_by(pygame.image.load(BASE_IMG_PATH + '/' + path), scale)
    img.convert()
    img.set_colorkey((0, 0, 0))
    return img

def mean_points(points):
    v = pygame.Vector2(0, 0)
    for p in points:
        v += p
    return v / len(points)
    
def snip(spritesheet, pos, dimensions):
    handle_surf = spritesheet.copy()
    clip_rect = pygame.Rect(pos, dimensions)
    handle_surf.set_clip(clip_rect)
    image = spritesheet.subsurface(handle_surf.get_clip())
    return image.copy()

def load_tile_assets(path, assets, tile_size):
    for img_name in sorted(os.listdir(BASE_IMG_PATH + '/' + path)):
        tile_imgs = load_tile_imgs(path + '/' + img_name, tile_size)
        tile_type = img_name.split('.')[0]
        assets[tile_type] = tile_imgs
    return assets.copy()

def key(pos, dim):
    return str(math.floor(pos[0] / dim[0])) + ';' + str(math.floor(pos[1] / dim[1]))

def load_audio(path):
    tracks = []
    for track_name in sorted(os.listdir(BASE_AUDIO_PATH + '/' + path)):
        tracks.append(pygame.mixer.Sound(BASE_AUDIO_PATH + '/' + path + '/' + track_name))
    return tracks

def load_spritesheet(path, name):
    img = load_img(path + '/' + name + '.png')
    f = open(BASE_IMG_PATH + '/' + path + '/' + name + '.json')
    img_data = json.load(f)
    f.close()
    imgs = []
    x = 0
    for dim in img_data['img_dims']:
        imgs.append(snip(img, [x, 0], dim))
        x += dim[0]
    return imgs

def outline(img, loc, surf, color):
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface(setcolor=color)
    mask_surf.set_colorkey((0, 0, 0))
    surf.blit(mask_surf, (loc[0] - 1, loc[1]))
    surf.blit(mask_surf, (loc[0] + 1, loc[1]))
    surf.blit(mask_surf, (loc[0], loc[1] - 1))
    surf.blit(mask_surf, (loc[0], loc[1] + 1))

def read_f(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data

def write_f(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

def read_json(path):
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    return data

def write_json(path, data):
    f = open(path, 'w')
    json.dump(data, f)
    f.close()

def load_entity_assets(path, assets, name):
    for img_name in sorted(os.listdir(BASE_IMG_PATH + '/' + path)):
        aloc = img_name.split('.')[-1]
        if aloc == 'png':
            imgs = load_spritesheet(path, img_name.split('.')[0])
            assets[name + '/' + img_name.split('.')[0]] = imgs
    return assets.copy()

def load_palette(img: pygame.Surface):
    img_array = pygame.pixelarray.PixelArray(img)
    palette = []
    for row in img_array:
        for color in row:
            c = img.unmap_rgb(color)
            if c != (0, 0, 0, 0): palette.append(tuple(c))
    return palette

def load_palettes(assets):
    palettes = {}
    def get_pals(imgs: pygame.Surface | list):
        palettes = []
        if not (type(imgs) == pygame.Surface):
            for item in imgs:
                if (type(imgs) == list):
                    palettes.append(get_pals(item))
        else:
            palettes.append(load_palette(imgs))
        return palettes
    for key in assets:
        palettes[key] = get_pals(assets[key])
    return palettes

def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clip_rect = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clip_rect)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

def color_swap(orig_color, swap_color, surf):
    return_surf = surf.copy()
    return_surf.set_colorkey(orig_color)
    color_surf = pygame.Surface(return_surf.get_size())
    color_surf.fill(swap_color)
    color_surf.blit(return_surf, (0, 0))
    return color_surf

def load_tile_imgs(path, tile_size):
    img = load_img(path)
    img_surf = pygame.Surface((tile_size, tile_size))
    tiles = []
    dimensions = [int(img.get_width() / tile_size), int(img.get_height() / tile_size)]
    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            img_surf.fill((0, 0, 0))
            img_surf.blit(img, (-x * tile_size, -y * tile_size))
            img_surf.convert()
            img_surf.set_colorkey((0, 0, 0))
            tiles.append(img_surf.copy())
    return tiles

def load_imgs(path):
    imgs = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + '/' + path)):
        imgs.append(load_img(path + '/' + img_name))
    return imgs

def load_chunks(tiles, tile_size, chunk_size: pygame.Vector2, data):
    chunk_data = dict(data)
    for tile in tiles:
        tile_loc = str(math.floor(tile.pos.x / tile_size / chunk_size.x)) + ';' + str(math.floor(tile.pos.y / tile_size / chunk_size.y))
        if not tile_loc in chunk_data:
            chunk_data[tile_loc] = []
        chunk_data[tile_loc].append(tile)
    return chunk_data

def load_key(key: str, dim):
    return [int(n) * dim[i] for i, n in enumerate(key.split(';'))]

def alpha_surf(surf, alpha):
    alpha_surf = surf.copy()
    alpha_surf.set_alpha(alpha)
    return_surf = pygame.Surface(surf.get_size())
    return_surf.blit(alpha_surf, (0, 0))
    return_surf.convert_alpha()
    return return_surf

