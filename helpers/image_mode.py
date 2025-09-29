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

    # Add sliders
    controls.add_slider("Pixel Size", 1, 50, 12, (50, 80))
    controls.add_slider("Color Levels", 1, 16, 6, (50, 160))
    controls.add_slider("Brightness", 0, 100, 50, (50, 240))
    controls.add_slider("Contrast", 0, 100, 50, (50, 320))
    controls.add_slider("Palette", 0, len(PALETTES) - 1, 0, (50, 400))

    # Button actions
    def save_image():
        cv2.imwrite("pngs/image_snapshot.png", processed)
        print("Saved pngs/image_snapshot.png")

    def reload_palette():
        custom = load_custom_palette("custom/palette.png")
        if custom is not None:
            PALETTES[4] = ("Custom", custom)
            print("Reloaded custom palette")

    def quit_app():
        print("Quit Image Mode")
        cv2.destroyAllWindows()
        exit()

    # Add buttons
    controls.add_button("Save Image", (350, 80), action=save_image)
    controls.add_button("Reload Palette", (350, 140), action=reload_palette)
    controls.add_button("Quit", (350, 200), action=quit_app)

    while True:
        controls.show()
        pixel_size, levels, brightness, contrast, palette_id = controls.get_slider_values()

        processed = process_frame(img.copy(), pixel_size, levels, brightness, contrast, palette_id, PALETTES)
        cv2.imshow("8-bit Image", processed)

        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
