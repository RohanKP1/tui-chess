import unittest
from moves import is_legal_move


class TestMoves(unittest.TestCase):
    def setUp(self):
        self.board = [
            ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
            ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
            ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
        ]

    def test_white_pawn_two_steps_from_start(self):
        self.assertTrue(is_legal_move(self.board, (0, 6), (0, 4)))

    def test_white_pawn_three_steps_illegal(self):
        self.assertFalse(is_legal_move(self.board, (0, 6), (0, 3)))

    def test_rook_blocked_by_piece(self):
        # Move white pawn one step to open rook path
        self.board[5][0] = 'WP'
        self.board[6][0] = '--'
        # Rook can't jump over a pawn at (0,5)
        self.assertFalse(is_legal_move(self.board, (0, 7), (0, 4)))

    def test_knight_jump(self):
        # Knight at b1 to c3
        self.assertTrue(is_legal_move(self.board, (1, 7), (2, 5)))


if __name__ == '__main__':
    unittest.main()
