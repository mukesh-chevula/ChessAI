import pygame
import os

# Initialize Pygame
pygame.init()

# Constants for the window size
WIDTH, HEIGHT = 640, 640  # 8x8 grid, 80x80 pixels per square
SQUARE_SIZE = WIDTH // 8  # Size of each chess square

# Colors for the chessboard
LIGHT_COLOR = (240, 217, 181)  # Light squares (beige)
DARK_COLOR = (181, 136, 99)     # Dark squares (brown)
HIGHLIGHT_COLOR = (200, 200, 0, 100)  # Yellowish highlight

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Define the starting position of the chessboard
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

board = [row[:] for row in STARTING_POSITION]  # Copy of board state

selected_piece = None  # Stores the selected piece (row, col)

# Load piece images into a dictionary

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

# Function to draw the chessboard
def draw_chessboard(screen):
    for row in range(8):
        for col in range(8):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
            # Highlight selected square
            if selected_piece == (row, col):
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight_surface.fill(HIGHLIGHT_COLOR)
                screen.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Function to draw the chess pieces
def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                image = PIECE_IMAGES.get(piece)
                if image:
                    screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Handle user clicks
def handle_click(position):
    global selected_piece
    x, y = position
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE

    if selected_piece:
        move_piece(selected_piece, (row, col))
        selected_piece = None
    else:
        if board[row][col]:  # Select a piece only if it's not empty
            selected_piece = (row, col)

# Move the selected piece
def move_piece(start, end):
    sr, sc = start
    er, ec = end

    if start != end:  # Ensure it's not clicking the same spot
        board[er][ec] = board[sr][sc]  # Move piece to new square
        board[sr][sc] = ""  # Empty old square

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)

    # Draw everything
    draw_chessboard(screen)
    draw_pieces(screen, board)

    pygame.display.flip()

pygame.quit()
