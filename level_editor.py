import pygame, sys, time

from src.imgs import Cache, RotImg
from src.utils import load_img, load_imgs
from src.player import Player
from src.objects import Tree
from src.level import LevelLoader

class Controller:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)

class Editor:
    def __init__(self):
        self.display = pygame.display.set_mode((1000, 600))
        self.screen = pygame.Surface((500, 300))
        self.dt = 1
        self.last_time = time.time() - 1 / 60
        self.clock = pygame.time.Clock()
        self.running = True

        self.assets = {'car_0': load_img('lawn_mower.png'),
                       'tree_0': load_img('tree_0.png'),
                       'dirt_0': load_img('grass.png')}

        self.player = Controller()
        self.levels = LevelLoader(self, [50, 50])
        self.levels.load_level(self.assets['dirt_0'], 'dirt_0')

        self.scroll = pygame.Vector2(0, 0)
    
    def close(self):
        self.running = False
        pygame.quit()
        sys.exit()
    
    def update(self):
        render_scroll = self.scroll.copy()
        render_scroll[0] = int(render_scroll[0])
        render_scroll[1] = int(render_scroll[1])
        self.levels.draw(self.screen, render_scroll, 0, 'dirt_0')


    def run(self):
        while self.running:
            self.dt = time.time() - self.last_time
            self.dt *= 60
            self.last_time = time.time()
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()
            self.update()
            pygame.transform.scale_by(self.screen, 2.0, self.display)
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.1f}')
            pygame.display.flip()
            self.clock.tick()

if __name__ == '__main__':
    Editor().run()
