import cv2
import numpy as np

# --- Slider Data Structure ---
class Slider:
    def __init__(self, name, min_val, max_val, init_val, pos):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.value = init_val
        self.pos = pos  # (x, y) top-left
        self.width = 200
        self.height = 30
        self.dragging = False

    def draw(self, img):
        x, y = self.pos
        # Background
        cv2.rectangle(img, (x, y), (x + self.width, y + self.height), (50, 50, 50), -1)
        # Slider fill
        slider_x = int(x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.width)
        cv2.rectangle(img, (x, y), (slider_x, y + self.height), (0, 200, 200), -1)
        # Border
        cv2.rectangle(img, (x, y), (x + self.width, y + self.height), (255, 255, 255), 2)
        # Label
        cv2.putText(img, f"{self.name}: {self.value}", (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    def handle_event(self, event, mx, my, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.pos[0] <= mx <= self.pos[0] + self.width and self.pos[1] <= my <= self.pos[1] + self.height:
                self.dragging = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False
        elif event == cv2.EVENT_MOUSEMOVE and self.dragging:
            rel_x = max(self.pos[0], min(mx, self.pos[0] + self.width))
            percent = (rel_x - self.pos[0]) / self.width
            self.value = int(self.min_val + percent * (self.max_val - self.min_val))

# --- Control Panel ---
class ControlPanel:
    def __init__(self, palettes):
        self.sliders = [
            Slider("Pixel Size", 1, 50, 12, (50, 60)),
            Slider("Color Levels", 1, 16, 6, (50, 130)),
            Slider("Brightness", 0, 100, 50, (50, 200)),
            Slider("Contrast", 0, 100, 50, (50, 270)),
            Slider("Palette", 0, 4, 0, (50, 340)),
        ]
        self.palettes = palettes
        cv2.namedWindow("Controls")
        cv2.setMouseCallback("Controls", self.mouse_event)

    def mouse_event(self, event, x, y, flags, param):
        for s in self.sliders:
            s.handle_event(event, x, y, flags, param)

    def get_values(self):
        return [s.value for s in self.sliders]

    def show(self):
        panel = np.zeros((450, 350, 3), dtype=np.uint8)
        cv2.putText(panel, "RetroCam Controls", (50, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        for s in self.sliders:
            s.draw(panel)
        cv2.imshow("Controls", panel)