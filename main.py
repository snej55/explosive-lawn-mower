import pygame, sys, time, json, pymunk, random

from src.imgs import Cache, RotImg
from src.utils import load_img, load_imgs
from src.player import Player
from src.objects import Tree
from src.level import LevelLoader
from src.objects import *
from src.space import PhysicsManager

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
                       'box_0': [load_img('box.png')],
                       'dirt_0': load_img('grass.png')}
        self.physics_manager = PhysicsManager()
        # self.physics_manager.add_box((20, 20), 40, (50, 50), 30)
        self.cache = Cache(self)
        self.player = Player(self, (941, 411))
        self.init_player()
        # self.player.init(self.physics_manager)
        # self.player.shape = self.physics_manager.add_box(tuple(self.player.dimensions), 50, tuple(self.player.pos), self.player.angle)
        # self.physics_manager.space.add(self.player.shape.body, self.player.shape)
        self.scroll = pygame.Vector2(0, 0)
        self.camera_angle = 0
        self.levels = LevelLoader(self, [50, 50])
        self.levels.load_level(self.assets['dirt_0'], 'dirt_0')

        self.box = Box("box_0", self, (100, 100), [13, 13])
        self.tree = Tree("tree_0", self, (200, 200), [24, 24])
        self.init_box(self.box)
        self.init_tree(self.tree)

        self.object_chunks = None
        self.load_level("data/maps/0.json")
    
    @staticmethod
    def damp_velocity(body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, damping * 0.5, dt)
    
    def init_box(self, box):
        box.shape = self.physics_manager.add_box((13, 13), 50, pymunk.vec2d.Vec2d(box.pos.x, box.pos.y), random.random() * 360)
        box.shape.body.velocity_func = App.damp_velocity

    def init_tree(self, tree):
        tree.shape = self.physics_manager.add_box((13, 13), 50000, pymunk.vec2d.Vec2d(tree.pos.x, tree.pos.y), random.random() * 360)
        tree.shape.body.velocity_func = App.damp_velocity

    def init_player(self):
        self.player.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.player.body.friction = 0.0
        self.player.body.position = list(self.player.pos)
        self.player.body.angle = self.player.angle

        self.player.shape = pymunk.Poly.create_box(self.player.body, tuple(self.player.dimensions), 0.0)
        self.physics_manager.space.add(self.player.shape, self.player.shape.body)

    def load_level(self, path):
        with open(path, 'r') as f:
            level_data = json.load(f)
            objects = []
            for tree in level_data["trees"]:
                objects.append(Tree("tree_0", self, tree["pos"], [24, 24]))
                self.init_tree(objects[-1])
            for box in level_data["boxes"]:
                objects.append(Box("box_0", self, box["pos"], [13, 13]))
                self.init_box(objects[-1])

            self.object_chunks = ObjectChunks(objects, (50, 50), self)

    def close(self):
        self.running = False
        pygame.display.quit()
        pygame.quit()
        sys.exit()
    
    def update(self):
        self.player.update()
        self.scroll[0] += ((self.player.pos[0] - self.screen.get_width() * 0.5 - self.scroll[0])) * self.dt
        self.scroll[1] += ((self.player.pos[1] - self.screen.get_height() * 0.5 - self.scroll[1])) * self.dt
        # self.scroll = pygame.Vector2(0, 0)
        render_scroll = self.scroll.copy()
        render_scroll[0] = int(render_scroll[0])
        render_scroll[1] = int(render_scroll[1])
        # self.camera_angle += (self.player.angle - self.camera_angle) * 0.1 * self.dt
        self.time += 1 * self.dt
        self.physics_manager.update(self.dt)
        # self.physics_manager.set_draw_options(self.screen)
        # self.physics_manager.draw(self.screen)
        self.levels.draw(self.screen, self.scroll, self.camera_angle, 'dirt_0')
        self.player.draw(self.screen, self.scroll)
        self.box.update()
        self.box.draw(self.screen, render_scroll)
        self.tree.update()
        self.tree.draw(self.screen, render_scroll)

        self.object_chunks.draw(self.screen, render_scroll)
    
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
            self.update()
            pygame.transform.scale(self.screen, self.display.get_size(), self.display)
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.1f}')
            pygame.display.flip()
            self.clock.tick()

if __name__ == '__main__':
    App().run()
