import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import time
import logging
from pynput.keyboard import Controller, Key

# Configure logging
logging.basicConfig(filename='nuzlocke.log', level=logging.INFO)

# Initialize the keyboard controller
keyboard_controller = Controller()

# Define the room grid based on the game's grid system
room_grid = [
    ["wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall"],
    ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
    ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
    ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
    ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
    ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
    ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
    ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
]

# Map key positions to coordinates based on the game's grid system
positions = {
    "player": (3, 3),  # Starting position of the player (row 3, column 3)
    "computer": (6, 1),  # Position of the computer (row 6, column 1)
    "stairs": (7, 9),  # Position of the stairs (row 7, column 9)
    "tv": (4, 5),  # TV's position (row 4, column 5)
    "bed": [(2, 3), (2, 4)],  # Bed occupies multiple tiles
}

def capture_screen(region):
    """
    Captures a specific region of the screen.
    :param region: A tuple (x, y, width, height) defining the screen region to capture.
    :return: The captured screen as a NumPy array.
    """
    screenshot = ImageGrab.grab(bbox=region)  # Capture the specified screen region
    screenshot = np.array(screenshot)  # Convert to a NumPy array
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)  # Convert to OpenCV format
    return screenshot

def press_button(button):
    """
    Simulates a button press using pynput.
    :param button: The key to press (e.g., 'z', 'x', 'up', 'down').
    """
    key_mapping = {
        "up": Key.up,
        "down": Key.down,
        "left": Key.left,
        "right": Key.right,
        "z": "z",
        "x": "x"
    }

    if button in key_mapping:
        key = key_mapping[button]
        keyboard_controller.press(key)
        time.sleep(0.2)  # Delay to mimic natural key press
        keyboard_controller.release(key)
        time.sleep(0.2)  # Delay after releasing the key

def move(direction, steps=1):
    """
    Simulates movement in a given direction.
    :param direction: 'up', 'down', 'left', or 'right'.
    :param steps: Number of steps to move.
    """
    for _ in range(steps):
        press_button(direction)
        time.sleep(0.3)  # Increased delay between steps for smooth navigation

def focus_emulator():
    """
    Focuses the emulator window programmatically.
    """
    print("Focusing on the emulator window...")
    # Replace with the coordinates of the emulator window
    emulator_x, emulator_y = 100, 100  # Update these values based on your setup
    keyboard_controller.press(Key.alt)
    time.sleep(0.1)
    keyboard_controller.release(Key.alt)
    time.sleep(0.5)  # Short delay to ensure the window is focused

def navigate_to_stairs():
    """
    Hardcoded navigation to stairs: 7 left, 7 up, 4 right.
    """
    print("Navigating to stairs...")
    logging.info("Navigating to stairs...")

    # Move 7 steps left
    move("right", steps=7)

    # Move 7 steps up
    move("up", steps=7)

    # Move 4 steps right
    move("left", steps=4)

    print("Reached stairs.")
    logging.info("Reached stairs.")

def main():
    """
    Main function to initiate the AI navigation process.
    1. Waits for the game to start.
    2. Captures the emulator screen (if needed).
    3. Calls the navigation function.
    """
    # Define the emulator screen region (update with your emulator's position and size)
    screen_region = (0, 0, 1220, 850)  # Updated based on your emulator window

    # Focus the emulator window
    focus_emulator()

    # Wait a few seconds to ensure the game starts
    logging.info("Waiting for the game to start...")
    time.sleep(5)

    # Navigate to the stairs
    print("Starting navigation to stairs...")
    navigate_to_stairs()

    # Confirm navigation completion by taking a screenshot
    print("Taking a screenshot of the emulator window...")
    screen = capture_screen(screen_region)
    cv2.imwrite("screenshot.png", screen)
    print("Screenshot saved as 'screenshot.png'.")

if __name__ == "__main__":
    main()
