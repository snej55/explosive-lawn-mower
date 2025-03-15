import pygame, time, math
from pygame.locals import *
from ..utils import *

class TextBox:
    def __init__(self, path, rect: pygame.Rect, text: str, border=2, anim=None, color=(255, 255, 255), width=0):
        self.spacing = 1
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                'R', 'S', 'T', 'U', 'V',
                                'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                'n', 'o', 'p', 'q', 'r',
                                's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', "'", '!', '?', '0',
                                '1', '2', '3', '4', '5',
                                '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        font_img = color_swap((255, 255, 255), color, pygame.image.load(path).convert()) # - ' ' ... ' ' - ' ...
        self.color = color
        current_char_width = 0
        self.characters = {}
        self.chr_i = 0
        self.border = border
        self.text = text
        self.rect = rect
        self.width = width
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                self.characters[self.character_order[character_count]].convert()
                self.characters[self.character_order[character_count]].set_colorkey((0, 0, 0))
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.characters['\n'] = pygame.Surface((0, 0))
        self.characters['\t'] = pygame.Surface((0, 0))
        self.loc = list((c + self.border for c in self.rect.topleft))
        self.words = [(sum([self.characters[char].get_width() for char in word]), word) for word in self.text.split(' ')]
        self.max_word_length = 0
        for word in self.words:
            if word[0] > self.max_word_length:
                self.max_word_length = word[0]
        self.word = 0
        self.space_width = self.characters['A'].get_width()
        self.length = 0
        self.x_offset = 0
        self.y_offset = self.characters['A'].get_height()
        self.row = 0
        self.anim = anim
        if not self.anim:
            self.surf = pygame.Surface((self.rect.width, self.rect.height))
            self.surf.fill((0, 0, 0))
            self.surf.set_colorkey((0, 0, 0))

    def render(self, surf, dt):
        if self.anim:
            self.x_offset = 0
            self.y_offset = self.characters['A'].get_height()
            self.row = 0
            for char in self.text[0: min(len(self.text), int(self.chr_i))]:
                if char == '\n':
                    self.row += 1
                    self.x_offset = 0
                elif char != ' ':
                    surf.blit(self.characters[char], (self.loc[0] + self.x_offset, self.loc[1] + self.y_offset * self.row + self.anim[0] * math.sin(self.x_offset * self.anim[1] + time.time() * self.anim[2] + math.cos(self.row * self.anim[3]))))
                    self.x_offset += self.characters[char].get_width() + self.spacing
                else:
                    self.x_offset += self.space_width + self.spacing
                    self.word = min(len(self.words) - 1, self.word + 1)
                    if self.x_offset + self.max_word_length >= self.rect.width - self.border * 2:
                        self.x_offset = 0
                        self.row += 1
        else:
            if self.chr_i <= len(self.text) + 1:
                self.x_offset = 0
                self.y_offset = self.characters['A'].get_height()
                self.row = 0
                for char in self.text[0: min(len(self.text), int(self.chr_i))]:
                    if char == '\n':
                        self.row += 1
                        self.x_offset = 0
                    elif char != ' ':
                        surf.blit(self.characters[char], (self.loc[0] + self.x_offset, self.loc[1] + self.y_offset * self.row))# + self.anim[0] * math.sin(self.x_offset * self.anim[1] + time.time() * self.anim[2] + math.cos(self.row * self.anim[3]))))
                        self.surf.blit(self.characters[char], (self.loc[0] - self.rect.x + self.x_offset, self.loc[1] - self.rect.y + self.y_offset * self.row))
                        self.x_offset += self.characters[char].get_width() + self.spacing
                    else:
                        self.x_offset += self.space_width + self.spacing
                        self.word = min(len(self.words) - 1, self.word + 1)
                        if self.x_offset + self.max_word_length >= self.rect.width - self.border * 2:
                            self.x_offset = 0
                            self.row += 1
            else:
                if int(self.chr_i) == len(self.text) + 2:
                    self.surf.convert()
                surf.blit(self.surf, (self.rect.x, self.rect.y))
        self.chr_i += 1 * dt
        if self.width:
            pygame.draw.rect(surf, self.color, self.rect, self.width)

class Font:
    def __init__(self, path, color=(255, 255, 255)):
        self.spacing = 1
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                'R', 'S', 'T', 'U', 'V',
                                'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                'n', 'o', 'p', 'q', 'r',
                                's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', '\'', '!', '?', '0',
                                '1', '2', '3', '4', '5',
                                '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        font_img = color_swap((255, 255, 255), color, pygame.image.load(path).convert())
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                self.characters[self.character_order[character_count]].convert()
                self.characters[self.character_order[character_count]].set_colorkey((0, 0, 0))
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing