import socket
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="TCP Chat Server")
    parser.add_argument('--port', type=int, required=True, help="Port for the server to listen on")
    args = parser.parse_args()
    return args.port

class ChatServer:
    def __init__(self, port):
        self.host = '127.0.0.2'
        self.port = int(port)
        self.clients = {}  

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, _ = server_socket.accept()
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        data = client_socket.recv(1024).decode()
        command, *params = data.split('\r\n')
        
        if command.startswith("REGISTER"):
            self.register_client(params, client_socket)
        elif command.startswith("BRIDGE"):
            self.bridge_client(params[0].split(": ")[1], client_socket)

    def register_client(self, params, client_socket):
        client_id = ""
        for param in params:
            if param.startswith('clientID'):
                client_id = param.split(": ")[1]
            elif param.startswith('IP'):
                ip = param.split(": ")[1]
            elif param.startswith('Port'):
                port = param.split(": ")[1]
        self.clients[client_id] = (ip, port)
        response = f"REGACK\r\nclientID: {client_id}\r\nIP: {ip}\r\nPort: {port}\r\n\r\n"
        client_socket.send(response.encode())
        print(f"REGISTER {client_id} from {ip}:{port} received")

    def bridge_client(self, client_id, client_socket):
        for cid, (ip, port) in self.clients.items():
            if cid != client_id:
                response = f"BRIDGEACK\r\nclientID: {cid}\r\nIP: {ip}\r\nPort: {port}\r\n\r\n"
                client_socket.send(response.encode())
                print(f"BRIDGE: {cid} {ip}:{port} {client_id} {ip}:{self.clients[client_id][1]}")
                return

        response = "BRIDGEACK\r\nclientID: \r\nIP: \r\nPort: \r\n\r\n"
        client_socket.send(response.encode())
        print(f"BRIDGE: {client_id} {ip}:{port}")

if __name__ == "__main__":
    port = parse_arguments()
    server = ChatServer(port)
    server.start()
