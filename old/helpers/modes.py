import imageio
from c_palette import load_custom_palette
from helpers import PALETTES, process_frame, setup_controls, get_control_values
import cv2
import time

def camera_mode():
    cap = cv2.VideoCapture(0)

    prev_time = time.time()
    fps = 0
    frame_count = 0
    recording_gif = False
    gif_frames, gif_start_time = [], 0

    setup_controls()

    while True:
        ret, frame = cap.read()
        if not ret: break

        pixel_size, levels, brightness, contrast, palette_id = get_control_values()
        processed = process_frame(frame, pixel_size, levels, brightness, contrast, palette_id)

        # FPS counter
        frame_count += 1
        if frame_count >= 10:
            curr_time = time.time()
            fps = 10 / (curr_time - prev_time)
            prev_time, frame_count = curr_time, 0

        cv2.putText(processed, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        # GIF recording
        if recording_gif:
            gif_frames.append(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            if time.time() - gif_start_time >= 3:
                imageio.mimsave(f"gifs/clip_{gif_counter:03d}.gif", gif_frames, fps=int(fps if fps > 0 else 10), loop=0)
                print(f"Saved gifs/clip_{gif_counter:03d}.gif")
                gif_counter += 1
                recording_gif = False
                gif_frames = []

        cv2.imshow("8-bit Camera Feed", processed)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        elif key == ord('p'):
            cv2.imwrite(f"pngs/snapshot_{snapshot_counter:03d}.png", processed)
            print(f"Saved pngs/snapshot_{snapshot_counter:03d}.png")
            snapshot_counter += 1
        elif key == ord('g') and not recording_gif:
            print("Recording GIF...")
            recording_gif, gif_start_time = True, time.time()
            gif_frames = []
        elif key == ord('r'):
            custom = load_custom_palette("custom/palette.png")
            if custom is not None: PALETTES[4] = ("Custom", custom)

    cap.release()
    cv2.destroyAllWindows()

def image_mode(path="test.png"):
    img = cv2.imread(path)
    if img is None:
        print(f"Could not load {path}")
        return

    setup_controls()

    while True:
        pixel_size, levels, brightness, contrast, palette_id = get_control_values()
        processed = process_frame(img.copy(), pixel_size, levels, brightness, contrast, palette_id)

        cv2.imshow("8-bit Image", processed)
        key = cv2.waitKey(50) & 0xFF
        if key == ord('q'): break
        elif key == ord('p'):
            cv2.imwrite(f"pngs/image_snapshot.png", processed)
            print("Saved pngs/image_snapshot.png")
        elif key == ord('r'):
            custom = load_custom_palette("custom/palette.png")
            if custom is not None: PALETTES[4] = ("Custom", custom)

    cv2.destroyAllWindows()