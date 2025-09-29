import cv2
import numpy as np
import time
import os
from helpers.helpers import (PALETTES, process_frame, save_snapshot, save_gif, nothing)
from helpers.c_palette import load_custom_palette

# Ensure folders exist
os.makedirs("pngs", exist_ok=True)
os.makedirs("gifs", exist_ok=True)

def main():
    global snapshot_counter, gif_counter
    cap = cv2.VideoCapture(0)

    # Try to load custom palette
    custom_palette = load_custom_palette("custom/palette.png", max_colors=32)
    if custom_palette is not None:
        PALETTES[4] = ("Custom", custom_palette)

    prev_time = time.time()
    fps = 0
    frame_count = 0
    recording_gif = False
    gif_frames = []
    gif_start_time = 0
    gif_duration = 3  # seconds

    # --- Controls window ---
    cv2.namedWindow("Controls")
    cv2.createTrackbar("Pixel Size", "Controls", 12, 50, nothing)
    cv2.createTrackbar("Color Levels", "Controls", 6, 16, nothing)
    cv2.createTrackbar("Brightness", "Controls", 50, 100, nothing)
    cv2.createTrackbar("Contrast", "Controls", 50, 100, nothing)
    cv2.createTrackbar("Palette", "Controls", 0, len(PALETTES)-1, nothing)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # --- Get UI values ---
        pixel_size = max(1, cv2.getTrackbarPos("Pixel Size", "Controls"))
        levels = max(1, cv2.getTrackbarPos("Color Levels", "Controls"))
        brightness = cv2.getTrackbarPos("Brightness", "Controls")
        contrast = cv2.getTrackbarPos("Contrast", "Controls")
        palette_id = cv2.getTrackbarPos("Palette", "Controls")

        # --- Process frame ---
        processed = process_frame(frame, pixel_size, levels, brightness, contrast, palette_id)

        # --- FPS Counter ---
        frame_count += 1
        if frame_count >= 10:
            curr_time = time.time()
            fps = 10 / (curr_time - prev_time)
            prev_time = curr_time
            frame_count = 0

        palette_name = PALETTES[palette_id][0]
        cv2.putText(processed, f"FPS: {fps:.1f} | Palette: {palette_name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        # --- Handle GIF recording ---
        if recording_gif:
            gif_frames.append(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            if time.time() - gif_start_time >= gif_duration:
                save_gif(gif_frames, fps=int(fps if fps > 0 else 10))
                gif_frames = []
                recording_gif = False

        cv2.imshow("8-bit Camera Feed", processed)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            save_snapshot(processed)
        elif key == ord('g') and not recording_gif:
            print("Recording GIF for 3 seconds...")
            recording_gif = True
            gif_frames = []
            gif_start_time = time.time()
        elif key == ord('r'):  # reload custom palette
            custom_palette = load_custom_palette("custom/palette.png", max_colors=32)
            if custom_palette is not None:
                PALETTES[4] = ("Custom", custom_palette)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()