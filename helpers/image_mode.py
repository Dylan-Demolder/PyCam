import cv2
from helpers.effects import process_frame
from helpers.controls import ControlPanel
from helpers.io_helpers import load_custom_palette
from helpers.palettes import PALETTES

def image_mode(path="test.png"):
    img = cv2.imread(path)
    if img is None:
        print(f"Could not load {path}")
        return

    img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_AREA)
    print(f"Loaded {path}, resized to 512x512")

    controls = ControlPanel(PALETTES)

    while True:
        controls.show()
        pixel_size, levels, brightness, contrast, palette_id = controls.get_values()

        processed = process_frame(img.copy(), pixel_size, levels, brightness, contrast, palette_id, PALETTES)

        cv2.imshow("8-bit Image", processed)
        key = cv2.waitKey(50) & 0xFF
        if key == ord('q'): break
        elif key == ord('p'):
            cv2.imwrite("pngs/image_snapshot.png", processed)
            print("Saved pngs/image_snapshot.png")
        elif key == ord('r'):
            custom = load_custom_palette("custom/palette.png")
            if custom is not None: PALETTES[4] = ("Custom", custom)

    cv2.destroyAllWindows()
