import cv2, time
from helpers.effects import process_frame
from helpers.controls import ControlPanel
from helpers.io_helpers import save_snapshot, save_gif, load_custom_palette
from helpers.palettes import PALETTES

def camera_mode():
    cap = cv2.VideoCapture(0)
    controls = ControlPanel(PALETTES)

    prev_time = time.time()
    fps, frame_count = 0, 0
    recording_gif = False
    gif_frames, gif_start_time = [], 0

    while True:
        ret, frame = cap.read()
        if not ret: break

        controls.show()
        pixel_size, levels, brightness, contrast, palette_id = controls.get_values()

        processed = process_frame(frame, pixel_size, levels, brightness, contrast, palette_id, PALETTES)

        frame_count += 1
        if frame_count >= 10:
            curr_time = time.time()
            fps = 10 / (curr_time - prev_time)
            prev_time, frame_count = curr_time, 0

        cv2.putText(processed, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        if recording_gif:
            gif_frames.append(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            if time.time() - gif_start_time >= 3:
                save_gif(gif_frames, fps=int(fps if fps > 0 else 10))
                recording_gif, gif_frames = False, []

        cv2.imshow("8-bit Camera Feed", processed)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        elif key == ord('p'): save_snapshot(processed)
        elif key == ord('g') and not recording_gif:
            print("Recording GIF...")
            recording_gif, gif_start_time, gif_frames = True, time.time(), []
        elif key == ord('r'):
            custom = load_custom_palette("custom/palette.png")
            if custom is not None: PALETTES[4] = ("Custom", custom)

    cap.release()
    cv2.destroyAllWindows()
