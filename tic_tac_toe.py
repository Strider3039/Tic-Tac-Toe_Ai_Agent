"""
nxn Tic-Tac-Toe Game
Text-based implementation for Checkpoint 1 (Week 8).
Designed for board sizes up to 10x10. Extensible for UI and Minimax in later checkpoints.
"""

from typing import Optional


def create_board(size: int) -> list[list[str]]:
    """Create an empty nxn board."""
    return [[" " for _ in range(size)] for _ in range(size)]


def display_board(board: list[list[str]]) -> None:
    """Print the board to the console."""
    size = len(board)
    cell_width = max(2, len(str(size * size)))
    
    # Print column numbers
    header = "   " + " ".join(str(j + 1).rjust(cell_width) for j in range(size))
    print(header)
    print("   " + "-" * (size * (cell_width + 1)))
    
    for i in range(size):
        row_str = str(i + 1).rjust(2) + "|"
        for j in range(size):
            cell = board[i][j] if board[i][j] != " " else "."
            row_str += cell.center(cell_width + 1)
        print(row_str)


def get_move(board: list[list[str]], player: str) -> tuple[int, int]:
    """Prompt the player for a move. Returns (row, col) in 0-indexed form."""
    size = len(board)
    
    while True:
        try:
            raw = input(f"Player {player}, enter row and column (e.g. 1 2): ").strip().split()
            if len(raw) != 2:
                print("Enter two numbers: row and column.")
                continue
            
            row = int(raw[0])
            col = int(raw[1])
            
            if 1 <= row <= size and 1 <= col <= size:
                if board[row - 1][col - 1] == " ":
                    return row - 1, col - 1
                else:
                    print("That cell is already taken.")
            else:
                print(f"Row and column must be between 1 and {size}.")
        except ValueError:
            print("Invalid input. Enter two numbers.")


def check_winner(board: list[list[str]], row: int, col: int, player: str) -> bool:
    """
    Check if the last move at (row, col) wins the game for player.
    """
    size = len(board)
    
    # Check row
    if all(board[row][j] == player for j in range(size)):
        return True
    
    # Check column
    if all(board[i][col] == player for i in range(size)):
        return True
    
    # Check main diagonal (top-left to bottom-right)
    if row == col and all(board[i][i] == player for i in range(size)):
        return True
    
    # Check anti-diagonal (top-right to bottom-left)
    if row + col == size - 1 and all(board[i][size - 1 - i] == player for i in range(size)):
        return True
    
    return False


def is_board_full(board: list[list[str]]) -> bool:
    """Check if the board has no empty cells."""
    return all(board[i][j] != " " for i in range(len(board)) for j in range(len(board)))


def play_game(board_size: int = 3) -> Optional[str]:
    """
    Run one game of Tic-Tac-Toe.
    Returns the winning player ("X" or "O"), or None for a draw.
    """
    board = create_board(board_size)
    current_player = "X"
    
    while True:
        display_board(board)
        
        if current_player == "O": # ai player
            row, col = get_best_move(board)
        else:
            row, col = get_move(board, current_player)
    
        board[row][col] = current_player
        
        if check_winner(board, row, col, current_player):
            display_board(board)
            print(f"\nPlayer {current_player} wins!")
            return current_player
        
        if is_board_full(board):
            display_board(board)
            print("\nIt's a draw!")
            return None
        
        current_player = "O" if current_player == "X" else "X"

# ============================ MINIMAX ==================================

def minimax(board: list[list[str]], is_maximizing: bool, last_move: Optional[tuple[int, int]]) -> int:
    """
    Minimax evaluation of the board.
    simulates all possible moves with ai as maximizer and player as minimizer
    Returns:
        -1 if X wins (player)
        +1 if O wins (ai)
         0 if draw
    """
    # check the terminal state (win, lose, draw)
    if last_move is not None:
        row, col = last_move
        last_player = "X" if is_maximizing else "O"
        
        if check_winner(board, row, col, last_player):
            return 1 if last_player == "O" else -1

    if is_board_full(board):
        return 0

    size = len(board)

    if is_maximizing: # simulated ai turn
        best_score = float("-inf")
        player = "O"

        # find best posible move for ai
        for i in range(size):
            for j in range(size):
                if board[i][j] == " ":
                    board[i][j] = player
                    score = minimax(board, False, (i, j)) # false bc the next simulated turn will be the player's
                    board[i][j] = " "  # undo move
                    best_score = max(best_score, score)

        return best_score
    else: # simulated player turn
        best_score = float("inf")
        player = "X"

        # find best possible move for player
        for i in range(size):
            for j in range(size):
                if board[i][j] == " ":
                    board[i][j] = player
                    score = minimax(board, True, (i, j)) # true bc the next simulated turn is the ai's
                    board[i][j] = " "  # undo move
                    best_score = min(best_score, score)

        return best_score

def get_best_move(board: list[list[str]]) -> tuple[int, int]:
    best_score = float("-inf")
    best_move = None
    size = len(board)

    # find the minimax value for each possible move, and record the best one
    for i in range(size):
        for j in range(size):
            if board[i][j] == " ":
                board[i][j] = "O" # try this move
                score = minimax(board, False, (i, j))
                board[i][j] = " " # undo move
                print(score)
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

def main() -> None:
    """Main entry point."""
    print("=== nxn Tic-Tac-Toe ===\n")
    
    while True:
        try:
            size_input = input("Enter board size n (2-10, default 3): ").strip()
            size = int(size_input) if size_input else 3
            if 2 <= size <= 10:
                break
            print("Board size must be between 2 and 10.")
        except ValueError:
            print("Enter a valid number.")
    
    play_game(size)
    
    again = input("\nPlay again? (y/n): ").strip().lower()
    if again in ("y", "yes"):
        main()
    else:
        print("Thanks for playing!")


if __name__ == "__main__":
    main()
