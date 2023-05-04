import socket
import threading

HOST = '0.0.0.0'
PORT = 7777

clients = []


def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                clients.remove(client_socket)
                client_socket.close()
                print(f"Connection with {client_address}  has been refused")
                break

            for c in clients:
                if c != client_socket:
                    c.send(data)
        except:
            clients.remove(client_socket)
            client_socket.close()
            print(f"Connection with {client_address} has been refused")
            break


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_socket.bind((HOST, PORT))


server_socket.listen()

print(f"Server has been started on port: {PORT}")

while True:

    client_socket, client_address = server_socket.accept()

    clients.append(client_socket)

    client_thread = threading.Thread(
        target=handle_client, args=(client_socket, client_address))
    client_thread.start()