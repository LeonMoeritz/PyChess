import cv2
import numpy as np
import pyautogui
import os

def extract_squares_from_board(board_image_path, num_squares_per_side=8):
    board_image = cv2.imread(board_image_path, cv2.IMREAD_GRAYSCALE)
    h, w = board_image.shape
    square_size = w // num_squares_per_side

    squares = {}
    for row in range(num_squares_per_side):
        for col in range(num_squares_per_side):
            top_left_x = col * square_size
            top_left_y = row * square_size
            square_image = board_image[top_left_y:top_left_y + square_size, top_left_x:top_left_x + square_size]
            squares[f"{chr(ord('a') + col)}{8 - row}"] = square_image
    return squares

def load_templates_from_folder(folder):
    templates = {}
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            templates[filename.split('.')[0]] = img
    return templates

def compare_image_to_templates(image, templates):
    best_match = None
    best_match_score = float('inf')
    
    for template_name, template_image in templates.items():
        res = cv2.matchTemplate(image, template_image, cv2.TM_SQDIFF_NORMED)
        min_val, _, _, _ = cv2.minMaxLoc(res)
        if min_val < best_match_score:
            best_match_score = min_val
            best_match = template_name
    
    return best_match

def read_chess_position(board_image_path, templates_folder):
    squares = extract_squares_from_board(board_image_path)
    templates = load_templates_from_folder(templates_folder)

    position = {}
    for square_name, square_image in squares.items():
        best_match = compare_image_to_templates(square_image, templates)
        position[square_name] = best_match
    
    return position

def simplify_piece_name(piece):
    if piece:
        if 'pawn' in piece:
            return 'P'
        elif 'rook' in piece:
            return 'R'
        elif 'knight' in piece:
            return 'N'
        elif 'bishop' in piece:
            return 'B'
        elif 'queen' in piece:
            return 'Q'
        elif 'king' in piece:
            return 'K'
    return None

def generate_fen(position, turn):
    board = [["" for _ in range(8)] for _ in range(8)]
    columns = 'abcdefgh'
    rows = '87654321'
    
    for square, piece in position.items():
        col = columns.index(square[0])
        row = rows.index(square[1])
        piece_letter = simplify_piece_name(piece)
        if piece_letter:
            if 'white' in piece:
                board[row][col] = piece_letter.upper()
            else:
                board[row][col] = piece_letter.lower()

    fen_rows = []
    for row in board:
        fen_row = ""
        empty_count = 0
        for square in row:
            if square == "":
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += square
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    fen_position = "/".join(fen_rows)
    fen_turn = 'w' if turn == 'white' else 'b'
    
    return f"{fen_position} {fen_turn} - - 0 1"

