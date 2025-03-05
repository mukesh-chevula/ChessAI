import pygame

pygame.init()

WIDTH, HEIGHT = 640, 640  
SQUARE_SIZE = WIDTH // 8 
LIGHT_COLOR = (240, 217, 181)  
DARK_COLOR = (181, 136, 99)     

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

def draw_chessboard(screen):
    for row in range(8):
        for col in range(8):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_chessboard(screen)


    pygame.display.flip()

pygame.quit()