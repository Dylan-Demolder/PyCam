import cv2
import numpy as np
import os
from helpers.controls import ControlPanel

current_color = (255, 255, 255)
palette = []

def draw_palette(palette, swatch_size=50, cols=8):
    if not palette:
        return np.zeros((swatch_size, swatch_size, 3), dtype=np.uint8)
    rows = (len(palette) + cols - 1) // cols
    img = np.zeros((rows * swatch_size, cols * swatch_size, 3), dtype=np.uint8)
    for i, color in enumerate(palette):
        r = i // cols
        c = i % cols
        y1, y2 = r * swatch_size, (r + 1) * swatch_size
        x1, x2 = c * swatch_size, (c + 1) * swatch_size
        img[y1:y2, x1:x2] = color
    return img

def main():
    global current_color, palette

    os.makedirs("custom", exist_ok=True)

    controls = ControlPanel({0: ("dummy", None)})
    controls.add_slider("Red", 0, 255, 255, (50, 80))
    controls.add_slider("Green", 0, 255, 255, (50, 160))
    controls.add_slider("Blue", 0, 255, 255, (50, 240))
    controls.add_textbox("Palette Name", (50, 320), size=(250, 40))

    def add_color():
        global palette, current_color
        palette.append(current_color)
        print(f"Added color {current_color}")

    def save_palette():
        if not palette:
            print("No colors to save!")
            return
        name = controls.get_textbox_value("Palette Name").strip()
        if not name:
            print("No name entered, save cancelled.")
            return
        filename = os.path.join("palettes", f"{name}.png")
        cv2.imwrite(filename, draw_palette(palette, 50, 8))
        print(f"Saved {len(palette)} colors to {filename}")

    def clear_palette():
        global palette
        palette = []
        print("Cleared palette")

    def quit_app():
        print("Quit Palette Maker")
        cv2.destroyAllWindows()
        exit()

    # Add buttons
    controls.add_button("Add Color", (350, 80), action=add_color)
    controls.add_button("Save Palette", (350, 140), action=save_palette)
    controls.add_button("Clear Palette", (350, 200), action=clear_palette)
    controls.add_button("Quit", (350, 260), action=quit_app)

    while True:
        controls.show()
        r, g, b = controls.get_slider_values()
        current_color = (b, g, r)

        preview = np.zeros((100, 300, 3), dtype=np.uint8)
        preview[:] = current_color
        cv2.putText(preview, f"Current: R={r} G={g} B={b}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.imshow("Current Color", preview)

        palette_img = draw_palette(palette, swatch_size=50, cols=8)
        cv2.imshow("Palette", palette_img)

        key = cv2.waitKey(30) & 0xFF
        if key != 255:
            controls.handle_key(key)

            # Only quit if no text box is active
            if key == ord('q') and not any(t.active for t in controls.text_boxes):
                break


    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
