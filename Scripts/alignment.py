import pyautogui

def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Please enter a valid integer.")

def measure():

    x_found = False
    y_found = False
    w_found = False
    h_found = False

    # Get the X coordinate
    while not x_found:
        x = get_integer_input("Enter the X coordinate: ")
        board_xy = pyautogui.screenshot(region=(x, 0, 200, 200))
        board_xy.save('xy_alignment.png')
        if input("Is this X coordinate correct? (Type 'OK' to confirm or press Enter to retry): ") == "OK":
            x_found = True         

    # Get the Y coordinate
    while not y_found:
        y = get_integer_input("Enter the Y coordinate: ")
        board_xy = pyautogui.screenshot(region=(x, y, 200, 200))
        board_xy.save('xy_alignment.png')
        if input("Is this Y coordinate correct? (Type 'OK' to confirm or press Enter to retry): ") == "OK":
            y_found = True

    # Get the Width (W)
    while not w_found:
        w = get_integer_input("Enter the width: ")
        board_xy = pyautogui.screenshot(region=(x, y, w, 200))
        board_xy.save('xy_alignment.png')
        if input("Is this width correct? (Type 'OK' to confirm or press Enter to retry): ") == "OK":
            w_found = True

    # Get the Height (H)
    while not h_found:
        h = get_integer_input("Enter the height: ")
        board_xy = pyautogui.screenshot(region=(x, y, w, h))
        board_xy.save('xy_alignment.png')
        if input("Is this height correct? (Type 'OK' to confirm or press Enter to retry): ") == "OK":
            h_found = True

    # Output the final measured values
    print(f"You measured: X={x}, Y={y}, Width={w}, Height={h}")

measure()