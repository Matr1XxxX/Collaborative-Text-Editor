# server_side.py
import socket
import ssl
import threading
from networking import handle_client

class Group:
    def __init__(self, name):
        self.name = name
        self.clients = []

def start_server(host, port):
    # Create an SSL context
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # Set minimum and maximum SSL/TLS protocol version
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
    ssl_context.maximum_version = ssl.TLSVersion.TLSv1_2

    # Load the self-signed certificate and key
    ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    server = ssl_context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_side=True)
    server.bind((host, port))
    server.listen(5)
    print(f'Server listening on {host}:{port}')

    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')

        # Receive group name from the client
        group_name = client_socket.recv(1024).decode('utf-8')
        
        # Find or create the group
        group = groups.get(group_name)
        if not group:
            group = Group(group_name)
            groups[group_name] = group

        # Add client to the group
        group.clients.append((client_socket, addr))

        # Start handling client in a separate thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, group))
        client_handler.start()

def create_and_start_servers():
    global servers
    servers = []
    for port in range(12345, 12347):  # Change the range as per the number of servers needed
        server_thread = threading.Thread(target=start_server, args=('localhost', port))
        servers.append(server_thread)
        server_thread.start()

if __name__ == "__main__":
    groups = {}  # Dictionary to store groups
    create_and_start_servers()
    for server in servers:
        server.join()
