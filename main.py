import pygame
from pygame.font import SysFont
from pygame.time import get_ticks
from utils.functions import get_moves

pygame.init()

# Constants
screen_width, screen_height = 800, 600
board_size = 8
square_size = min(screen_width, screen_height) // (board_size + 1)

# Colors
Color = pygame.Color
bg_color = Color(128, 128, 128)
selected_color = Color(255, 90, 48)
color1 = Color(238, 238, 210)
color2 = Color(118, 150, 86)

# Fonts
font = SysFont("segoeui", 26)
winner_font = SysFont("segoeui", 50)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess game")

# Chessboard properties
start_x = (screen_width - (board_size * square_size)) // 2
start_y = (screen_height - (board_size * square_size)) // 2

# Chessboard pieces
pieces = {
    "black_pawn": pygame.image.load("images/black_pawn.png"),
    "black_rook": pygame.image.load("images/black_rook.png"),
    "black_knight": pygame.image.load("images/black_knight.png"),
    "black_bishop": pygame.image.load("images/black_bishop.png"),
    "black_queen": pygame.image.load("images/black_queen.png"),
    "black_king": pygame.image.load("images/black_king.png"),
    "white_pawn": pygame.image.load("images/white_pawn.png"),
    "white_rook": pygame.image.load("images/white_rook.png"),
    "white_knight": pygame.image.load("images/white_knight.png"),
    "white_bishop": pygame.image.load("images/white_bishop.png"),
    "white_queen": pygame.image.load("images/white_queen.png"),
    "white_king": pygame.image.load("images/white_king.png")
}

# Initialize chessboard
chessBoard = [[None for _ in range(board_size)] for _ in range(board_size)]
for i in range(8):
    chessBoard[0][i] = f"black_{['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook'][i]}"
    chessBoard[1][i] = f"black_pawn"
    chessBoard[7][i] = f"white_{['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook'][i]}"
    chessBoard[6][i] = f"white_pawn"

# Game state variables
selected_piece = None
selected_piece_row = None
selected_piece_col = None
turn = "white"
possible_moves = []
game_over = False
winner = None

# Timer
time_limit = 180000
start_time = get_ticks()
white_time = time_limit
black_time = time_limit

def draw_board():
    for row in range(board_size):
        for column in range(board_size):
            color = color1 if (row + column) % 2 == 0 else color2
            if (possible_moves is not None and (row, column) in possible_moves) or (selected_piece_row == row and selected_piece_col == column):
                color = selected_color
            pygame.draw.rect(screen, color, pygame.Rect((start_x + column * square_size), (start_y + row * square_size), square_size, square_size))

            piece = chessBoard[row][column]
            if piece:
                piece_img = pygame.transform.scale(pieces[piece], (square_size, square_size))
                screen.blit(piece_img, (start_x + column * square_size, start_y + row * square_size))

def draw_game_info():
    current_turn_text = font.render(f"Current Turn: {turn.capitalize()}", True, Color("white"))
    screen.blit(current_turn_text, (280, 0))

    white_time_text = font.render(f"White Time: {white_time // 1000}", True, Color("white"))
    screen.blit(white_time_text, (60, 0))

    black_time_text = font.render(f"Black Time: {black_time // 1000}", True, Color("white"))
    screen.blit(black_time_text, (540, 0))

    if game_over:
        pygame.draw.rect(screen, bg_color, pygame.Rect(0, 0, screen_width, screen_height))
        winner_text = winner_font.render(f"Winner: {winner.capitalize()}", True, Color("white") if winner == "white" else Color("black"))
        text_rect = winner_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(winner_text, text_rect)

def handleClick(row, col):
    global selected_piece, selected_piece_row, selected_piece_col, turn, possible_moves, winner, game_over

    if selected_piece and possible_moves is not None and (row, col) in possible_moves and selected_piece.startswith(turn):
        if chessBoard[row][col] and chessBoard[row][col].endswith("king"):
            print("Game over!")
            winner = turn
            game_over = True
            chessBoard[row][col] = selected_piece
            chessBoard[selected_piece_row][selected_piece_col] = None
            return

        if selected_piece.endswith("pawn") and (row == 0 or row == board_size - 1):
            selected_piece = selected_piece.replace("pawn", "queen")
        
        chessBoard[row][col] = selected_piece
        chessBoard[selected_piece_row][selected_piece_col] = None
        turn = "white" if turn == "black" else "black"
        selected_piece = None
    elif chessBoard[row][col] and chessBoard[row][col].startswith(turn):
        selected_piece = chessBoard[row][col]
        selected_piece_row, selected_piece_col = row, col
        possible_moves = get_moves(chessBoard[row][col], row, col, chessBoard, board_size, turn)
    else:
        selected_piece = None

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            mouse_x, mouse_y = event.pos
            if start_x <= mouse_x <= start_x + (board_size * square_size) and start_y <= mouse_y <= start_y + (board_size * square_size):
                col = (mouse_x - start_x) // square_size
                row = (mouse_y - start_y) // square_size
                handleClick(row, col)

    elapsed_time = get_ticks() - start_time
    if not game_over:
        if turn == "white":
            white_time -= elapsed_time
        else:
            black_time -= elapsed_time
        start_time = get_ticks()

        if white_time <= 0:
            game_over = True
            winner = "black"
        elif black_time <= 0:
            game_over = True
            winner = "white"

    screen.fill(bg_color)
    draw_board()
    draw_game_info()
    pygame.display.update()
