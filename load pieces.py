
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
