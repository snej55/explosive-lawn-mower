import pygame, sys, time, json

from src.imgs import Cache, RotImg
from src.utils import load_img, load_imgs
from src.player import Player
from src.objects import Tree
from src.level import LevelLoader

MAP_PATH = "data/maps/0.json"

class App:
    def __init__(self):
        self.display = pygame.display.set_mode((640, 640))
        self.screen = pygame.Surface((320, 320))
        self.time = 0
        self.dt = 1
        self.last_time = time.time() - 1 / 60
        self.clock = pygame.time.Clock()
        self.running = True
        self.assets = {'car_0': load_img('car.png'),
                       'tree_0': [load_img('tree_0.png')],
                       'dirt_0': load_img('grass.png')}
        self.cache = Cache(self)
        self.player = Player(self, (941, 411))
        self.scroll = pygame.Vector2(0, 0)
        self.camera_angle = 0
        self.levels = LevelLoader(self, [50, 50])
        self.levels.load_level(self.assets['dirt_0'], 'dirt_0')

        self.tree = Tree("tree_0", self, (50, 50), [24, 24], )

        self.level_data = {}
        self.load_map(MAP_PATH)

        self.rotating = False

        self.modes = [
            "tree",
            "box",
        ]

        self.mode = 0

    def load_map(self, path):
        with open(path, 'r') as f:
            self.level_data = json.load(f)
        
    def save_map(self, path):
        with open(path, 'w') as f:
            json.dump(self.level_data, f)

    def close(self):
        self.running = False
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def draw_objects(self):
        items = []
        for tree in self.level_data['trees']:
            items.append({"type": "tree", "pos": tree["pos"]})
        for box in self.level_data["boxes"]:
            items.append({"type": "box", "pos": box["pos"]})
        items.sort(key=lambda x: x["pos"][1])

        for item in items:
            if item["type"] == "tree":
                self.tree.draw(self.screen, self.scroll, item["pos"])

    def update(self):
        self.player.update()
        self.scroll[0] += ((self.player.pos[0] - self.screen.get_width() * 0.5 - self.scroll[0])) * self.dt
        self.scroll[1] += ((self.player.pos[1] - self.screen.get_height() * 0.5 - self.scroll[1])) * self.dt
        render_scroll = self.scroll.copy()
        render_scroll[0] = int(render_scroll[0])
        render_scroll[1] = int(render_scroll[1])
        if self.rotating:
            self.camera_angle += (self.player.angle - self.camera_angle) * 0.1 * self.dt
        else:
            self.camera_angle = 0
        self.time += 1 * self.dt
        self.levels.draw(self.screen, self.scroll, self.camera_angle, 'dirt_0')
        self.player.draw(self.screen, self.scroll)
        # self.tree.angle = self.player.angle
        # self.tree.draw(self.screen, render_scroll, self.player.pos)
        self.draw_objects()

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = pygame.Vector2(mouse_pos) / 2
        mouse_pos += self.scroll
        
        if self.get_mode() == "tree":
            self.tree.draw(self.screen, self.scroll, mouse_pos)
    
    def get_mode(self):
        return self.modes[self.mode]

    def run(self):
        while self.running:
            self.dt = time.time() - self.last_time
            self.dt *= 60
            self.last_time = time.time()
            self.screen.fill((94, 55, 53))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.controls['brake'] = True
                    if event.key == pygame.K_ESCAPE:
                        self.close()
                    if event.key == pygame.K_LEFT:
                        self.player.controls['left'] = True
                    if event.key == pygame.K_RIGHT:
                        self.player.controls['right'] = True
                    if event.key == pygame.K_UP:
                        self.player.controls['up'] = True
                    if event.key == pygame.K_DOWN:
                        self.player.controls['down'] = True
                    if event.key == pygame.K_r:
                        self.rotating = not self.rotating
                    if event.key == pygame.K_m:
                        self.mode = (self.mode + 1) % len(self.modes)
                    if event.key == pygame.K_o:
                        self.save_map(MAP_PATH)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player.controls['brake'] = False
                    if event.key == pygame.K_LEFT:
                        self.player.controls['left'] = False
                    if event.key == pygame.K_RIGHT:
                        self.player.controls['right'] = False
                    if event.key == pygame.K_UP:
                        self.player.controls['up'] = False
                    if event.key == pygame.K_DOWN:
                        self.player.controls['down'] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        mouse_pos = pygame.Vector2(mouse_pos) / 2
                        mouse_pos += self.scroll
                        
                        if self.get_mode() == "tree":
                            self.level_data["trees"].append({"pos": list(mouse_pos)})

            self.update()
            pygame.transform.scale(self.screen, self.display.get_size(), self.display)
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.1f}')
            pygame.display.flip()
            self.clock.tick()

if __name__ == '__main__':
    App().run()
