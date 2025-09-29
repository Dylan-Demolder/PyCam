import cv2, time
from helpers.effects import process_frame
from helpers.controls import ControlPanel
from helpers.io_helpers import save_snapshot, save_gif, load_custom_palette
from helpers.palette_loader import load_all_palettes
PALETTES = load_all_palettes("palettes")

def camera_mode():
    cap = cv2.VideoCapture(0)
    controls = ControlPanel(PALETTES)

    # Add sliders
    controls.add_slider("Pixel Size", 1, 25, 4, (50, 80))
    controls.add_slider("Color Levels", 1, 16, 6, (50, 160))
    controls.add_slider("Brightness", 0, 100, 50, (50, 240))
    controls.add_slider("Contrast", 0, 100, 50, (50, 320))
    controls.add_slider("Palette", 0, len(PALETTES) - 1, 0, (50, 400))

    # GIF state
    recording_gif = False
    gif_frames, gif_start_time = [], 0
    prev_time, fps, frame_count = time.time(), 0, 0

    # Button actions
    def take_snapshot():
        save_snapshot(processed)

    def start_gif():
        nonlocal recording_gif, gif_frames, gif_start_time
        if not recording_gif:
            print("Recording GIF...")
            recording_gif, gif_start_time, gif_frames = True, time.time(), []

    def reload_palette():
        custom = load_custom_palette("palette.png")
        if custom is not None:
            PALETTES[4] = ("Custom", custom)
            print("Reloaded custom palette")

    def quit_app():
        print("Quit Camera Mode")
        cap.release()
        cv2.destroyAllWindows()
        exit()

    # Add buttons
    controls.add_button("Snapshot", (350, 80), size=(200, 50), action=take_snapshot)
    controls.add_button("Record GIF", (350, 140), size=(200, 50), action=start_gif)
    controls.add_button("Reload Palette", (350, 200), size=(200, 50), action=reload_palette)
    controls.add_button("Quit", (350, 260), size=(200, 50), action=quit_app)
    controls.add_slider("GIF length", 1, 15, 5, (50, 480))
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        controls.show()
        pixel_size, levels, brightness, contrast, palette_id, gif_length = controls.get_slider_values()

        # Process frame
        processed = process_frame(frame, pixel_size, levels, brightness, contrast, palette_id, PALETTES)

        # FPS
        frame_count += 1
        if frame_count >= 10:
            curr_time = time.time()
            fps = 10 / (curr_time - prev_time)
            prev_time, frame_count = curr_time, 0

        palette_name = PALETTES[palette_id][0] if palette_id in PALETTES else "Unknown"
        cv2.putText(processed, f"FPS: {fps:.1f} | Palette: {palette_name}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


        # GIF recording
        if recording_gif:
            gif_frames.append(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            if time.time() - gif_start_time >= gif_length:
                save_gif(gif_frames, fps=int(fps if fps > 0 else 10))
                recording_gif, gif_frames = False, []

        cv2.imshow("8-bit Camera Feed", processed)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
