def recognize_piece(board, start):
    return board[start[1]][start[0]][1]   

def is_legal_pawn_move(board, start):
    return True

def is_legal_rook_move(board, start):
    return True

def is_legal_bishop_move(board, start):
    return True

def is_legal_knight_move(board, start):
    return True

def is_legal_queen_move(board, start):
    return True

def is_legal_king_move(board, start):
    return True        

def is_legal_move(board, start):
    piece = recognize_piece(board, start)
    if piece == 'P':
        return is_legal_pawn_move(board, start)
    elif piece == 'R':
        return is_legal_rook_move(board, start)
    elif piece == 'B':
        return is_legal_bishop_move(board, start)
    elif piece == 'N':
        return is_legal_knight_move(board, start)
    elif piece == 'Q':
        return is_legal_queen_move(board, start)
    elif piece == 'K':
        return is_legal_king_move(board, start)
    else:
        return False

if __name__ == "__main__":
    BOARD = [
    ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
    ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
    ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
    ]

    start = [0, 0]
    print(is_legal_move(BOARD, start))        