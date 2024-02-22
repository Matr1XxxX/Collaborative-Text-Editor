import socket
import threading
import tkinter as tk
from tkinter import filedialog
from networking import receive_messages, send_text
from gui import CollaborativeTextEditor

if __name__ == "__main__":
    app = CollaborativeTextEditor()
    app.mainloop()