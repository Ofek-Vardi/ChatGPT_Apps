import tkinter as tk
import tkinter.messagebox as messagebox
import pyperclip
import keyboard
import threading
import time


class ClipboardManager:
    def __init__(self):
        self.clipboard_items = []

    def add_item(self, item):
        if item in self.clipboard_items:
            self.clipboard_items.remove(item)
        self.clipboard_items.append(item)

    def get_items(self):
        return self.clipboard_items

    def clear_items(self):
        self.clipboard_items = []

    def move_to_top(self, item):
        if item in self.clipboard_items:
            self.clipboard_items.remove(item)
        self.clipboard_items.append(item)
        pyperclip.copy(item)


class ClipboardManagerGUI:
    def __init__(self, clipboard_manager):
        self.clipboard_manager = clipboard_manager

        self.root = tk.Tk()
        self.root.title("Clipboard Manager")
        self.root.withdraw()  # Hide the UI initially

        self.item_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.item_listbox.pack(fill=tk.BOTH, expand=True)
        self.item_listbox.bind("<<ListboxSelect>>", self.move_item_to_top)
        self.item_listbox.bind("<Button-1>", self.hide)  # Bind to mouse button 1 click event
        self.root.bind("<Escape>", self.hide)  # Bind to 'Escape' key press event
        self.root.bind("<FocusOut>", self.hide)  # Bind to focus out event

    def show(self):
        self.root.update()
        self.root.deiconify()
        self.root.focus_force()  # Set focus to the window

    def hide(self, event=None):
        self.root.withdraw()

    def move_item_to_top(self, event):
        selected_index = self.item_listbox.curselection()
        if selected_index:
            selected_item = self.item_listbox.get(selected_index)
            self.clipboard_manager.move_to_top(selected_item)
            self.item_listbox.delete(selected_index)
            self.item_listbox.insert(0, selected_item)


def handle_shortcut():
    if gui.root.state() == "normal":
        gui.hide()
    else:
        gui.show()


def safe_shutdown():
    if gui.root:
        gui.hide()
        keyboard.unhook_all()
        gui.root.destroy()


def check_clipboard():
    try:
        while True:
            try:
                current_clipboard = pyperclip.paste()
                if current_clipboard and current_clipboard != clipboard_manager.get_items()[-1:]:
                    clipboard_manager.add_item(current_clipboard)
                    gui.item_listbox.delete(0, tk.END)
                    for item in clipboard_manager.get_items():
                        gui.item_listbox.insert(tk.END, item)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                messagebox.showerror("Error", str(e))
            # Sleep for a short duration to avoid excessive CPU usage
            # and allow the GUI to handle events
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass


clipboard_manager = ClipboardManager()
gui = ClipboardManagerGUI(clipboard_manager)

keyboard.add_hotkey("alt+1", handle_shortcut)

check_clipboard_thread = threading.Thread(target=check_clipboard, daemon=True)
check_clipboard_thread.start()

try:
    gui.root.mainloop()
except KeyboardInterrupt:
    pass
finally:
    safe_shutdown()
