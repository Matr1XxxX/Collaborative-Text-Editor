import socket
import threading

clients = []
text_content = ""

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove the broken connection
                clients.remove(client)

def handle_client(client_socket, addr):
    clients.append(client_socket)

    global text_content
    client_socket.send(text_content.encode('utf-8'))  # Send the current text content to the new client

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            if data.lower() == 'exit':
                break
            elif data.lower() == 'get_text':
                client_socket.send(text_content.encode('utf-8'))  # Send the current text content to the client
            else:
                text_content = data
                # Broadcast the updated text content to all connected clients
                broadcast(text_content.encode('utf-8'), client_socket)
        except:
            # Remove the broken connection
            clients.remove(client_socket)
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)

    print('Server listening on port 12345')

    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

start_server()
