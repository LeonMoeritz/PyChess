import os
import pyautogui
import tkinter as tk
from PIL import Image
import time

def draw_border(x, y, width, height):
    # Create a transparent window to draw the border
    root = tk.Tk()
    root.attributes('-topmost', True)  # Keep the window on top
    root.attributes('-fullscreen', True)  # Fullscreen mode
    root.attributes('-transparentcolor', 'white')  # Make the background transparent
    root.configure(bg='white')

    canvas = tk.Canvas(root, bg='white', width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
    canvas.create_rectangle(x-5, y-5, x+5 + width, y+5 + height, outline='red', width=10)
    canvas.place(x=0, y=0)
    root.update()
    time.sleep(0.3)

    # Take the actual screenshot
    board_image = pyautogui.screenshot(region=(x, y, width, height))
    output_file_original = os.path.join('Screenshots', 'board.png')
    board_image.save(output_file_original)

    # Resize the screenshot
    with Image.open(output_file_original) as img:
        resized_img = img.resize((230, 230), Image.LANCZOS)
        output_file_resized = os.path.join('Screenshots', 'board_resized.png')
        resized_img.save(output_file_resized)

    # Close the tkinter window
    root.destroy()

def take_board_screenshot(x, y, width, height):
    draw_border(x, y, width, height)


