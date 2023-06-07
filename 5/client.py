import json
import socket
import sys
import log.client_log_config
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


CLIENT_LOGGER = logging.getLogger('client')


@log
def send_message(sock, message):
    encoded_message = json.dumps(message).encode('utf-8')
    sock.send(encoded_message)


@log
def receive_message(sock):
    data = sock.recv(1024)
    return json.loads(data.decode('utf-8'))


@log
def create_presence_message(account_name):
    message = {
        'action': 'presence',
        'time': 12345,
        'user': {
            'account_name': account_name,
            'status': 'online'
        }
    }
    return message


@log
def parse_server_response(response):
    if 'response' in response:
        return response['response']
    else:
        return None
def main():
    if len(sys.argv) < 2:
        print("Usage: client.py <addr> [<port>]")
        return
    try:
        address = sys.argv[1]
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 7777
        sock = socket.socket()
        sock.connect((address, port))
        account_name = 'Guest'
        message = create_presence_message(account_name)
        send_message(sock, message)
        response = receive_message(sock)
        result = parse_server_response(response)
        # if result:
        CLIENT_LOGGER.debug(f"Server response: {result}")
        print(f"Server response: {result}")
        sock.close()
    except ConnectionRefusedError:
        # print("Invalid server response")
        CLIENT_LOGGER.critical(
            f'Could not connect to the server {address}:{port}')
        sock.close()
    except OSError:
        CLIENT_LOGGER.critical(
            f"Address isn't valid {address}:{port}")
        sock.close()
    except json.JSONDecodeError:
        CLIENT_LOGGER.error("Couldn't decode json string")
if __name__ == '__main__':
    main()