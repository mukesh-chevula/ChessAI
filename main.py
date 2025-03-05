import pygame

pygame.init()

WIDTH, HEIGHT = 640, 640  
SQUARE_SIZE = WIDTH // 8 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.display.flip()

pygame.quit()