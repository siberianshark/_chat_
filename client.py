import socket
import threading	
import dis

PEER_IP = '127.0.0.1'	
PEER_PORT = 7777	

class ClientVerifier(type):
    def __init__(cls, name, bases, attrs):
        cls._verify_sockets(attrs)
        super().__init__(name, bases, attrs)
        	
    @staticmethod
    def _verify_sockets(attrs):
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, socket.socket):
                raise TypeError(
                    f"Socket creation not allowed in class attribute '{attr_name}'")

            if callable(attr_value):
                bytecode = dis.Bytecode(attr_value)
                for instruction in bytecode:
                    if instruction.opname in ("CALL_FUNCTION", "CALL_METHOD") and isinstance(instruction.argval, socket.socket):
                        raise TypeError(
                            f"Socket method calls not allowed in function '{attr_name}'")

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._socket = None

    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))

    def send(self, data):
        if not self._socket:
            raise RuntimeError(
                "Socket is not connected. Call connect() method first.")

        self._socket.sendall(data.encode())

    def receive(self, buffer_size=1024):
        if not self._socket:
            raise RuntimeError(
                "Socket is not connected. Call connect() method first.")

        data = self._socket.recv(buffer_size)
        return data.decode()

    def close(self):
        if self._socket:
            self._socket.close()
            self._socket = None

def main():
    client = Client(PEER_IP, PEER_PORT)
    client.connect()
    client.send("Hello, server!")
    response = client.receive()
    print(response)
    client.close()