import os
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from tkinter import ttk
import json
import screenshot
import read
import calc
import move
import time


board_image_path = 'Screenshots/board.png'
templates_folder = 'Templates'




def load_settings():
    with open('Settings/settings.json', 'r') as file:
        settings = json.load(file)
    return settings

def update_console_label_sequence(updates_with_delays):
    def update_text(index):
        if index < len(updates_with_delays):
            text, delay = updates_with_delays[index]
            label_console.config(text=text)
            root.after(delay, lambda: update_text(index + 1))

    # Start the update process
    update_text(0)

def start(radio_var, radio_var1, settings):

    global x, y, w, h, selected_color, game_running

    selected_mode = radio_var.get()
    selected_color = radio_var1.get()

    
    
    if selected_mode in settings:
        x = int(settings[selected_mode]['x'])
        y = int(settings[selected_mode]['y'])
        w = int(settings[selected_mode]['w'])
        h = int(settings[selected_mode]['h'])

        updates_with_delays = [
            (f"Mode selected: {selected_mode}", 2000),
            (f"PyChess playing as {selected_color}", 2000),
            (f"taking screenshot", 2000),
            (f"reading position", 2000)
        ]

        update_console_label_sequence(updates_with_delays)

        root.after(6000, lambda: screenshot.take_board_screenshot(x, y, w, h))
        root.after(6500, lambda: update_image())
        root.after(7000, lambda: run_game())

        button_start.config(text="Stop", command=stop)
        game_running = True
        

    else:
        print(f"Mode {selected_mode} not found in settings")

def update_image():
    img_board = ImageTk.PhotoImage(Image.open('Screenshots/board_resized.png'))
    label_img.config(image=img_board)
    label_img.image = img_board

def update_console(text):
    label_console.config(text=text)

def run_game():
    global game_running

    update_console("Starting game loop...")
    while game_running:
        # Take screenshot
        update_console("Taking screenshot...")
        screenshot.take_board_screenshot(x, y, w, h)
        update_image()
        
        # Read position
        position = read.read_chess_position(board_image_path, templates_folder)
        
        # Convert position to FEN
        fen = read.generate_fen(position, selected_color)
        
        # Calculate best move
        best_move, new_fen = calc.get_best_move(fen, selected_color)
        
        if best_move is None:
            update_console("Error calculating the best move.")
            break
        
        # Perform move
        update_console(f"Performing move: {best_move}...")
        time.sleep(0.2)
        move.perform_move(best_move, x, y, w // 8)
        
        while True:
            update_console("Taking screenshot...")
            screenshot.take_board_screenshot(x, y, w, h)
            update_image()
            position = read.read_chess_position(board_image_path, templates_folder)
            fen = read.generate_fen(position, selected_color)
            print(fen.split()[0])
            print(new_fen.split()[0])
            if new_fen.split()[0] != fen.split()[0]:
                update_console("waiting for opponent")
                print("OPPONENT MOVED")
                break

            time.sleep(0.1)
            root.update()

    update_console("Game stopped.")



def stop():
    global game_running
    game_running = False
    button_start.config(text="Start", command=lambda: start(radio_var, radio_var1, settings))

def run_gui():

    
    global settings, label_img, label_console, root, game_running, button_start, radio_var, radio_var1

    settings = load_settings()

    root = tk.Tk()
    root.title("PyChess")
    root.configure(bg="black")

    img_logo = tk.PhotoImage(file="Logo/logo.png")

    root.geometry("250x420")
    root.resizable(False, False)

    font_roboto = "Roboto"

    #LABELS
    label_top = tk.Label(root, text="Welcome to PyChess", bg = "black", fg= "#ffffda", font = (font_roboto, 12, "bold"))
    label_top.place(x= 10, y= 10, width= 230, height = 20)

    label_img = tk.Label(root, image=img_logo)
    label_img.place(x= 10, y= 110, width= 230, height= 230)

    label_console = tk.Label(root, text="press start", bg = "black", fg= "#ffffda", font = (font_roboto, 10, "bold"))
    label_console.place(x= 10, y= 350, width= 230, height = 20)

    # RADIO BUTTONS
    style = ttk.Style()
    style.configure('TRadiobutton',
                    background='black',
                    foreground='white',
                    font=(font_roboto, 10),
                    focuscolor='none')
    
    radio_var = tk.StringVar(value="online (normal)")
    radio_var1 = tk.StringVar(value="white")

    radio_online_normal = ttk.Radiobutton(root, text="online (normal)", variable=radio_var, value="online (normal)", style='TRadiobutton')
    radio_online_normal.place(x=30, y=40)

    radio_online_focus = ttk.Radiobutton(root, text="online (focus)", variable=radio_var, value="online (focus)", style='TRadiobutton')
    radio_online_focus.place(x=30, y=60)

    radio_puzzles = ttk.Radiobutton(root, text="puzzles", variable=radio_var, value="puzzles", style='TRadiobutton')
    radio_puzzles.place(x=30, y=80)

    radio_white = ttk.Radiobutton(root, text="white", variable=radio_var1, value="white", style='TRadiobutton')
    radio_white.place(x=160, y=40)

    radio_black = ttk.Radiobutton(root, text="black", variable=radio_var1, value="black", style='TRadiobutton')
    radio_black.place(x=160, y=60)
    

    #BUTTON
    button_start = tk.Button(
        root, 
        text="Start", 
        font=(font_roboto, 12, "bold"), 
        bg="#00bf7a", 
        fg="black", 
        borderwidth=2, 
        relief="solid", 
        activebackground="#0bbe7f", 
        activeforeground="black",
        command=lambda: start(radio_var, radio_var1, settings) 
    )
    button_start.place(x=10, y=380, width= 230, height=30)

    root.mainloop()

run_gui()