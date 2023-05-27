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
        self.root.overrideredirect(True)  # Remove title bar and window controls

        self.item_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.item_listbox.pack(fill=tk.BOTH, expand=True)
        self.root.bind("<Button-1>", self.move_item_to_top)  # Bind to mouse button 1 click event
        self.root.bind("<Escape>", self.hide)  # Bind to 'Escape' key press event
        self.root.bind("<FocusOut>", self.hide)  # Bind to focus out event

    def show(self):
        # Retrieve cursor position
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()

        # Position the window near the cursor
        self.root.geometry(f"+{x}+{y}")  # Set window position to cursor coordinates

        self.root.update()
        self.root.deiconify()
        self.root.lift()  # Raise the window to the top
        self.root.attributes("-topmost", True)  # Ensure the window stays on top

        self.root.focus_force()  # Set focus to the window

        if self.item_listbox.size() > 0:
            self.item_listbox.selection_set(0)  # Select the first item
            self.item_listbox.activate(0)  # Set the focus to the first item

            self.root.bind("<Up>", self.move_up)  # Bind to up arrow key
            self.root.bind("<Down>", self.move_down)  # Bind to down arrow key
            self.root.bind("<Return>", self.move_item_to_top)  # Bind to Enter key

    def hide(self, event=None):
        self.root.withdraw()

    def update_item_list(self):
        self.item_listbox.delete(0, tk.END)
        for item in self.clipboard_manager.get_items()[::-1]:
            self.item_listbox.insert(tk.END, item)

    def move_up(self, event):
        current_index = self.item_listbox.curselection()
        if current_index:
            new_index = max(0, current_index[0] - 1)
            self.item_listbox.selection_clear(0, tk.END)
            self.item_listbox.selection_set(new_index)
            self.item_listbox.activate(new_index)
            self.item_listbox.see(new_index)  # Scroll to the new index

    def move_down(self, event):
        current_index = self.item_listbox.curselection()
        if current_index:
            new_index = min(current_index[0] + 1, self.item_listbox.size() - 1)
            self.item_listbox.selection_clear(0, tk.END)
            self.item_listbox.selection_set(new_index)
            self.item_listbox.activate(new_index)
            self.item_listbox.see(new_index)  # Scroll to the new index

    def move_item_to_top(self, event=None):
        selected_index = self.item_listbox.curselection()
        if selected_index:
            self.hide()
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
    previous_clipboard = pyperclip.paste()
    try:
        while True:
            current_clipboard = pyperclip.paste()
            newest_item = clipboard_manager.get_items()[-1] if clipboard_manager.get_items() else None
            if current_clipboard != previous_clipboard and current_clipboard != newest_item:
                clipboard_manager.add_item(current_clipboard)
                gui.update_item_list()
                previous_clipboard = current_clipboard
            # Sleep for a short duration to avoid excessive CPU usage
            # and allow the GUI to handle events
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        gui.safe_shutdown()

clipboard_manager = ClipboardManager()
gui = ClipboardManagerGUI(clipboard_manager)

keyboard.add_hotkey("alt+1", handle_shortcut)

check_clipboard_thread = threading.Thread(target=check_clipboard, daemon=True)
check_clipboard_thread.start()

try:
    gui.root.mainloop()
except KeyboardInterrupt:
    pass
except Exception as e:
    messagebox.showerror("Error", str(e))
finally:
    safe_shutdown()
