import pygame

pygame.init()

display = pygame.display.set_mode((500, 500))

level_img = pygame.image.load("data/images/grass.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            break

    display.fill((0, 0, 0))
    display.blit(level_img, (0, 0))
    pygame.draw.rect(display, (255, 0, 0), (0, 0, 50, 50))
    pygame.display.flip()