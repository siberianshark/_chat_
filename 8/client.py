import socket
import threading

PEER_IP = '127.0.0.1'
PEER_PORT = 7777


def receive():
    while True:
        try:
            data = client_socket.recv(1024)
            print(data.decode())
        except:
            break


def send():
    while True:
        message = input()
        client_socket.send(message.encode())


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client_socket.connect((PEER_IP, PEER_PORT))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()