from moves import is_legal_move

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

# function to print the board
def print_board(board):
    for row in board:
        print(" ".join(row))
    print()    

# function to parse the input into a list where column is in alphabet and row is in number
def parse_input(input):
    input = input.upper()
    column = ord(input[0]) - 65
    row = 8 - int(input[1])
    return [column, row]  

# function to check if the move is valid
def is_valid_move(board, start, end):
    if board[start[1]][start[0]] == '--':
        return False
    elif board[start[1]][start[0]][0] == board[end[1]][end[0]][0] and is_legal_move(board, start):
        return False      
    return True

# function to move the piece if the move is valid
def move_piece(board, start, end):
    if is_valid_move(board, start, end):
        board[end[1]][end[0]] = board[start[1]][start[0]]
        board[start[1]][start[0]] = '--'
        return True
    else:
       return False    


# main function
if __name__ == "__main__":
    # while loop untill input is exit
    while True:
        move = input()
        if move == 'exit':
            break

        # take starting and ending position as input
        start, end = move.split()

        # parse the input
        start = parse_input(start)
        end = parse_input(end)

        # print(start, end)
        # print(BOARD[start[1]][start[0]])
        # print(BOARD[end[1]][end[0]])
        # print(is_valid_move(BOARD, start, end))

        # move the piece
        if move_piece(BOARD, start, end):
            print_board(BOARD)
        else:
            print("Invalid Move")    


