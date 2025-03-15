import pygame, os

BASE_IMG_PATH = 'data/images/'

def render_stack(surf, images, pos, rotation, spread=1):
    for i, img in sorted(enumerate(images), reverse=True):
        rotated_img = pygame.transform.rotate(img, rotation)
        surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 + i * spread))

def snip(spritesheet, pos, dimensions):
    handle_surf = spritesheet.copy()
    clip_rect = pygame.Rect(pos, dimensions)
    handle_surf.set_clip(clip_rect)
    image = spritesheet.subsurface(handle_surf.get_clip())
    return image.copy()

def load_img(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return img

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
    for img_path in os.listdir(BASE_IMG_PATH + path):
        imgs.append(load_img(path + '/' + img_path))
    return imgs