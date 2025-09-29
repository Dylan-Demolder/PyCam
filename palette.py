import cv2
import numpy as np

# Global state
current_color = (255, 255, 255)
palette = []

def nothing(x): pass

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

    # Create control window with 3 sliders (B, G, R)
    cv2.namedWindow("Controls")
    cv2.createTrackbar("R", "Controls", 255, 255, nothing)
    cv2.createTrackbar("G", "Controls", 255, 255, nothing)
    cv2.createTrackbar("B", "Controls", 255, 255, nothing)

    print("🎨 Controls:")
    print("  SPACE = Add current color to palette")
    print("  S     = Save palette to custom/palette.png")
    print("  C     = Clear palette")
    print("  Q     = Quit")

    while True:
        # Read trackbar values
        r = cv2.getTrackbarPos("R", "Controls")
        g = cv2.getTrackbarPos("G", "Controls")
        b = cv2.getTrackbarPos("B", "Controls")
        current_color = (b, g, r)

        # Show current color
        preview = np.zeros((100, 300, 3), dtype=np.uint8)
        preview[:] = current_color
        cv2.putText(preview, f"Current: B={b} G={g} R={r}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        cv2.imshow("Current Color", preview)

        # Show palette
        palette_img = draw_palette(palette, swatch_size=50, cols=8)
        cv2.imshow("Palette", palette_img)

        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
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
