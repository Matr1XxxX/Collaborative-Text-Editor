import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import messagebox

def save_file(text_widget):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        text_content = text_widget.get("1.0", "end-1c")
        with open(file_path, "w") as file:
            file.write(text_content)
        messagebox.showinfo("Info", "File saved successfully.")  # Show a success message

def zoom_in(text_widget):
    font = tkFont.Font(font=text_widget.cget("font"))
    current_size = font.actual()["size"]
    new_size = current_size + 2
    text_widget.configure(font=("TkFixedFont", new_size))

def zoom_out(text_widget):
    font = tkFont.Font(font=text_widget.cget("font"))
    current_size = font.actual()["size"]
    new_size = current_size - 2
    if new_size > 0:
        text_widget.configure(font=("TkFixedFont", new_size))

class FindDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Find")
        self.geometry("300x100")

        self.find_label = tk.Label(self, text="Find:")
        self.find_label.pack()

        self.find_entry = tk.Entry(self)
        self.find_entry.pack()

        self.find_button = tk.Button(self, text="Find", command=self.find)
        self.find_button.pack()

    def find(self):
        search_str = self.find_entry.get()
        text_widget = self.parent.text_widget
        start_index = text_widget.search(search_str, "1.0", stopindex=tk.END)
        if start_index:
            end_index = f"{start_index}+{len(search_str)}c"
            text_widget.tag_remove("found", "1.0", tk.END)
            text_widget.tag_add("found", start_index, end_index)
            text_widget.see(start_index)
            text_widget.focus_set()
        else:
            messagebox.showinfo("Info", "Text not found.")