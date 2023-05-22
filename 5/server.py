import json
import socket
import sys
import log.server_log_config
import logging
import datetime
import inspect


def log(func):
    def wrapper(*args, **kwargs):
        calling_func = inspect.stack()[1][3]
        now = datetime.datetime.now()
        log_string = f'{now} Function {func.__name__} called from function {calling_func}'
        print(log_string)
        with open('log.txt', 'a') as log_file:
            log_file.write(log_string + '\n')
        result = func(*args, **kwargs)
        return result
    return wrapper


SERVER_LOGGER = logging.getLogger('server')


@log
def send_message(sock, message):
    encoded_message = json.dumps(message).encode('utf-8')
    sock.send(encoded_message)


@log
def receive_message(sock):
    data = sock.recv(1024)
    return json.loads(data.decode('utf-8'))


@log
def handle_presence_message(message):
    response = {
        'response': 200,
        'time': message['time'],
        'alert': f"{message['user']['account_name']} is online"
    }
    return response


@log
def handle_client_message(sock, message):
    action = message.get('action')
    if action == 'presence':
        response = handle_presence_message(message)
        send_message(sock, response)
    else:
        response = {
            'response': 400,
            'error': f"Unknown action '{action}'"
        }
        send_message(sock, response)
def main():
    if len(sys.argv) < 2:
        print("Usage: server.py -p <port> [-a <addr>]")
        SERVER_LOGGER.info(" Use 'server.py -p <port> [-a <addr>]'")
        return
    port_index = sys.argv.index('-p') + 1
    port = int(sys.argv[port_index])
    address = ''
    if '-a' in sys.argv:
        addr_index = sys.argv.index('-a') + 1
        address = sys.argv[addr_index]
    sock = socket.socket()
    sock.bind((address, port))
    sock.listen(1)
    SERVER_LOGGER.debug(f"Listening on {address}:{port}")
    print(f"Listening on {address}:{port}")
    while True:
        try:
            client_sock, client_address = sock.accept()
            print(f"Accepted connection from {client_address}")
            message = receive_message(client_sock)
            handle_client_message(client_sock, message)
            SERVER_LOGGER.info(f"Accepted connection from {client_address}")
            client_sock.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(
                f"Couldn't decode json string from {client_address}")
            client_sock.close()
if __name__ == '__main__':
    main()
