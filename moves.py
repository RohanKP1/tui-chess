BOARD_SIZE = 8

def in_bounds(pos):
    x, y = pos
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def get_piece(board, pos):
    return board[pos[1]][pos[0]]

def get_color(piece):
    if piece == '--':
        return None
    return piece[0]  # 'W' or 'B'

def get_type(piece):
    if piece == '--':
        return None
    return piece[1]  # 'P','R','N','B','Q','K'

def is_empty(board, pos):
    return get_piece(board, pos) == '--'

def is_opponent(board, src_color, pos):
    dst_color = get_color(get_piece(board, pos))
    return dst_color is not None and dst_color != src_color

def same_color(board, a, b):
    ca = get_color(get_piece(board, a))
    cb = get_color(get_piece(board, b))
    return ca is not None and ca == cb

def path_clear(board, start, end):
    sx, sy = start
    ex, ey = end
    dx = ex - sx
    dy = ey - sy
    stepx = 0 if dx == 0 else (1 if dx > 0 else -1)
    stepy = 0 if dy == 0 else (1 if dy > 0 else -1)
    x, y = sx + stepx, sy + stepy
    while (x, y) != (ex, ey):
        if board[y][x] != '--':
            return False
        x += stepx
        y += stepy
    return True

def is_legal_pawn_move(board, start, end):
    sx, sy = start
    ex, ey = end
    piece = get_piece(board, start)
    color = get_color(piece)
    direction = -1 if color == 'W' else 1
    start_row = 6 if color == 'W' else 1
    dx = ex - sx
    dy = ey - sy

    # Forward move: one square
    if dx == 0 and dy == direction and is_empty(board, end):
        return True

    # Forward move: two squares from initial rank
    if dx == 0 and sy == start_row and dy == 2 * direction:
        middle = (sx, sy + direction)
        if is_empty(board, middle) and is_empty(board, end):
            return True

    # Capture move: one diagonal forward if opponent piece
    if abs(dx) == 1 and dy == direction and is_opponent(board, color, end):
        return True

    # No en passant in this simplified engine
    return False

def is_legal_rook_move(board, start, end):
    sx, sy = start
    ex, ey = end
    if sx != ex and sy != ey:
        return False
    if not path_clear(board, start, end):
        return False
    return True

def is_legal_bishop_move(board, start, end):
    sx, sy = start
    ex, ey = end
    if abs(ex - sx) != abs(ey - sy):
        return False
    if not path_clear(board, start, end):
        return False
    return True

def is_legal_knight_move(board, start, end):
    sx, sy = start
    ex, ey = end
    dx = abs(ex - sx)
    dy = abs(ey - sy)
    return (dx, dy) in ((1, 2), (2, 1))

def is_legal_queen_move(board, start, end):
    return is_legal_rook_move(board, start, end) or is_legal_bishop_move(board, start, end)

def is_legal_king_move(board, start, end):
    sx, sy = start
    ex, ey = end
    return max(abs(ex - sx), abs(ey - sy)) == 1

def is_legal_move(board, start, end):
    """Return True if moving piece at start to end is legal, ignoring check rules and castling/en passant."""
    if not in_bounds(start) or not in_bounds(end):
        return False
    if start == end:
        return False
    src = get_piece(board, start)
    if src == '--':
        return False
    dst = get_piece(board, end)
    # can't capture own piece
    if dst != '--' and same_color(board, start, end):
        return False

    ptype = get_type(src)
    if ptype == 'P':
        return is_legal_pawn_move(board, start, end)
    if ptype == 'R':
        return is_legal_rook_move(board, start, end)
    if ptype == 'B':
        return is_legal_bishop_move(board, start, end)
    if ptype == 'N':
        return is_legal_knight_move(board, start, end)
    if ptype == 'Q':
        return is_legal_queen_move(board, start, end)
    if ptype == 'K':
        return is_legal_king_move(board, start, end)
    return False

# --- Move generation helpers ---

FILES = 'ABCDEFGH'

def to_algebraic(pos):
    x, y = pos
    return f"{FILES[x]}{8 - y}"

def generate_moves_for_piece(board, start):
    sx, sy = start
    piece = get_piece(board, start)
    color = get_color(piece)
    ptype = get_type(piece)
    if piece == '--':
        return []
    moves = []

    def add_if_legal(x, y):
        end = (x, y)
        if in_bounds(end) and (is_empty(board, end) or is_opponent(board, color, end)):
            if is_legal_move(board, start, end):
                moves.append(end)

    if ptype == 'P':
        direction = -1 if color == 'W' else 1
        # forward
        f1 = (sx, sy + direction)
        if in_bounds(f1) and is_empty(board, f1):
            if is_legal_move(board, start, f1):
                moves.append(f1)
            start_row = 6 if color == 'W' else 1
            f2 = (sx, sy + 2*direction)
            if sy == start_row and is_empty(board, f2):
                if is_legal_move(board, start, f2):
                    moves.append(f2)
        # captures
        for dx in (-1, 1):
            ex = sx + dx
            ey = sy + direction
            if 0 <= ex < BOARD_SIZE and 0 <= ey < BOARD_SIZE and is_opponent(board, color, (ex, ey)):
                if is_legal_move(board, start, (ex, ey)):
                    moves.append((ex, ey))

    elif ptype == 'N':
        for dx, dy in ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)):
            add_if_legal(sx+dx, sy+dy)

    elif ptype in ('B','R','Q'):
        directions = []
        if ptype in ('B','Q'):
            directions += [(1,1), (1,-1), (-1,1), (-1,-1)]
        if ptype in ('R','Q'):
            directions += [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            x, y = sx+dx, sy+dy
            while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                if is_empty(board, (x,y)):
                    if is_legal_move(board, start, (x,y)):
                        moves.append((x,y))
                else:
                    if is_opponent(board, color, (x,y)) and is_legal_move(board, start, (x,y)):
                        moves.append((x,y))
                    break
                x += dx
                y += dy

    elif ptype == 'K':
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx == 0 and dy == 0:
                    continue
                add_if_legal(sx+dx, sy+dy)

    return moves

def generate_legal_moves(board, color):
    moves = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if get_color(board[y][x]) == color:
                start = (x, y)
                for end in generate_moves_for_piece(board, start):
                    moves.append((start, end))
    return moves

if __name__ == "__main__":
    # simple self-checks
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
    assert is_legal_move(BOARD, (0, 6), (0, 4))  # white pawn two steps
    assert not is_legal_move(BOARD, (0, 6), (0, 3))
    print("Basic move validation self-checks passed.")