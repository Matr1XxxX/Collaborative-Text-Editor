# networking.py
import threading
import tkinter as tk
import socket

# networking.py
def handle_client(client_socket, addr, group):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            if data.lower() == 'exit':
                break
            else:
                broadcast(data.encode('utf-8'), client_socket, group)
        except:
            break

    client_socket.close()

def broadcast(message, client_socket, group):
    for client in group.clients:
        if client[0] != client_socket:
            try:
                client[0].send(message)
            except:
                group.clients.remove(client)


def receive_messages(client_socket, text_widget):
    last_data = ""
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            
            if data != last_data:
                text_widget.delete(1.0, "end")
                text_widget.insert("end", data)
                text_widget.see("end")
                last_data = data
                
        except:
            print("Server disconnected.")
            break


def send_text(text_widget, client_socket):
    text_content = text_widget.get("1.0", "end-1c")  
    client_socket.send(text_content.encode('utf-8'))
