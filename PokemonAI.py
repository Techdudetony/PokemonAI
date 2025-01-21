import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import time
import logging

# Configure logging
logging.basicConfig(filename='nuzlocke.log', level=logging.INFO)

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
    Simulates a button press.
    :param button: The key to press (e.g., 'z', 'x', 'up', 'down').
    """
    pyautogui.keyDown(button)
    time.sleep(0.1)  # Short delay to mimic natural key press
    pyautogui.keyUp(button)

def move(direction, steps=1):
    """
    Simulates movement in a given direction.
    :param direction: 'up', 'down', 'left', or 'right'.
    :param steps: Number of steps to move.
    """
    for _ in range(steps):
        press_button(direction)
        time.sleep(0.2)  # Delay between steps for smooth navigation

def find_template(screen, template_path):
    """
    Matches a template image within the given screen.
    :param screen: The screen (NumPy array) to search within.
    :param template_path: The path to the template image file.
    :return: The location of the match or None if not found.
    """
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.8:  # Confidence threshold
        return max_loc
    return None

def navigate_room():
    """
    Navigates the player's room from the starting position to the stairs.
    Detailed Steps:
    1. Turn downward to face the correct direction.
    2. Move downward to the bottom of the room.
    3. Move leftward to align with the stairs.
    4. Move downward to reach the stairs.
    """
    print("Starting navigation from the player's room.")  # Debugging output
    logging.info("Starting navigation from the player's room.")

    # Step 1: Turn downward (optional based on starting orientation)
    print("Turning downward...")
    press_button("down")
    time.sleep(0.5)  # Small delay to simulate real-time gameplay

    # Step 2: Move downward to the bottom of the room
    print("Moving downward...")
    logging.info("Moving downward to the bottom of the room.")
    for _ in range(6):  # Adjust the range based on the number of steps needed
        press_button("down")
        time.sleep(0.2)

    # Step 3: Move left to align with the stairs
    print("Moving left...")
    logging.info("Moving left to align with the stairs.")
    for _ in range(4):  # Adjust the range based on the number of steps needed
        press_button("left")
        time.sleep(0.2)

    # Step 4: Move downward to reach the stairs
    print("Moving downward to stairs...")
    logging.info("Moving downward to reach the stairs.")
    for _ in range(3):  # Adjust the range based on the number of steps needed
        press_button("down")
        time.sleep(0.2)

    print("Navigation complete.")
    logging.info("Navigation complete. Player should now be at the stairs.")

def main():
    """
    Main function to initiate the AI navigation process.
    1. Waits for the game to start.
    2. Captures the emulator screen (if needed).
    3. Calls the room navigation function.
    """
    # Define the emulator screen region (update with your emulator's position and size)
    screen_region = (0, 0, 1000, 1000)  # Update based on your emulator window

    # Wait a few seconds to ensure the game starts
    logging.info("Waiting for the game to start...")
    time.sleep(5)

    # Navigate the player's room
    print("Starting navigation...")
    navigate_room()

    # Confirm navigation completion by taking a screenshot
    print("Taking a screenshot of the emulator window...")
    screen = capture_screen(screen_region)
    cv2.imwrite("screenshot.png", screen)
    print("Screenshot saved as 'screenshot.png'.")

if __name__ == "__main__":
    main()
