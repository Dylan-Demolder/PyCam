import cv2
import numpy as np
import os
from helpers.controls import Slider, ControlPanel

# Global state
current_color = (255, 255, 255)
palette = []

def draw_palette(palette, swatch_size=50, cols=8):
    """Render the palette as an image grid"""
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

    # Use the custom control panel for R, G, B sliders
    controls = ControlPanel({0: ("dummy", None)})
    controls.sliders = [
        Slider("Red", 0, 255, 255, (50, 80)),
        Slider("Green", 0, 255, 255, (50, 160)),
        Slider("Blue", 0, 255, 255, (50, 240)),
    ]

    print("🎨 Palette Maker Controls:")
    print("  SPACE = Add current color to palette")
    print("  S     = Save palette to custom/palette.png")
    print("  C     = Clear palette")
    print("  Q     = Quit")

    while True:
        controls.show()
        r, g, b = controls.get_values()
        current_color = (b, g, r)

        # Show current color
        preview = np.zeros((300, 300, 3), dtype=np.uint8)
        preview[:] = current_color
        #cv2.putText(preview, f"Current: R={r} G={g} B={b}", (10, 70),
        #            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
        cv2.imshow("Current Color", preview)

        # Show palette
        palette_img = draw_palette(palette, swatch_size=50, cols=8)
        cv2.imshow("Palette", palette_img)

        # Keyboard controls
        key = cv2.waitKey(30) & 0xFF
        if key == ord(' '):  # Add color
            palette.append(current_color)
            print(f"Added color {current_color}")
        elif key == ord('s'):  # Save
            if palette:
                cv2.imwrite("custom/palette.png", draw_palette(palette, 50, 8))
                print(f"Saved {len(palette)} colors to custom/palette.png")
            else:
                print("No colors in palette to save!")
        elif key == ord('c'):  # Clear
            palette = []
            print("Cleared palette")
        elif key == ord('q'):  # Quit
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
