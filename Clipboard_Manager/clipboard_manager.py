import tkinter as tk
import tkinter.messagebox as messagebox
import pyperclip
import keyboard


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

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_items)
        self.clear_button.pack(side=tk.BOTTOM)

        self.root.bind("<Button>", self.hide)  # Bind to any mouse button click event
        self.root.bind("<Escape>", self.hide)  # Bind to 'Escape' key press event

    def show(self):
        self.root.update()
        self.root.deiconify()

    def hide(self, event=None):
        self.root.withdraw()

    def move_item_to_top(self, event):
        selected_index = self.item_listbox.curselection()
        if selected_index:
            selected_item = self.item_listbox.get(selected_index)
            self.clipboard_manager.move_to_top(selected_item)
            self.item_listbox.delete(selected_index)
            self.item_listbox.insert(0, selected_item)

    def clear_items(self):
        self.clipboard_manager.clear_items()
        self.item_listbox.delete(0, tk.END)


def handle_shortcut():
    if gui.root.state() == "normal":
        gui.hide()
    else:
        gui.show()

def safe_shutdown():
    gui.hide()
    keyboard.unhook_all()
    gui.root.destroy()

def check_clipboard():
    try:
        current_clipboard = pyperclip.paste()
        if current_clipboard and current_clipboard != clipboard_manager.get_items()[-1:]:
            clipboard_manager.add_item(current_clipboard)
            gui.item_listbox.delete(0, tk.END)
            for item in clipboard_manager.get_items():
                gui.item_listbox.insert(tk.END, item)
    except KeyboardInterrupt:
        safe_shutdown()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        safe_shutdown()
    finally:
        gui.root.after(1000, check_clipboard)


clipboard_manager = ClipboardManager()
gui = ClipboardManagerGUI(clipboard_manager)

keyboard.add_hotkey("alt+1", handle_shortcut)
gui.root.after(1000, check_clipboard)
gui.root.mainloop()
