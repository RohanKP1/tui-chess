from typing import Dict

# Piece values in centipawns
PIECE_VALUES: Dict[str, int] = {
    'P': 100,
    'N': 320,
    'B': 330,
    'R': 500,
    'Q': 900,
    'K': 0,  # king safety not modeled
}


def evaluate_board(board) -> int:
    """Return evaluation in centipawns: positive favors White, negative favors Black.
    Ignores check, mobility, king safety, etc.—material only.
    """
    score = 0
    for row in board:
        for cell in row:
            if cell == '--':
                continue
            color = cell[0]
            ptype = cell[1]
            val = PIECE_VALUES.get(ptype, 0)
            score += val if color == 'W' else -val
    return score


def win_probability(cp_score: int) -> float:
    """Convert centipawn score to a pseudo win probability for White (0.0-1.0).
    Uses a logistic mapping; 300cp ~ 75%.
    """
    # Prevent overflow for extreme scores
    x = max(-2000, min(2000, cp_score)) / 300.0
    # logistic
    import math
    return 1.0 / (1.0 + math.exp(-x))
