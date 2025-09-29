import cv2
import numpy as np

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

def process_frame(frame, pixel_size, levels, brightness, contrast, palette_id, palettes):
    from helpers.palettes import PALETTES
    frame = pixelate(frame, pixel_size)
    if palette_id in palettes and palettes[palette_id][1] is not None:
        frame = apply_palette(frame, palettes[palette_id][1])
    else:
        frame = quantize_colors_fast(frame, levels)
    return adjust_brightness_contrast(frame, brightness - 50, contrast / 50.0)
