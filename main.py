import cv2
import numpy as np
from helpers.camera_mode import camera_mode
from helpers.image_mode import image_mode
from helpers.io_helpers import load_custom_palette
from helpers.palettes import PALETTES
from helpers.controls import Button
from tkinter import Tk, filedialog
from helpers.palette_loader import load_all_palettes

# Dynamically load palettes from folder
PALETTES = load_all_palettes("palettes")


def select_image_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"), ("All Files", "*.*")]
    )
    root.destroy()
    return file_path

def main_menu():
    # Define button actions
    def start_camera():
        cv2.destroyAllWindows()
        camera_mode()

    def start_image():
        cv2.destroyAllWindows()
        path = select_image_file()
        if path:
            image_mode(path)

    def quit_app():
        print("Quit RetroCam")
        cv2.destroyAllWindows()
        exit()

    # Create buttons directly
    buttons = [
        Button("Camera Mode", (100, 120), size=(200, 50), action=start_camera),
        Button("Image Mode", (100, 190), size=(200, 50), action=start_image),
        Button("Quit", (100, 260), size=(200, 50), action=quit_app),
    ]

    cv2.namedWindow("Main Menu")
    cv2.setMouseCallback("Main Menu", lambda e, x, y, f, p: [b.handle_event(e, x, y, f, p) for b in buttons])

    while True:
        panel = np.zeros((400, 400, 3), dtype=np.uint8)
        cv2.putText(panel, "Retro Camera", (80, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        for b in buttons:
            b.draw(panel)

        cv2.imshow("Main Menu", panel)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            quit_app()

if __name__ == "__main__":
    custom = load_custom_palette("custom/palette.png")
    if custom is not None:
        PALETTES[4] = ("Custom", custom)
    main_menu()
