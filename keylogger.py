import tkinter as tk
from tkinter import scrolledtext

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Keylogger")
        self.root.geometry("400x300")
        self.root.config(bg='white')
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg='white', fg='black', font=('Arial', 12))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.log_file = open("keylog.txt", "a")

        self.shift_pressed = False
        self.caps_lock = False

        # Bindings for key events
        self.root.bind("<KeyPress>", self.on_press)
        self.root.bind("<KeyRelease>", self.on_release)

    def on_press(self, event):
        char_to_log = event.char
        
        if event.keysym in ["Shift_L", "Shift_R"]:
            self.shift_pressed = True
        elif event.keysym == "Caps_Lock":
            self.caps_lock = not self.caps_lock

        # Handle special keys
        special_keys = {
            "space": "[SPACE]",
            "Return": "[ENTER]",
            "Escape": "[ESC]",
            "Tab": "[TAB]",
            "BackSpace": "[BACKSPACE]"
        }
        
        if event.keysym in special_keys:
            char_to_log = special_keys[event.keysym]
        elif char_to_log:
            # Apply shift or caps lock for uppercase letters
            if self.shift_pressed or self.caps_lock:
                char_to_log = char_to_log.upper()
            elif not event.char.isalpha():
                char_to_log = event.char

        # Display and log the character
        self.text_area.insert(tk.END, char_to_log)
        self.log_file.write(char_to_log)
        self.text_area.see(tk.END)

    def on_release(self, event):
        if event.keysym in ["Shift_L", "Shift_R"]:
            self.shift_pressed = False

    def on_closing(self):
        self.log_file.close()
        self.root.destroy()

root = tk.Tk()
app = KeyloggerApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)

root.mainloop()
