import socket
import threading
from networking import handle_client

clients = []

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)

    print('Server listening on port 12345')

    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, clients))
        client_handler.start()

if __name__ == "__main__":
    start_server()