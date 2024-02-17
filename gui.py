import socket
import tkinter as tk
import threading
from tkinter import filedialog
from tkinter import messagebox  # Import messagebox for showing alerts
from networking import receive_messages, send_text

class CollaborativeTextEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Collaborative Text Editor")

        self.text_widget = tk.Text(self, wrap="word")
        self.text_widget.pack(expand=True, fill="both")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 12345))

        self.receive_thread = threading.Thread(target=receive_messages, args=(self.client, self.text_widget))
        self.receive_thread.start()

        self.text_widget.bind("<Key>", self.on_key_press)

        # Add a menu bar
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find_text)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.config(menu=self.menu_bar)

    def on_key_press(self, event):
        send_text(self.text_widget, self.client)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            text_content = self.text_widget.get("1.0", "end-1c")
            with open(file_path, "w") as file:
                file.write(text_content)
            messagebox.showinfo("Info", "File saved successfully.")  # Show a success message

    def cut_text(self):
        self.clipboard_clear()
        text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.clipboard_append(text)
        self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def copy_text(self):
        self.clipboard_clear()
        text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.clipboard_append(text)

    def paste_text(self):
        text = self.selection_get(selection='CLIPBOARD')
        self.text_widget.insert(tk.INSERT, text)

    def find_text(self):
        find_dialog = FindDialog(self)
        self.wait_window(find_dialog)

    def destroy(self):
        self.client.send('exit'.encode('utf-8'))
        super().destroy()

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
