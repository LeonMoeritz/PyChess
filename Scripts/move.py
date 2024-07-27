import tkinter as tk
import pyautogui
import time
from PIL import Image, ImageTk
import chess  # Ensure you have the python-chess library installed

# Define the coordinates for each chessboard square
BOARD_LEFT = 223
BOARD_TOP = 103
SQUARE_SIZE = 912 // 8  # The size of each square on the board

def get_square_coords(board_left, board_top, square_size):
    squares = {}
    for row in range(8):
        for col in range(8):
            square_name = f"{chr(97 + col)}{8 - row}"  # 'a1', 'b1', ..., 'h8'
            x = board_left + col * square_size
            y = board_top + row * square_size
            squares[square_name] = (x, y)
    return squares

def highlight_square(canvas, x, y, size, color="red"):
    canvas.create_rectangle(x, y, x + size, y + size, outline=color, width=5)

def perform_move(move, board_left, board_top, square_size):
    square_coords = get_square_coords(board_left, board_top, square_size)

    # Convert Move object to UCI format
    move_uci = move.uci()

    if len(move_uci) == 4:  # Standard move like 'e2e4'
        start_square = move_uci[:2]
        end_square = move_uci[2:]
        promotion = None
    elif len(move_uci) == 5 and move_uci[4] in 'qrbn':  # Promotion move like 'e7e8q'
        start_square = move_uci[:2]
        end_square = move_uci[2:4]
        promotion = move_uci[4]
    else:
        print(f"Invalid move format: {move_uci}")
        return

    if start_square in square_coords and end_square in square_coords:
        start_x, start_y = square_coords[start_square]
        end_x, end_y = square_coords[end_square]

        # Create a transparent overlay window
        root = tk.Tk()
        root.overrideredirect(True)  # Remove window decorations
        root.geometry(f"{square_size*8}x{square_size*8}+{board_left}+{board_top}")
        root.attributes("-topmost", True)  # Keep the window on top
        root.attributes("-transparentcolor", root["bg"])  # Make the window transparent

        canvas = tk.Canvas(root, width=square_size*8, height=square_size*8, highlightthickness=0)
        canvas.pack()


        # Highlight the start and end squares
        highlight_square(canvas, start_x - board_left, start_y - board_top, square_size)
        highlight_square(canvas, end_x - board_left, end_y - board_top, square_size)

        root.update()
        time.sleep(2)  # Small delay to allow for visual confirmation

        # Click the start square and then the end square
        print(f"Clicking at start position ({start_x + square_size // 2}, {start_y + square_size // 2})")
        pyautogui.click(start_x + square_size // 2, start_y + square_size // 2)
        time.sleep(0.5)  # Small delay to mimic human reaction time
        print(f"Clicking at end position ({end_x + square_size // 2}, {end_y + square_size // 2})")
        pyautogui.click(end_x + square_size // 2, end_y + square_size // 2)

        if promotion:
            # Handle promotion by clicking on the appropriate promotion choice
            print(f"Handling promotion to {promotion}")
            # Example for handling promotion - adjust according to your UI
            promotion_choices = {'q': (end_x + square_size // 2, end_y + square_size // 2 - 30),
                                  'r': (end_x + square_size // 2, end_y + square_size // 2 - 60),
                                  'b': (end_x + square_size // 2, end_y + square_size // 2 - 90),
                                  'n': (end_x + square_size // 2, end_y + square_size // 2 - 120)}
            if promotion in promotion_choices:
                pyautogui.click(*promotion_choices[promotion])
                time.sleep(0.5)

        root.destroy()  # Close the overlay window
    else:
        print(f"Invalid move or coordinates not found: {move_uci}")

