import pygame, sys, time, math

from maf import direction_to

class App:
    def __init__(self):
        self.display = pygame.display.set_mode((500, 500))
        self.screen = pygame.Surface((500, 500))
        self.dt = 1
        self.last_time = time.time() - 1 / 60
        self.clock = pygame.time.Clock()
        self.running = True
    
    def close(self):
        self.running = False
        pygame.quit()
        sys.exit()
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        angle = direction_to(mouse_pos, (250, 250))
        pygame.draw.line(self.screen, (255, 0, 255), (250, 250), (250 + math.cos(angle) * 100, 250 + math.sin(angle) * 100))
    
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
            pygame.transform.scale_by(self.screen, 1.0, self.display)
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.1f}')
            pygame.display.flip()
            self.clock.tick()

if __name__ == '__main__':
    App().run()
