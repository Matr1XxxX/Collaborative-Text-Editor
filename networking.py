import socket

def handle_client(client_socket, addr, clients):
    clients.append(client_socket)

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            if data.lower() == 'exit':
                break
            else:
                broadcast(data.encode('utf-8'), client_socket, clients)
        except:
            clients.remove(client_socket)
            break

    client_socket.close()

def broadcast(message, client_socket, clients):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def receive_messages(client_socket, text_widget):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            text_widget.delete(1.0, "end")
            text_widget.insert("end", data)
            text_widget.see("end")
        except:
            print("Server disconnected.")
            break

def send_text(text_widget, client_socket):
    text_content = text_widget.get("1.0", "end-1c")  
    client_socket.send(text_content.encode('utf-8'))
