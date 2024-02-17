import socket
import tkinter as tk
import threading
from tkinter import filedialog
import tkinter.font as tkFont
from networking import receive_messages, send_text
from utils import save_file, FindDialog , zoom_in , zoom_out

class CollaborativeTextEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Collaborative Text Editor")

        self.text_widget = tk.Text(self, wrap="word")
        self.text_widget.pack(expand=True, fill="both")
        
        # Set the default font size here
        self.text_widget.configure(font=("TkFixedFont", 12))

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
        
        # Add View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Zoom In", command=self.zoom_in)
        self.view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        self.config(menu=self.menu_bar)

    def on_key_press(self, event):
        send_text(self.text_widget, self.client)

    def save_file(self):
        save_file(self.text_widget)

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
        
    def zoom_in(self):
        zoom_in(self.text_widget)

    def zoom_out(self):
        zoom_out(self.text_widget)

    def destroy(self):
        self.client.send('exit'.encode('utf-8'))
        super().destroy()