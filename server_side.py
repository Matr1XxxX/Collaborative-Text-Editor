import socket
import ssl
import threading
from networking import handle_client

clients = []

def start_server():
    # Create an SSL context
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # Set minimum and maximum SSL/TLS protocol version
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
    ssl_context.maximum_version = ssl.TLSVersion.TLSv1_2

    # Load the self-signed certificate and key
    ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    server = ssl_context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_side=True)
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
