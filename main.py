import pygame
import os

pygame.init()

WIDTH, HEIGHT = 640, 640  
SQUARE_SIZE = WIDTH // 8  

LIGHT_COLOR = (240, 217, 181)  
DARK_COLOR = (181, 136, 99)     
HIGHLIGHT_COLOR = (200, 200, 0, 100)  

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

board = [row[:] for row in STARTING_POSITION]  
selected_piece = None  
turn = "w"  

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
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if selected_piece == (row, col):
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight_surface.fill(HIGHLIGHT_COLOR)
                screen.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                image = PIECE_IMAGES.get(piece)
                if image:
                    screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def handle_click(position):
    global selected_piece, turn
    x, y = position
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE

    if selected_piece:
        if is_valid_move(selected_piece, (row, col)):
            move_piece(selected_piece, (row, col))
            selected_piece = None
            turn = "b" if turn == "w" else "w"  
        else:
            selected_piece = None  
    else:
        if board[row][col] and board[row][col][0] == turn:  
            selected_piece = (row, col)

def move_piece(start, end):
    sr, sc = start
    er, ec = end

    if start != end:  
        board[er][ec] = board[sr][sc]  
        board[sr][sc] = ""  

def is_valid_move(start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]

    if not piece:  
        return False

    if start == end:
        return False

    color = piece[0]
    piece_type = piece[1]

    if board[er][ec] and board[er][ec][0] == color:
        return False

    if piece_type == "P":  
        return is_valid_pawn_move(start, end, color)

    elif piece_type == "N":  
        return is_valid_knight_move(start, end)

    elif piece_type == "B":  
        return is_valid_bishop_move(start, end)

    elif piece_type == "R":  
        return is_valid_rook_move(start, end)

    elif piece_type == "Q":  
        return is_valid_queen_move(start, end)

    elif piece_type == "K":  
        return is_valid_king_move(start, end)

    return False

def is_valid_pawn_move(start, end, color):
    sr, sc = start
    er, ec = end
    direction = -1 if color == "w" else 1  

    if sc == ec:  
        if (sr + direction == er and not board[er][ec]) or (sr + 2 * direction == er and sr in (1, 6) and not board[er][ec] and not board[sr + direction][sc]):
            return True  

    elif abs(sc - ec) == 1 and er == sr + direction and board[er][ec] and board[er][ec][0] != color:
        return True  

    return False

def is_valid_knight_move(start, end):
    sr, sc = start
    er, ec = end
    return (abs(sr - er), abs(sc - ec)) in [(2, 1), (1, 2)]

def is_valid_bishop_move(start, end):
    sr, sc = start
    er, ec = end
    return abs(sr - er) == abs(sc - ec) and not is_blocked(start, end)

def is_valid_rook_move(start, end):
    sr, sc = start
    er, ec = end
    return (sr == er or sc == ec) and not is_blocked(start, end)

def is_valid_queen_move(start, end):
    return is_valid_bishop_move(start, end) or is_valid_rook_move(start, end)

def is_valid_king_move(start, end):
    sr, sc = start
    er, ec = end
    return max(abs(sr - er), abs(sc - ec)) == 1

def is_blocked(start, end):
    sr, sc = start
    er, ec = end

    if sr == er:  
        step = 1 if ec > sc else -1
        for c in range(sc + step, ec, step):
            if board[sr][c]:
                return True

    elif sc == ec:  
        step = 1 if er > sr else -1
        for r in range(sr + step, er, step):
            if board[r][sc]:
                return True

    else:  
        step_r = 1 if er > sr else -1
        step_c = 1 if ec > sc else -1
        r, c = sr + step_r, sc + step_c
        while r != er and c != ec:
            if board[r][c]:
                return True
            r += step_r
            c += step_c

    return False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)

    draw_chessboard(screen)
    draw_pieces(screen, board)

    pygame.display.flip()

pygame.quit()
