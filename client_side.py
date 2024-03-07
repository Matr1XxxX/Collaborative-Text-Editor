import socket
import ssl
from gui import CollaborativeTextEditor
import threading
import tkinter as tk

def create_client_context():
    server_host = input("Enter server ip address: ")
    server_port = int(input("Enter server port: "))

    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_2

    # Load the system's trusted CA certificates
    context.load_default_certs()

    # Add the server's certificate as a trusted CA (change 'server.crt' to your server's certificate file)
    context.load_verify_locations(cafile="server.crt")
    context.check_hostname = False

    return context, server_host, server_port


def main():
    group_name = input("Enter project name: ")
    context, server_host, server_port = create_client_context()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = context.wrap_socket(client_socket, server_hostname=server_host)

    try:
        secure_socket.connect((server_host, server_port))
        print("Connected to the server.")

        # Send group name to the server
        secure_socket.send(group_name.encode('utf-8'))

        # Launch the GUI
        app = CollaborativeTextEditor.get_instance(secure_socket)
        app.protocol("WM_DELETE_WINDOW", app.on_close)
        app.mainloop()
    except Exception as e:
        print(f"Error connecting to the server: {e}")
    finally:
        secure_socket.close()

if __name__ == "__main__":
    main()