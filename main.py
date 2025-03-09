import tkinter as tk
import keyboard
from pynput import mouse
from screen_capture import screenshot
from text_extract import extract_text

class GlobalSelectionApp:
    def __init__(self):
        self.activate = False
        self.start_x = None
        self.start_y = None

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.2)
        self.root.configure(bg="black")
        self.root.withdraw()

        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect_id = None

        keyboard.add_hotkey("ctrl+e", self.on_ctrl_e)
        keyboard.add_hotkey("esc", self.on_esc)

        self.mouse_listener = mouse.Listener(
            on_click=self.on_mouse_press,
            on_move=self.on_mouse_move
        )

    def on_ctrl_e(self):
        print("Selection mode activated")
        self.activate = True
        self.root.deiconify()
        self.mouse_listener.start()

    def on_esc(self):
        if self.activate:
            print("Selection cancelled")
            self.cancel_selection()

    def on_mouse_press(self, x, y, button, pressed):
        if self.activate and button == mouse.Button.left and pressed:
            self.start_x, self.start_y = x, y
            self.rect_id = self.canvas.create_rectangle(x, y, x, y, outline="red", width=2)
        elif self.activate and button == mouse.Button.left and not pressed :
            self.root.attributes("-alpha", 0)
            capture = screenshot(self.start_x, self.start_y, x - self.start_x, y - self.start_y)
            print("Saved as img.png")
            text = extract_text(capture)
            print(text)
            self.cancel_selection()

    def on_mouse_move(self, x, y):
        if self.activate and self.start_x is not None and self.start_y is not None:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, x, y)

    def cancel_selection(self):
        self.activate = False
        self.root.attributes("-alpha", 0.2)
        self.root.withdraw()
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.start_x, self.start_y = None, None
        self.rect_id = None
        self.mouse_listener.stop()
        self.mouse_listener = mouse.Listener(
            on_click=self.on_mouse_press,
            on_move=self.on_mouse_move
        )

if __name__ == "__main__":
    app = GlobalSelectionApp()
    app.root.mainloop()