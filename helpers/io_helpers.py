import cv2
import os
import imageio
import numpy as np

os.makedirs("pngs", exist_ok=True)
os.makedirs("gifs", exist_ok=True)

snapshot_counter = 1
gif_counter = 1

def save_snapshot(frame):
    global snapshot_counter
    filename = f"pngs/snapshot_{snapshot_counter:03d}.png"
    cv2.imwrite(filename, frame)
    print(f"📸 Saved {filename}")
    snapshot_counter += 1

def save_gif(frames, fps=10):
    global gif_counter
    filename = f"gifs/clip_{gif_counter:03d}.gif"
    imageio.mimsave(filename, frames, fps=fps, loop=0)
    print(f"🎞️ Saved {filename} ({len(frames)} frames)")
    gif_counter += 1

def load_custom_palette(path="custom/palette.png", max_colors=32):
    img = cv2.imread(path)
    if img is None:
        print(f"⚠️ No custom palette found at {path}")
        return None
    data = img.reshape((-1, 3))
    unique_colors = np.unique(data, axis=0)
    if len(unique_colors) > max_colors:
        data = np.float32(data)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, _, centers = cv2.kmeans(data, max_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        unique_colors = np.uint8(centers)
    print(f"✅ Loaded custom palette with {len(unique_colors)} colors")
    return unique_colors
