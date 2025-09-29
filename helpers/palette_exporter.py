import cv2
import numpy as np
import os
from helpers.palettes import PALETTES

def make_palette(colors, filename="palette.png", swatch_size=50, cols=8):
    """
    Save a list of colors as a PNG grid.
    colors: list of [B, G, R]
    filename: output file path
    swatch_size: size of each swatch in pixels
    cols: number of swatches per row
    """
    if colors is None or len(colors) == 0:
        return

    rows = (len(colors) + cols - 1) // cols
    img = np.zeros((rows * swatch_size, cols * swatch_size, 3), dtype=np.uint8)

    for i, color in enumerate(colors):
        r = i // cols
        c = i % cols
        y1, y2 = r * swatch_size, (r + 1) * swatch_size
        x1, x2 = c * swatch_size, (c + 1) * swatch_size
        img[y1:y2, x1:x2] = color

    cv2.imwrite(filename, img)
    print(f"🎨 Saved {filename} with {len(colors)} colors")

def export_all_palettes(out_dir="palettes"):
    os.makedirs(out_dir, exist_ok=True)
    for pid, (name, colors) in PALETTES.items():
        if colors is not None:
            filename = os.path.join(out_dir, f"{name.replace(' ', '_').lower()}.png")
            make_palette(colors, filename)

if __name__ == "__main__":
    export_all_palettes()
