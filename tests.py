import pygame, sys, time, random, math

class App:
    def __init__(self):
        self.display = pygame.display.set_mode((500, 500))
        self.screen = pygame.Surface((500, 500))
        self.time = 0
        self.dt = 1
        self.last_time = time.time() - 1 / 60
        self.clock = pygame.time.Clock()
        self.running = True
        self.angle = 0
        self.camera_pos = pygame.Vector2(0, 0)
        self.points = [[random.randint(0, 250), random.randint(0, 250)] for _ in range(10000)]
    
    def close(self):
        self.running = False
        pygame.display.quit()
        pygame.quit()
        sys.exit()
    
    def update(self):
        self.angle += 1 * self.dt
        self.camera_pos = pygame.Vector2(pygame.mouse.get_pos())
        for point in self.points:
            pos = pygame.Vector2(point) - self.camera_pos
            pos.rotate_ip(self.angle)
            pos += self.camera_pos
            self.screen.set_at(pos, (255, 255, 255))
    
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
            pygame.transform.scale(self.screen, self.display.get_size(), self.display)
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.1f}')
            pygame.display.flip()
            self.clock.tick()

if __name__ == '__main__':
    App().run()
