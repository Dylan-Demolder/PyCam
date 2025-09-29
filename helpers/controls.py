import cv2
import numpy as np

class Slider:
    def __init__(self, name, min_val, max_val, init_val, pos):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.value = init_val
        self.pos = pos
        self.width = 250
        self.height = 30
        self.dragging = False

    def draw(self, img):
        x, y = self.pos
        cv2.rectangle(img, (x, y), (x + self.width, y + self.height), (50, 50, 50), -1)
        slider_x = int(x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.width)
        cv2.rectangle(img, (x, y), (slider_x, y + self.height), (0, 200, 200), -1)
        cv2.rectangle(img, (x, y), (x + self.width, y + self.height), (255, 255, 255), 2)
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

class Button:
    def __init__(self, label, pos, size=(150, 40), color=(100, 100, 100), action=None):
        self.label = label
        self.pos = pos
        self.size = size
        self.color = color
        self.action = action
        self.clicked = False

    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, (x, y), (x + w, y + h), self.color, -1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # Center text
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.7
        thickness = 2
        (text_w, text_h), baseline = cv2.getTextSize(self.label, font, scale, thickness)
        text_x = x + (w - text_w) // 2
        text_y = y + (h + text_h) // 2

        cv2.putText(img, self.label, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), thickness)

    def handle_event(self, event, mx, my, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            x, y = self.pos
            w, h = self.size
            if x <= mx <= x + w and y <= my <= y + h:
                self.clicked = True
        elif event == cv2.EVENT_LBUTTONUP and self.clicked:
            self.clicked = False
            if self.action:  
                self.action()

class TextBox:
    def __init__(self, label, pos, size=(200, 40), text=""):
        self.label = label
        self.pos = pos
        self.size = size
        self.text = text
        self.active = False

    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        # background
        color = (150, 150, 150) if self.active else (100, 100, 100)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        # label
        cv2.putText(img, self.label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        # text inside box
        cv2.putText(img, self.text, (x + 5, y + int(h * 0.7)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    def handle_event(self, event, mx, my, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            x, y = self.pos
            w, h = self.size
            self.active = (x <= mx <= x + w and y <= my <= y + h)

    def handle_key(self, key):
        if not self.active:
            return
        if key == 8:  # backspace
            self.text = self.text[:-1]
        elif 32 <= key <= 126:  # printable ASCII
            self.text += chr(key)


class ControlPanel:
    def __init__(self, palettes):
        self.sliders = []
        self.buttons = []
        self.text_boxes = []
        cv2.namedWindow("Controls")
        cv2.setMouseCallback("Controls", self.mouse_event)

    def add_slider(self, *args, **kwargs):
        self.sliders.append(Slider(*args, **kwargs))

    def add_button(self, *args, **kwargs):
        self.buttons.append(Button(*args, **kwargs))

    def add_textbox(self, *args, **kwargs):
        self.text_boxes.append(TextBox(*args, **kwargs))

    def mouse_event(self, event, x, y, flags, param):
        for s in self.sliders:
            s.handle_event(event, x, y, flags, param)
        for b in self.buttons:
            b.handle_event(event, x, y, flags, param)
        for t in self.text_boxes:
            t.handle_event(event, x, y, flags, param)

    def handle_key(self, key):
        for t in self.text_boxes:
            t.handle_key(key)

    def get_slider_values(self):
        return [s.value for s in self.sliders]
    
    def get_textbox_value(self, label):
        for t in self.text_boxes:
            if t.label == label:
                return t.text
        return ""

    def show(self):
        panel = np.zeros((600, 700, 3), dtype=np.uint8)
        cv2.putText(panel, "RetroCam Controls", (50, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        for s in self.sliders:
            s.draw(panel)
        for b in self.buttons:
            b.draw(panel)
        for t in self.text_boxes:
            t.draw(panel)
        cv2.imshow("Controls", panel)
