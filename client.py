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

        self.text_widget.bind("<Key>", self.on_key_press)

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                self.text_widget.delete(1.0, "end")
                self.text_widget.insert("end", data)
                self.text_widget.see("end")
            except:
                print("Server disconnected.")
                break

    def on_key_press(self, event):
        self.send_text()

    def send_text(self):
        text_content = self.text_widget.get("1.0", "end-1c")  # Get the entire text content
        self.client.send(text_content.encode('utf-8'))

    def destroy(self):
        self.client.send('exit'.encode('utf-8'))
        super().destroy()

if __name__ == "__main__":
    app = CollaborativeTextEditor()
    app.mainloop()
