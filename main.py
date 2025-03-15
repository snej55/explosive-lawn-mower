import pygame, sys, time, json, pymunk, random, asyncio

from src.imgs import Cache, RotImg
from src.utils import load_img, load_imgs, snip
from src.player import Player
from src.objects import Tree
from src.level import LevelLoader
from src.objects import *
from src.space import PhysicsManager
from src.grass import GrassManager
from src.bip import TILE_SIZE

pygame.mixer.init()

SMOKE_DELAY = 100
FADE = 4

class Smoke:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = 100
        self.timer = 0
        self.img = pygame.Surface((self.size, self.size))
        pygame.draw.rect(self.img, (200, 200, 200), (1, 1, self.size - 2, self.size - 2))
        self.img.set_colorkey((0, 0, 0))
        self.img.convert_alpha()
        self.target_angle = random.random() * 360 + 720
        self.angle = 0
        self.smoke = []
    
    @property
    def pos(self):
        return self.x, self.y
    
    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.dx += (self.dx * 0.989 - self.dx) * dt
        self.dy += (self.dy * 0.989 - self.dy) * dt
        self.timer += 1 * dt
        self.angle += (self.target_angle - self.angle) / 15 * dt
    
    def draw(self, surf, scroll=[0, 0]):
        self.img.set_alpha(int(255 - 255 * self.timer / SMOKE_DELAY * FADE))
        img_copy = pygame.transform.scale(pygame.transform.rotate(self.img, (self.angle)),
                                          (1 + self.size * self.timer / SMOKE_DELAY, 1 + self.size * self.timer / SMOKE_DELAY)).convert_alpha()
        surf.blit(img_copy, (self.x - scroll[0], self.y - scroll[1]))

class App:
    def __init__(self):
        self.display = pygame.display.set_mode((640, 640), pygame.RESIZABLE)
        self.display.fill((100, 240, 100))
        pygame.display.flip()
        self.screen = pygame.Surface((320, 320))
        self.time = 0
        self.dt = 1
        self.last_time = time.time() - 1 / 60
        self.clock = pygame.time.Clock()
        self.running = True
        self.assets = {'car_0': load_img('car.png'),
                       'tree_0': [load_img('tree_0.png')],
                       'box_0': [load_img('box.png')],
                       'dirt_0': load_img('grass.png'),
                       'light': load_img('light.png'),
                       'leaf': load_img('leaf.png')}
        filt = pygame.Surface(self.assets['light'].get_size())
        filt.fill((0, 0, 0))
        filt.set_alpha(200)
        self.assets['light'].blit(filt, (0, 0))
        self.physics_manager = PhysicsManager()
        # self.physics_manager.add_box((20, 20), 40, (50, 50), 30)
        self.cache = Cache(self)
        self.player = Player(self, (50, 50))#, (941, 411))
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

        self.grass_locs = []
        for x in range(int(self.assets["dirt_0"].get_width() / TILE_SIZE)):
            for y in range(int(self.assets["dirt_0"].get_height() / TILE_SIZE)):
                self.grass_locs.append(f"{x};{y}")
        print(f"{len(self.grass_locs) * 64} blades of grass")
        
        self.grass_img = load_img("grass_blades.png")
        self.grass_manager = GrassManager(self.grass_locs, self.grass_img)

        self.leaf_anim = [snip(self.assets['leaf'], (8 * x, 0), (8, 8)) for x in range(17)]
        self.leaves = []

        self.revving = False

        self.screen_shake = 0.0
        self.smoke = []

        pygame.mixer.music.load("data/audio/ben.wav")
        pygame.mixer.music.play(-1)
    
    @staticmethod
    def damp_velocity(body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, damping * 0.5, dt)
    
    def add_leaf(self, pos):
        # xy pos, vel, height, frame
        self.leaves.append([pos, [random.random() - 0.5, -random.random()], random.random() * 20, random.randint(0, 2)])
    
    def update_leaves(self, scroll):
        for i, leaf in sorted(enumerate(self.leaves), reverse=True):
            leaf[0][0] += leaf[1][0] * self.dt
            leaf[2] += leaf[1][1] * self.dt
            leaf[0][0] += math.sin(leaf[3] * 0.035) * 0.3 * self.dt
            leaf[1][1] = min(0.2, leaf[1][1] + 0.005 * self.dt)
            leaf[3] += 0.2 * self.dt
            if leaf[3] >= 17:
                self.leaves.pop(i)
            else:
                self.screen.blit(self.leaf_anim[math.floor(leaf[3])], (leaf[0][0] - scroll[0], leaf[0][1] - leaf[2] - scroll[1]))
                # self.screen.blit(self.leaf_anim[math.floor(leaf[3])], (leaf[0][0] - scroll[0], leaf[0][1] - scroll[1]), special_flags=pygame.BLEND_RGBA_SUB)
    
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
        self.screen_shake = max(0, self.screen_shake - 1 * self.dt)

        screen_shake_offset = (random.random() * self.screen_shake - self.screen_shake / 2, random.random() * self.screen_shake - self.screen_shake / 2)
        render_scroll = pygame.Vector2(int(self.scroll[0] + screen_shake_offset[0]), int(self.scroll[1] + screen_shake_offset[1]))
        # self.camera_angle += (self.player.angle - self.camera_angle) * 0.1 * self.dt
        self.time += 1 * self.dt
        self.physics_manager.update(self.dt)
        # self.physics_manager.set_draw_options(self.screen)
        # self.physics_manager.draw(self.screen)
        self.levels.draw(self.screen, render_scroll, self.camera_angle, 'dirt_0')
        self.grass_manager.render(pygame.Rect(self.player.pos.x, self.player.pos.y, 14, 14), self.dt, self.screen, render_scroll)
        self.screen.blit(pygame.transform.scale(self.assets['light'], (50, 50)), (self.player.pos.x - 17 - render_scroll[0], self.player.pos.y - 22 - render_scroll[1]), special_flags=pygame.BLEND_RGBA_SUB)
        self.player.draw(self.screen, self.scroll)
        self.box.update()
        self.box.draw(self.screen, render_scroll)
        self.tree.update()
        self.tree.draw(self.screen, render_scroll)
        self.object_chunks.draw(self.screen, render_scroll)
        if self.revving:
            self.check_to_destroy()
        self.update_leaves(render_scroll)
        for i, bit in sorted(enumerate(self.smoke), reverse=True):
            bit.update(self.dt)
            if bit.timer > SMOKE_DELAY // FADE:
                self.smoke.pop(i)
            bit.draw(self.screen, render_scroll)
    
    def check_to_destroy(self):
        for offset in [(-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (-1, -1), (0, -1), (1, -1)]:
            pos = pygame.Vector2(self.player.pos.x + self.player.dimensions.x / 2 + offset[0] * TILE_SIZE, 
                                 self.player.pos.y + self.player.dimensions.y / 2 + offset[1] * TILE_SIZE)
            loc = f"{math.floor(pos.x / TILE_SIZE)};{math.floor(pos.y / TILE_SIZE)}"
            if loc in self.grass_manager.grass_tiles:
                del self.grass_manager.grass_tiles[loc]
                self.screen_shake = max(self.screen_shake, 16)
                for x in range(TILE_SIZE // 4):
                    for y in range(TILE_SIZE // 4):
                        if random.random() < 0.2:
                            self.smoke.append(Smoke(math.floor(pos.x / TILE_SIZE) * TILE_SIZE + x * 4, math.floor(pos.y / TILE_SIZE) * TILE_SIZE + y * 4, random.randint(-1, 1), -1.1))
                        self.add_leaf(pygame.Vector2(math.floor(pos.x / TILE_SIZE) * TILE_SIZE + x * 4, math.floor(pos.y / TILE_SIZE) * TILE_SIZE + y * 4))
    
    async def run(self):
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
                        self.revving = True
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
                    if event.key == pygame.K_r:
                        self.revving = False
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.Surface((event.w // 2, event.h // 2))

            self.update()
            pygame.transform.scale(self.screen, self.display.get_size(), self.display)
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.1f}')
            pygame.display.flip()
            self.clock.tick()
            await asyncio.sleep(0)

async def main():
    app = App()
    await app.run()
    await asyncio.sleep(0)

if __name__ == '__main__':
    asyncio.run(main())
