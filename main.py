import pygame
import os
import copy

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

def find_king(color, board_state):
    for row in range(8):
        for col in range(8):
            if board_state[row][col] == f"{color}K":
                return (row, col)
    return None

def is_square_attacked(row, col, attacker_color, board_state):
    for r in range(8):
        for c in range(8):
            piece = board_state[r][c]
            if piece and piece[0] == attacker_color:
                if is_piece_attack_valid((r, c), (row, col), board_state):
                    return True
    return False

def is_piece_attack_valid(start, end, board_state):
    sr, sc = start
    er, ec = end
    piece = board_state[sr][sc]

    if not piece:  
        return False

    color = piece[0]
    piece_type = piece[1]

    if piece_type == "P":  
        direction = -1 if color == "w" else 1
        return (abs(sc - ec) == 1 and er == sr + direction and 
                board_state[er][ec] and board_state[er][ec][0] != color)

    elif piece_type == "N":  
        return (abs(sr - er), abs(sc - ec)) in [(2, 1), (1, 2)]

    elif piece_type == "B":  
        return (abs(sr - er) == abs(sc - ec) and 
                not is_path_blocked(start, end, board_state))

    elif piece_type == "R":  
        return ((sr == er or sc == ec) and 
                not is_path_blocked(start, end, board_state))

    elif piece_type == "Q":  
        return ((abs(sr - er) == abs(sc - ec) or sr == er or sc == ec) and 
                not is_path_blocked(start, end, board_state))

    elif piece_type == "K":  
        return max(abs(sr - er), abs(sc - ec)) == 1

    return False

def is_path_blocked(start, end, board_state):
    sr, sc = start
    er, ec = end

    if sr == er:  
        step = 1 if ec > sc else -1
        for c in range(sc + step, ec, step):
            if board_state[sr][c]:
                return True

    elif sc == ec: 
        step = 1 if er > sr else -1
        for r in range(sr + step, er, step):
            if board_state[r][sc]:
                return True

    else:  
        step_r = 1 if er > sr else -1
        step_c = 1 if ec > sc else -1
        r, c = sr + step_r, sc + step_c
        while r != er and c != ec:
            if board_state[r][c]:
                return True
            r += step_r
            c += step_c

    return False

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

    temp_board = [row[:] for row in board]
    temp_board[er][ec] = temp_board[sr][sc]
    temp_board[sr][sc] = ""

    if is_in_check(color, temp_board):
        return False

    if piece_type == "P":  
        direction = -1 if color == "w" else 1
        if sc == ec:
            if (sr + direction == er and not board[er][ec]) or \
               (sr + 2 * direction == er and sr in (1, 6) and 
                not board[er][ec] and not board[sr + direction][sc]):
                return True
        elif abs(sc - ec) == 1 and er == sr + direction and \
             board[er][ec] and board[er][ec][0] != color:
            return True

    elif piece_type == "N":  
        return (abs(sr - er), abs(sc - ec)) in [(2, 1), (1, 2)]

    elif piece_type == "B":  
        return (abs(sr - er) == abs(sc - ec) and 
                not is_path_blocked(start, end, board))

    elif piece_type == "R":  
        return ((sr == er or sc == ec) and 
                not is_path_blocked(start, end, board))

    elif piece_type == "Q":  
        return ((abs(sr - er) == abs(sc - ec) or sr == er or sc == ec) and 
                not is_path_blocked(start, end, board))

    elif piece_type == "K":  
        return max(abs(sr - er), abs(sc - ec)) == 1

    return False

def is_in_check(color, board_state):
    king_pos = find_king(color, board_state)
    if king_pos:
        return is_square_attacked(king_pos[0], king_pos[1], 
                                   "b" if color == "w" else "w", 
                                   board_state)
    return False

def get_all_legal_moves(color):
    legal_moves = []
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece[0] == color:
                for r in range(8):
                    for c in range(8):
                        if is_valid_move((row, col), (r, c)):
                            legal_moves.append(((row, col), (r, c)))
    
    return legal_moves

def is_checkmate(color):
    return is_in_check(color, board) and len(get_all_legal_moves(color)) == 0

def main():
    global selected_piece, turn, board
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos)

        screen.fill((255, 255, 255))
        draw_chessboard(screen)
        draw_pieces(screen, board)

        if is_in_check(turn, board):
            print(f"{turn} is in check!")
        
        if is_checkmate(turn):
            print(f"Checkmate! {turn} loses.")
            running = False  
        pygame.display.flip()
        clock.tick(60)  
    pygame.quit()

if __name__ == "__main__":
    main()