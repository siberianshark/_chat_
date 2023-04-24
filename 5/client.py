import json
import socket
import sys
import log.client_log_config
import logging

CLIENT_LOGGER = logging.getLogger('client')

def send_message(sock, message):
    encoded_message = json.dumps(message).encode('utf-8')
    sock.send(encoded_message)
def receive_message(sock):
    data = sock.recv(1024)
    return json.loads(data.decode('utf-8'))
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