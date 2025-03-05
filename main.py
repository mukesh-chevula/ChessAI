import pygame
import os

pygame.init()

WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8

LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

STARTING_POSITION = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
]

def load_pieces():
    pieces = {}
    piece_mapping = {
        "P": "pawn", "N": "knight", "B": "bishop",
        "R": "rook", "Q": "queen", "K": "king"
    }
    
    for color in ["w", "b"]:
        for key, piece_name in piece_mapping.items():
            image_path = os.path.join("assets", "pieces", f"{piece_name}-{color}.svg")
            try:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                pieces[f"{color}{key}"] = image
            except Exception as e:
                print(f"Error loading {image_path}: {e}")
    return pieces

PIECE_IMAGES = load_pieces()

def draw_chessboard(screen):
    for row in range(8):
        for col in range(8):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )

def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                image = PIECE_IMAGES.get(piece)
                if image:
                    screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_chessboard(screen)
    draw_pieces(screen, STARTING_POSITION)

    pygame.display.flip()

pygame.quit()
