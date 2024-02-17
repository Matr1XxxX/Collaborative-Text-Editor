import socket
import threading
import tkinter as tk

class CollaborativeTextEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Collaborative Text Editor")

        self.text_widget = tk.Text(self, wrap="word")
        self.text_widget.pack(expand=True, fill="both")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 12345))

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        self.bind("<Key>", self.on_key_press)

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                self.text_widget.insert("end", data)
                self.text_widget.see("end")
            except:
                print("Server disconnected.")
                break

    def on_key_press(self, event):
        key = event.char
        if key:
            self.client.send(key.encode('utf-8'))

    def destroy(self):
        self.client.send('exit'.encode('utf-8'))
        super().destroy()

if __name__ == "__main__":
    app = CollaborativeTextEditor()
    app.mainloop()