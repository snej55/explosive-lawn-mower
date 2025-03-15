import pygame

class Box:
    def __init__(self, app, rect, fill, stroke=None, width=0, alpha=255):
        self.rect = pygame.Rect(rect)
        self.fill = list(fill)
        self.app = app
        self.width = int(width)
        self.stroke = list(stroke) if stroke else None
        self.alpha = alpha
    
    def __mul__(self, n):
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.width * n, self.rect.height * n)
    
    def add(self, rect, dr='h'):
        if dr=='h':
            return pygame.Rect(self.rect.x, self.rect.y, self.rect.width + ((rect.width * rect.height) / self.rect.height), self.rect.height)
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height + ((rect.width * rect.height) / self.rect.width))
    
    def __div__(self, n):
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.width / n, self.rect.height / n)
    
    def sub(self, rect, dr='h'):
        if dr=='h':
            return pygame.Rect(self.rect.x, self.rect.y, self.rect.width - ((rect.width * rect.height) / self.rect.height), self.rect.height)
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height - ((rect.width * rect.height) / self.rect.width))
    
    def draw(self, screen, scroll=(0, 0)):
        surf = pygame.Surface(screen.get_size())
        surf.set_colorkey((0, 0, 0))
        pygame.draw.rect(surf, {False: tuple(self.fill), True: self.stroke}[bool(self.width)], self.rect, width=int(self.width))
        surf.set_alpha(self.alpha)
        screen.blit(surf, (self.rect.x - scroll[0], self.rect.y - scroll[1]))