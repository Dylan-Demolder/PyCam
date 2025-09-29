import cv2
import numpy as np

# --- Custom Palette Loader ---
def load_custom_palette(path="custom/palette.png", max_colors=32):
    img = cv2.imread(path)
    if img is None:
        print(f"No custom palette found at {path}")
        return None

    data = img.reshape((-1, 3))
    unique_colors = np.unique(data, axis=0)

    if len(unique_colors) > max_colors:
        data = np.float32(data)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, _, centers = cv2.kmeans(data, max_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        unique_colors = np.uint8(centers)

    print(f"Loaded custom palette with {len(unique_colors)} colors from {path}")
    return unique_colors