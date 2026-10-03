def print_board(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                print(" . ", end="")
            elif board[i][j] == 1:
                print(" X ", end="")
            else:
                print(" O ", end="")
        print()

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != 0:
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]

    return 0  # No winner yet

def is_full(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True

def minimax(board, is_maximizing, ai_player):
    winner = check_winner(board)
    if winner == ai_player:
        return 1
    elif winner != 0:
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = -10
        current_player = ai_player
    else:
        best_score = 10
        current_player = 3 - ai_player

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = current_player
                score = minimax(board, not is_maximizing, ai_player)
                board[i][j] = 0
                if is_maximizing:
                    best_score = max(score, best_score)
                else:
                    best_score = min(score, best_score)
    return best_score

def find_best_move(board, ai_player):
    best_score = -10
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = ai_player
                score = minimax(board, False, ai_player)
                board[i][j] = 0

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

def play_game():
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)
    print("Select your mode: You play with X (1) or O (2)")
    mode = input("Enter your choice (1 or 2): ")

    if mode == "1":
        human_player = 1
        ai_player = 2
    else:
        human_player = 2
        ai_player = 1

    human_turn = human_player == 1
    while True:
        if human_turn:
            row = int(input("Enter your move (row: 0-2): "))
            col = int(input("Enter your move (col: 0-2): "))
            if not (0 <= row < 3 and 0 <= col < 3) or board[row][col] != 0:
                print("Invalid move! Try again.")
                continue
            board[row][col] = human_player
        else:
            print("AI is making a move...")
            row, col = find_best_move(board, ai_player)
            board[row][col] = ai_player

        print_board(board)

        winner = check_winner(board)
        if winner != 0:
            if winner == human_player:
                print("Congratulations! You win!")
            else:
                print("AI wins!")
            break
        elif is_full(board):
            print("Draw!")
            break

        human_turn = not human_turn

if __name__ == "__main__":
    play_game()