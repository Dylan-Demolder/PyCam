import cv2
import numpy as np
import imageio

# --- Base Palettes (BGR for OpenCV) ---
PALETTES = {
    0: ("Quantized", None),
    1: ("Game Boy", np.array([[15, 56, 15], [48, 98, 48], [139, 172, 15], [155, 188, 15]], dtype=np.uint8)),
    2: ("CGA", np.array([[0, 0, 0], [85, 255, 255], [255, 85, 255], [255, 255, 255]], dtype=np.uint8)),
    3: ("NES", np.array([[84, 84, 84], [0, 30, 116], [8, 16, 144], [48, 0, 136],
                         [68, 0, 100], [92, 0, 48], [84, 4, 0], [60, 24, 0],
                         [32, 42, 0], [8, 58, 0], [0, 64, 0], [0, 60, 0],
                         [0, 50, 60], [0, 0, 0]], dtype=np.uint8)),
    4: ("Custom", None),  # will be loaded dynamically
}

# --- Image Effects ---
def pixelate(frame, pixel_size=10):
    h, w = frame.shape[:2]
    temp = cv2.resize(frame, (max(1, w // pixel_size), max(1, h // pixel_size)), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

def quantize_colors_fast(frame, levels=6):
    div = max(1, 256 // levels)
    quantized = (frame // div) * div + div // 2
    return np.clip(quantized, 0, 255).astype(np.uint8)

def apply_palette(frame, palette):
    h, w, _ = frame.shape
    reshaped = frame.reshape((-1, 3)).astype(np.int16)
    distances = np.sqrt(((reshaped[:, None, :] - palette[None, :, :]) ** 2).sum(axis=2))
    nearest = distances.argmin(axis=1)
    return palette[nearest].reshape((h, w, 3)).astype(np.uint8)

def adjust_brightness_contrast(frame, brightness=0, contrast=1.0):
    return cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

def process_frame(frame, pixel_size, levels, brightness, contrast, palette_id):
    frame = pixelate(frame, pixel_size)

    if palette_id in PALETTES and PALETTES[palette_id][1] is not None:
        frame = apply_palette(frame, PALETTES[palette_id][1])
    else:
        frame = quantize_colors_fast(frame, levels)

    return adjust_brightness_contrast(frame, brightness - 50, contrast / 50.0)

snapshot_counter = 1
gif_counter = 1
# --- Save Helpers ---
def save_snapshot(frame):
    global snapshot_counter
    filename = f"pngs/snapshot_{snapshot_counter:03d}.png"
    cv2.imwrite(filename, frame)
    print(f"Saved {filename}")
    snapshot_counter += 1

def save_gif(frames, fps=10):
    global gif_counter
    filename = f"gifs/clip_{gif_counter:03d}.gif"
    imageio.mimsave(filename, frames, fps=fps, loop=0)  # loop=0 = infinite
    print(f"Saved {filename} ({len(frames)} frames at {fps} FPS, loops forever)")
    gif_counter += 1

def nothing(x): pass