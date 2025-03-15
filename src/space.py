import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

FRICTION = 0.7

# a class for managing the physics of the robots & target
class PhysicsManager:
    def __init__(self) -> None:
       # set up pymunk
        self.space = pymunk.Space()
        self.space.iterations = 10
        self.space.sleep_time_threshold = 0.5

        self.static_body = self.space.static_body

        self.draw_options = None
    
    @staticmethod
    def get_pos(x, y):
        return Vec2d(x, y)

    def add_box(self, size, mass, pos: Vec2d, angle):
        body = pymunk.Body()
        self.space.add(body)

        body.position = pos
        body.angle = angle

        shape = pymunk.Poly.create_box(body, size, 0.0)
        shape.mass = mass
        shape.friction = FRICTION
        self.space.add(shape)

        return shape

    def add_circle(self, readius, mass, pos: Vec2d, angle):
        body = pymunk.Body()
        self.space.add(body)

        body.position = pos
        body.angle = angle

        shape = pymunk.Circle(body, readius, (0, 0))
        shape.mass = mass
        shape.friction = FRICTION
        self.space.add(shape)

        return shape
    
    def update(self, time_step):
        # update bodies
        self.space.step(time_step)
    
    def set_draw_options(self, surf):
        self.draw_options = pymunk.pygame_util.DrawOptions(surf)
        return self.draw_options

    def draw(self, screen):
        if not self.draw_options:
            self.set_draw_options(screen)
        self.space.debug_draw(self.draw_options)