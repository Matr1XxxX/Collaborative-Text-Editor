import socket
import tkinter as tk
import threading
from tkinter import filedialog
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
        self.config(menu=self.menu_bar)

    def on_key_press(self, event):
        send_text(self.text_widget, self.client)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            text_content = self.text_widget.get("1.0", "end-1c")
            with open(file_path, "w") as file:
                file.write(text_content)
            print("File saved successfully.")

    def destroy(self):
        self.client.send('exit'.encode('utf-8'))
        super().destroy()
