import os
import sys
import time
from moves import is_legal_move, get_piece, get_color, generate_legal_moves, to_algebraic
from agent import get_agent
from eval import evaluate_board, win_probability

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

GLYPHS = {
    'WR': '♖', 'WN': '♘', 'WB': '♗', 'WQ': '♕', 'WK': '♔', 'WP': '♙',
    'BR': '♜', 'BN': '♞', 'BB': '♝', 'BQ': '♛', 'BK': '♚', 'BP': '♟',
    '--': ' '
}

ASCII = {
    'WR': 'R', 'WN': 'N', 'WB': 'B', 'WQ': 'Q', 'WK': 'K', 'WP': 'P',
    'BR': 'r', 'BN': 'n', 'BB': 'b', 'BQ': 'q', 'BK': 'k', 'BP': 'p',
    '--': '.'
}

def supports_unicode():
    # Basic heuristic; Windows terminals typically support Unicode nowadays
    return True

def print_board(board):
    use = GLYPHS if supports_unicode() else ASCII
    files = "A B C D E F G H".split()
    header = "    " + "   ".join(files)
    top =   "  " + "┌" + "┬".join(["───"] * 8) + "┐"
    mid =   "  " + "├" + "┼".join(["───"] * 8) + "┤"
    bottom ="  " + "└" + "┴".join(["───"] * 8) + "┘"

    print(header)
    print(top)
    for i, row in enumerate(board):
        rank = 8 - i
        cells = [f" {use[piece]} " for piece in row]
        print(f"{rank} " + "│" + "│".join(cells) + "│")
        if i < 7:
            print(mid)
    print(bottom)
    print(header)


def _group_captured(captured: list, use_map: dict) -> str:
    if not captured:
        return "-"
    from collections import Counter
    # Map to rendered symbol and count
    syms = [use_map[p] for p in captured]
    counts = Counter(syms)
    parts = []
    for sym, cnt in sorted(counts.items(), key=lambda x: (x[0])):
        parts.append(f"{sym} x{cnt}" if cnt > 1 else f"{sym}")
    return " ".join(parts)


def _wrap_text(text: str, width: int) -> list:
    # simple word-wrap by spaces
    if not text:
        return [""]
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= width:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def print_ui(board, captured_by_white, captured_by_black, move_log, turn=None):
    use = GLYPHS if supports_unicode() else ASCII
    files = "A B C D E F G H".split()
    header = "     " + "    ".join(files)
    top =   "  " + "┌" + "┬".join(["────"] * 8) + "┐"
    mid =   "  " + "├" + "┼".join(["────"] * 8) + "┤"
    bottom ="  " + "└" + "┴".join(["────"] * 8) + "┘"

    # Build right-side panel: Turn, Win%, Last move, Captured summaries
    side_to_move = ('White' if turn == 'W' else 'Black') if turn is not None else None
    last = None
    if move_log:
        lcolor, lstart, lend, lcap = move_log[-1]
        last = f"{('W' if lcolor=='W' else 'B')}: {to_algebraic(lstart)} {to_algebraic(lend)}"
        if lcap and lcap != '--':
            last += f" x {use[lcap]}"

    cap_w = _group_captured(captured_by_white, use)
    cap_b = _group_captured(captured_by_black, use)

    panel_items = []
    if side_to_move:
        cp = evaluate_board(board)
        prob = win_probability(cp)
        white_pct = int(round(prob * 100))
        black_pct = 100 - white_pct
        panel_items.append(f"Turn: {side_to_move}")
        panel_items.append(f"Win%: White {white_pct}% / Black {black_pct}% (cp {cp})")
    if last:
        panel_items.append(f"Last: {last}")
    panel_items.append(f"Cap W: {cap_w}")
    panel_items.append(f"Cap B: {cap_b}")

    # Wrap panel into multiple lines with fixed width
    panel_width = 32
    panel_lines = []
    for item in panel_items:
        panel_lines.extend(_wrap_text(item, panel_width))

    # Pad panel lines to match 8 ranks (top-aligned next to rank 8)
    while len(panel_lines) < 8:
        panel_lines.append("")

    # Advantage display
    cp = evaluate_board(board)
    prob = win_probability(cp)
    white_pct = int(round(prob * 100))
    black_pct = 100 - white_pct

    # Header bar
    title = " TUI Chess "
    print("╔" + "═" * 20 + title + "═" * 20 + "╗")
    print("║" + " " * (20 + len(title) + 20) + "║")
    print("╚" + "═" * (20 + len(title) + 20) + "╝")
    print(header)
    print(top)
    for i, row in enumerate(board):
        rank = 8 - i
        cells = [f" {use[piece]} " for piece in row]
        row_str = f"{rank} " + "│" + " │".join(cells) + " │"
        side = panel_lines[i]
        gap = "  "
        print(row_str + (gap + side if side else ""))
        if i < 7:
            print(mid)
    print(bottom)
    print(header)

    # Status line now appears in the right-side panel above; nothing below.

    # Move logs below (full-move table format)
    print()
    print("Moves:")
    if not move_log:
        print("(none)")
    else:
        # Build pairs: white then black
        lines = []
        tmp = []
        for ply in move_log:
            color, start, end, captured = ply
            move_txt = f"{to_algebraic(start)} {to_algebraic(end)}"
            if captured and captured != '--':
                move_txt += f" x {use[captured]}"
            tmp.append((color, move_txt))
            if len(tmp) == 2:
                lines.append(tmp)
                tmp = []
        if tmp:
            lines.append(tmp)

        # Show last 8 full moves
        last = lines[-8:]
        for i, pair in enumerate(last, start=len(lines) - len(last) + 1):
            white_move = next((m for c, m in pair if c == 'W'), " ")
            black_move = next((m for c, m in pair if c == 'B'), " ")
            print(f"{i:>2}. {white_move:<10}  {black_move:<10}")

# function to parse the input into a list where column is in alphabet and row is in number
def parse_input(token):
    token = token.strip().upper()
    if len(token) < 2 or len(token) > 3:
        raise ValueError("Square must be like E2")
    file_char = token[0]
    if file_char < 'A' or file_char > 'H':
        raise ValueError("File must be A-H")
    try:
        rank = int(token[1:])
    except ValueError:
        raise ValueError("Rank must be 1-8")
    if rank < 1 or rank > 8:
        raise ValueError("Rank must be 1-8")
    col = ord(file_char) - ord('A')
    row = 8 - rank
    return (col, row)

# function to check if the move is valid
def is_valid_move(board, start, end, turn_color):
    src = get_piece(board, start)
    if src == '--':
        return False
    if get_color(src) != turn_color:
        return False
    return is_legal_move(board, start, end)

# function to move the piece if the move is valid
def move_piece(board, start, end, turn_color):
    if is_valid_move(board, start, end, turn_color):
        board[end[1]][end[0]] = board[start[1]][start[0]]
        board[start[1]][start[0]] = '--'
        return True
    return False


# main function
def reset_board():
    return [
        ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
        ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
        ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
    ]


def menu():
    print("Select mode:")
    print("1) Human vs Human")
    print("2) Human (White) vs LLM (Black)")
    print("3) LLM (White) vs Human (Black)")
    print("4) LLM vs LLM")
    print("q) Quit")
    return input("> ").strip().lower()


def clear_screen():
    # Try ANSI escape (works in most terminals including modern Windows)
    try:
        print("\x1b[2J\x1b[H", end="")
        sys.stdout.flush()
    except Exception:
        pass
    # Fallback to system clear
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)


def human_turn(board, color):
    prompt = "White to move > " if color == 'W' else "Black to move > "
    while True:
        move = input(prompt).strip()
        if move.lower() in ("exit", "quit", "q"):
            return None
        parts = move.split()
        if len(parts) != 2:
            print("Please enter a move like 'E2 E4'.")
            continue
        try:
            start = parse_input(parts[0])
            end = parse_input(parts[1])
        except ValueError as e:
            print(f"Input error: {e}")
            continue
        captured = board[end[1]][end[0]]
        if move_piece(board, start, end, color):
            return (start, end, captured)
        print("Illegal move. Try again.")


def agent_turn(board, color, agent):
    legal = generate_legal_moves(board, color)
    if not legal:
        return None
    choice = agent.choose_move(color, legal)
    if choice is None:
        return None
    start, end = choice
    captured = board[end[1]][end[0]]
    if move_piece(board, start, end, color):
        return (start, end, captured)
    return None


def run_game(mode):
    board = reset_board()
    agent = get_agent()
    clear_screen()
    captured_by_white = []  # white captured black pieces
    captured_by_black = []  # black captured white pieces
    move_log = []  # list of tuples (color, start, end, captured_code)
    turn = 'W'
    print_ui(board, captured_by_white, captured_by_black, move_log, turn)
    while True:
        mover = None
        if mode == '1':
            mover = 'human'
        elif mode == '2':
            mover = 'human' if turn == 'W' else 'agent'
        elif mode == '3':
            mover = 'agent' if turn == 'W' else 'human'
        elif mode == '4':
            mover = 'agent'
        else:
            break

        # End if no legal moves for side to move
        legal_now = generate_legal_moves(board, turn)
        if not legal_now:
            cp = evaluate_board(board)
            if cp > 0:
                winner = 'White'
            elif cp < 0:
                winner = 'Black'
            else:
                winner = 'Draw'
            clear_screen()
            print_ui(board, captured_by_white, captured_by_black, move_log, turn)
            print()
            if winner == 'Draw':
                print('Game over: Draw (no legal moves).')
            else:
                print(f'Game over: {winner} wins (no legal moves by opponent).')
            input("Press Enter to return to menu...")
            break

        if mover == 'human':
            mv = human_turn(board, turn)
            if mv is None:
                break
        else:
            mv = agent_turn(board, turn, agent)
            if mv is None:
                # Safety: treat as no move selected
                continue
            time.sleep(0.5)

        # Update captured lists and logs
        start, end, captured = mv
        if captured and captured != '--':
            if turn == 'W':
                captured_by_white.append(captured)
            else:
                captured_by_black.append(captured)
            # Immediate win if king captured
            if len(captured) == 2 and captured[1] == 'K':
                winner = 'White' if turn == 'W' else 'Black'
                clear_screen()
                print_ui(board, captured_by_white, captured_by_black, move_log + [(turn, start, end, captured)], 'B' if turn=='W' else 'W')
                print()
                print(f'Game over: {winner} wins (king captured).')
                input("Press Enter to return to menu...")
                break
        move_log.append((turn, start, end, captured))

        # Next turn and refresh UI
        turn = 'B' if turn == 'W' else 'W'
        clear_screen()
        print_ui(board, captured_by_white, captured_by_black, move_log, turn)

    clear_screen()
    print_ui(board, captured_by_white, captured_by_black, move_log, turn)


if __name__ == "__main__":
    while True:
        clear_screen()
        choice = menu()
        if choice in ('1','2','3','4'):
            run_game(choice)
        elif choice in ('q','quit','exit'):
            break


