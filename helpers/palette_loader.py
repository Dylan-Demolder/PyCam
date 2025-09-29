import os
import cv2
import numpy as np

def load_palette_from_image(path, max_colors=64):
    img = cv2.imread(path)
    if img is None:
        return None
    data = img.reshape((-1, 3))
    unique_colors = np.unique(data, axis=0)

    # If too many unique colors, cluster down
    if len(unique_colors) > max_colors:
        data = np.float32(data)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, _, centers = cv2.kmeans(data, max_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        unique_colors = np.uint8(centers)

    return unique_colors

def load_all_palettes(folder="./palettes"):
    palettes = {}
    if not os.path.exists(folder):
        os.makedirs(folder)
    for i, filename in enumerate(sorted(os.listdir(folder))):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            path = os.path.join(folder, filename)
            colors = load_palette_from_image(path)
            if colors is not None:
                name = os.path.splitext(filename)[0]
                palettes[i] = (name, colors)
    return palettes
