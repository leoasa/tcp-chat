# Final Project Part 2
import socket
import sys
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="TCP Chat Client")
    parser.add_argument('--id', required=True, help="Client ID")
    parser.add_argument('--port', type=int, required=True, help="Client port to listen on")
    parser.add_argument('--server', required=True, help="Server IP and port in format ip:port")
    args = parser.parse_args()
    return args.id, args.port, args.server.split(':')

def create_socket():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Failed to create socket. Error: {e}")
        sys.exit()
    return client_socket

def connect_to_server(client_socket, server_ip, server_port):
    try:
        client_socket.connect((server_ip, int(server_port)))
    except socket.error as e:
        print(f"Connection to server failed. Error: {e}")
        sys.exit()

def register(client_socket, client_id, client_port):
    message = f"REGISTER\r\nclientID: {client_id}\r\nIP: {client_socket.getsockname()[0]}\r\nPort: {client_port}\r\n\r\n"
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    print("Registration response:", response)

def bridge(client_socket, client_id):
    message = f"BRIDGE\r\nclientID: {client_id}\r\n\r\n"
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    return response  # Return peer contact info

def chat(peer_socket, client_id, mode):

    while (True):
      try:

        if mode == "WAIT":
            read_msg = peer_socket.recv(1024).decode()
            if read_msg == '/quit':
                print("\nPeer has left the chat.")
                return
            print(f"{read_msg}\n")
            mode = "WRITE"

        elif mode == "WRITE":
            print("In WRITE mode\n")
            write_msg = input(f"{client_id}> ")
            chat_msg = f"{client_id}> {write_msg}\n\n"
            peer_socket.send(chat_msg.encode())
            if write_msg == '/quit':
                print("\nProgram terminated by user.")
                return
            mode = "READ"

        elif mode == "READ":
            print("\nIn READ mode\n")
            read_msg = peer_socket.recv(1024).decode()
            if '/quit' in str(read_msg):
                print("\nPeer has left the chat.")
                return
            print(f"{read_msg}\n")
            mode = "WRITE"

      except KeyboardInterrupt:
          return

def main():

    client_id, client_port, server_info = parse_arguments()
    server_ip, server_port = server_info
    chat_ip = '127.0.0.4'
    chat_port = '2800'
    print(f"\n{client_id}> running on {server_ip}\n")

    #Client Main Loop
    while True:

        try:
            #Get Input
            command = input("Enter command (/id, /register, /bridge, /chat): ").strip()

            #ID
            if command == "/id":
                print(f"Client ID: {client_id}\n")

            #REGISTER
            elif command == "/register":
                client_socket = create_socket()
                connect_to_server(client_socket, server_ip, server_port)
                print("\nConnected to the server successfully.\n")
                register(client_socket, client_id, client_port)
                client_socket.close()

            #BRIDGE
            elif command == "/bridge":
                client_socket = create_socket()
                connect_to_server(client_socket, server_ip, server_port)
                print("\nConnected to the server successfully.\n")
                response = bridge(client_socket, client_id)
                print("Bridge response:", response)
                client_socket.close()

            #CHAT
            elif command == "/chat":
                
                print("\nEntering chat...\n")

                #First digit of IP in BRIDGEACK; shows BRIDGEACK isn't empty
                peer_ip1 = response.split("IP: ", 1)[-1][0]

                if peer_ip1.isdigit():
                    #BRIDGEACK is not empty - go into write mode

                    mode = "WRITE" 

                    #Assumes the other peer is in wait and connects to it
                    peer_socket = create_socket()
                    peer_socket.connect((chat_ip, int(chat_port)))
                    chat(peer_socket, client_id, mode)
                    peer_socket.close()


                else:
                    #BRIDGEACK is empty - go into wait mode
                    print("Other client not bridged.")
                    print("\nIn WAIT mode\n")
                    mode = "WAIT"

                    #Creates the socket for the peer that will act as a server
                    peer_server_socket = create_socket()
                    peer_server_socket.bind((chat_ip, int(chat_port)))
                    peer_server_socket.listen(1)
                    peer_socket, _ = peer_server_socket.accept()
                    chat(peer_socket, client_id, mode)
                    peer_server_socket.close()

                print("\nChat session ended.\n")
                break

            #Invalid Command Error Catch
            else:
                print("Invalid command. Please try again.")

        #Control-C Exit
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            break

if __name__ == "__main__":
    main()
