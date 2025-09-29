import cv2
import numpy as np
from helpers.camera_mode import camera_mode
from helpers.image_mode import image_mode
from helpers.io_helpers import load_custom_palette
from helpers.palettes import PALETTES

def main_menu():
    # Create a blank black canvas
    menu = np.zeros((300, 500, 3), dtype=np.uint8)

    # Draw menu text
    cv2.putText(menu, "Retro Camera", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.putText(menu, "Press C = Camera Mode", (80, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(menu, "Press I = Image Mode", (80, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(menu, "Press Q = Quit", (80, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    while True:
        cv2.imshow("Mode Select", menu)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('c'):
            cv2.destroyWindow("Mode Select")
            camera_mode()
            break
        elif key == ord('i'):
            cv2.destroyWindow("Mode Select")
            path = input("Enter image path: ")
            image_mode(path)
            break
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    custom = load_custom_palette("custom/palette.png")
    if custom is not None:
        PALETTES[4] = ("Custom", custom)
    main_menu()
