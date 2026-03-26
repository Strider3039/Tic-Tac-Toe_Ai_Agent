import pygame
import sys
import random
from tic_tac_toe import create_board, check_winner, is_board_full

WINDOW_SIZE = 600
BG_COLOR = (28, 28, 28)
LINE_COLOR = (200, 200, 200)
X_COLOR = (229, 115, 115)
O_COLOR = (100, 181, 246)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)
STATUS_BAR_HEIGHT = 60

HUMAN = "X"
AI = "O"


def get_ai_move(board):
    """
    Placeholder AI: picks a random empty cell.
    Replace this function with the Minimax + Alpha-Beta implementation.
    Should return (row, col).
    """
    empty_cells = [
        (r, c)
        for r in range(len(board))
        for c in range(len(board))
        if board[r][c] == " "
    ]
    return random.choice(empty_cells)


def get_font(size):
    return pygame.font.SysFont("Arial", size)


def draw_grid(screen, board_size, cell_size):
    """Draw the grid lines."""
    for i in range(1, board_size):
        pygame.draw.line(screen, LINE_COLOR,
                         (i * cell_size, 0),
                         (i * cell_size, WINDOW_SIZE), 2)
        pygame.draw.line(screen, LINE_COLOR,
                         (0, i * cell_size),
                         (WINDOW_SIZE, i * cell_size), 2)


def draw_pieces(screen, board, cell_size):
    """Draw X and O pieces on the board."""
    board_size = len(board)
    margin = cell_size // 5

    for row in range(board_size):
        for col in range(board_size):
            piece = board[row][col]
            cx = col * cell_size + cell_size // 2
            cy = row * cell_size + cell_size // 2

            if piece == "X":
                top_left = (col * cell_size + margin, row * cell_size + margin)
                bottom_right = ((col + 1) * cell_size - margin, (row + 1) * cell_size - margin)
                top_right = ((col + 1) * cell_size - margin, row * cell_size + margin)
                bottom_left = (col * cell_size + margin, (row + 1) * cell_size - margin)
                pygame.draw.line(screen, X_COLOR, top_left, bottom_right, 4)
                pygame.draw.line(screen, X_COLOR, top_right, bottom_left, 4)

            elif piece == "O":
                radius = cell_size // 2 - margin
                pygame.draw.circle(screen, O_COLOR, (cx, cy), radius, 4)


def draw_status_bar(screen, message, board_size):
    """Draw the status bar at the bottom with the current game message."""
    bar_rect = pygame.Rect(0, WINDOW_SIZE, WINDOW_SIZE, STATUS_BAR_HEIGHT)
    pygame.draw.rect(screen, (40, 40, 40), bar_rect)

    font = get_font(max(18, 32 - board_size * 2))
    text = font.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE + STATUS_BAR_HEIGHT // 2))
    screen.blit(text, text_rect)


def draw_restart_button(screen, mouse_pos):
    """Draw a restart button and return its rect."""
    button_rect = pygame.Rect(WINDOW_SIZE - 110, WINDOW_SIZE + 10, 100, 40)
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect, border_radius=6)

    font = get_font(18)
    label = font.render("Restart", True, TEXT_COLOR)
    label_rect = label.get_rect(center=button_rect.center)
    screen.blit(label, label_rect)

    return button_rect


def get_board_size_from_user():
    """Show a screen to let the user pick a board size between 2 and 10."""
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Tic-Tac-Toe - Choose Board Size")
    input_text = ""
    error = ""

    while True:
        screen.fill(BG_COLOR)

        title_font = get_font(28)
        msg_surf = title_font.render("Enter board size (2-10) and press Enter:", True, TEXT_COLOR)
        screen.blit(msg_surf, msg_surf.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 60)))

        input_box = pygame.Rect(WINDOW_SIZE // 2 - 40, WINDOW_SIZE // 2 - 10, 80, 44)
        pygame.draw.rect(screen, (60, 60, 60), input_box, border_radius=6)
        pygame.draw.rect(screen, LINE_COLOR, input_box, 2, border_radius=6)

        input_font = get_font(30)
        input_surf = input_font.render(input_text, True, TEXT_COLOR)
        screen.blit(input_surf, input_surf.get_rect(center=input_box.center))

        if error:
            err_font = get_font(20)
            err_surf = err_font.render(error, True, (255, 100, 100))
            screen.blit(err_surf, err_surf.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 60)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        size = int(input_text)
                        if 2 <= size <= 10:
                            return size
                        else:
                            error = "Please enter a number between 2 and 10."
                            input_text = ""
                    except ValueError:
                        error = "Invalid input. Please enter a number."
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() and len(input_text) < 2:
                    input_text += event.unicode


def main():
    pygame.init()

    board_size = get_board_size_from_user()
    cell_size = WINDOW_SIZE // board_size

    total_height = WINDOW_SIZE + STATUS_BAR_HEIGHT
    screen = pygame.display.set_mode((WINDOW_SIZE, total_height))
    pygame.display.set_caption("Tic-Tac-Toe")

    board = create_board(board_size)
    game_over = False
    status_message = "Your turn (X)"

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                restart_btn = draw_restart_button(screen, mouse_pos)

                if restart_btn.collidepoint(event.pos):
                    board_size = get_board_size_from_user()
                    cell_size = WINDOW_SIZE // board_size
                    screen = pygame.display.set_mode((WINDOW_SIZE, total_height))
                    board = create_board(board_size)
                    game_over = False
                    status_message = "Your turn (X)"
                    continue

                if not game_over and event.pos[1] < WINDOW_SIZE:
                    col = event.pos[0] // cell_size
                    row = event.pos[1] // cell_size

                    if 0 <= row < board_size and 0 <= col < board_size:
                        if board[row][col] == " ":
                            board[row][col] = HUMAN

                            if check_winner(board, row, col, HUMAN):
                                status_message = "You win!"
                                game_over = True
                            elif is_board_full(board):
                                status_message = "It's a draw!"
                                game_over = True
                            else:
                                status_message = "thinking..."
                                draw_status_bar(screen, status_message, board_size)
                                pygame.display.flip()

                                ai_row, ai_col = get_ai_move(board)
                                board[ai_row][ai_col] = AI

                                if check_winner(board, ai_row, ai_col, AI):
                                    status_message = "AI wins!"
                                    game_over = True
                                elif is_board_full(board):
                                    status_message = "It's a draw!"
                                    game_over = True
                                else:
                                    status_message = "Your turn (X)"

        screen.fill(BG_COLOR)
        draw_grid(screen, board_size, cell_size)
        draw_pieces(screen, board, cell_size)
        draw_status_bar(screen, status_message, board_size)
        draw_restart_button(screen, mouse_pos)

        pygame.display.flip()


if __name__ == "__main__":
    main()