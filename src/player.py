import math, pygame, pymunk

from .stacked_sprite import SpriteStack
from .space import PhysicsManager

class Player:
    def __init__(self, app, pos):
        self.app = app
        self.pos = pygame.Vector2(pos)
        self.car = SpriteStack(app, pos, self.app.assets['car_0'], (14, 17), 'car_0', 1, 2, 14) #app, pos, sheet, dim, name, spread, accuracy, padding, variant=0
        self.movement = 0
        self.target_motion = pygame.Vector2(0, 0)
        self.motion = pygame.Vector2(0, 0)
        self.target_angle = 0
        self.friction = 0.09
        self.turning = 0
        self.drifting = True
        self.controls = {'up': False, 'down': False, 'left': False, 'right': False, 'brake': False}
        self.turning = 0
        self.angle = 0
        self.speed = 0.01

        self.dimensions = pygame.Vector2(14, 17)

        self.body = None
        self.shape = None
    
    @staticmethod
    def damp_velocity(body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, damping * 0.5, dt)

    def update(self):
        if self.controls['up']:
            self.movement += self.speed * self.app.dt
        if self.controls['down']:
            self.movement -= self.speed * self.app.dt
        if not (self.controls['down'] or self.controls['up']):
            self.movement += (self.movement * 0.97 - self.movement) * self.app.dt
        if self.controls['brake']:
            self.movement += (self.movement * 0.95 - self.movement) * self.app.dt
            self.turning += (self.turning * 0.9 - self.turning) * self.app.dt
        self.movement = min(max(-5, self.movement), 5)
        if self.controls['left']:
            self.turning += 0.05 * self.app.dt
        if self.controls['right']:
            self.turning -= 0.05 * self.app.dt
        if not (self.controls['left'] or self.controls['right']):
            self.turning += (self.turning * 0.65 - self.turning) * self.app.dt
        self.turning = min(max(-2, self.turning), 2)
        self.angle += self.turning * self.app.dt
        self.target_motion.x = math.cos(math.radians(self.angle + 90)) * self.movement
        self.target_motion.y = -math.sin(math.radians(self.angle + 90)) * self.movement
        self.motion += (self.target_motion - self.motion) * self.friction * self.app.dt
        self.pos += self.motion * self.app.dt

        self.shape.body.velocity = pymunk.vec2d.Vec2d(
            self.pos.x + self.dimensions.x / 2 - self.shape.body.position.x,
            self.pos.y + 5 - self.shape.body.position.y
        )
        self.shape.body.angle = math.radians(-self.angle)
        
    def draw(self, surf, scroll=(0, 0)):
        shadow = self.car.get_shadow(self.angle + 180 - self.app.camera_angle)
        surf.blit(shadow, (self.pos[0] - shadow.get_width() // 2 - scroll[0] + 4, self.pos[1] - scroll[1] - shadow.get_height() // 2 + 1))
        surf.blit(self.car.get_img(self.angle + 180 - self.app.camera_angle), (self.pos[0] - scroll[0] - 13, self.pos[1] - scroll[1] - 13))