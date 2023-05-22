import dis
import socket	
import threading	


HOST = '0.0.0.0'	
PORT = 7777
clients = []

class PortDescriptor:
    def __init__(self, default_port=7777):
        self._default_port = default_port
        self._value = None


    def __get__(self, instance, owner):
        if self._value is None:
            return self._default_port
        return self._value
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Port number must be an integer.")
        if value < 0:
            raise ValueError(
                "Port number must be greater than or equal to zero.")
        self._value = value
class ServerVerifier(type):
    def __init__(cls, name, bases, attrs):
        cls._verify_sockets(attrs)
        super().__init__(name, bases, attrs)

    @staticmethod
    def _verify_sockets(attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value):
                bytecode = dis.Bytecode(attr_value)
                for instruction in bytecode:
                    if instruction.opname == "CALL_METHOD" and isinstance(instruction.argval, socket.socket) and instruction.argval.type != socket.SOCK_STREAM:
                        raise TypeError(
                            f"Socket method calls not allowed in function '{attr_name}'")
                    if instruction.opname == "LOAD_METHOD" and instruction.argval == "connect":
                        raise TypeError(
                            f"Socket 'connect' method calls not allowed in function '{attr_name}'")

class Server(metaclass=ServerVerifier):
    port = PortDescriptor()
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._socket = None

    def start(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self.host, self.port))
        self._socket.listen(1)

        while True:
            client_socket, client_address = self._socket.accept()
            self.handle_client(client_socket, client_address)

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                data = client_socket.recv(1024)

                if not data:
                    clients.remove(client_socket)
                    client_socket.close()
                    print(
                        f"Connection with {client_address}  has been refused")
                    break

                for c in clients:
                    if c != client_socket:
                        c.send(data)
            except:
                clients.remove(client_socket)	                
                client_socket.close()	                
                print(f"Connection with {client_address} has been refused")
                break	               

    def close(self):
        if self._socket:
            self._socket.close()
            self._socket = None
class MyServer(Server):
    def handle_client(self, client_socket, client_address):
        data = client_socket.recv(1024)
        response = "Received: " + data.decode()
        client_socket.sendall(response.encode())
        client_socket.close()

my_server = MyServer(HOST, PORT)
my_server.start()