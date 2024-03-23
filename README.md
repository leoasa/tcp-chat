# tcp-chat
Python3 chat client and server programs using TCP sockets. Finite state machine diagram included in tcp-chat-state-diagram.pdf.

## Description of the Chat Program

The TCP-Chat program is a communication application that allows two peers to exchange messages using TCP. This program is designed to emulate the functionality of walkie-talkies in a digital format where peers can alternate between writing and reading messages in a turn-based fashion.

## Server

The server in this program is responsible for managing connections and facilitating the exchange of peer contact information. It operates on a designated port and handles two specific requests:

- `REGISTER`: For clients to register their contact details.
- `BRIDGE`: To provide clients with the contact information of their peer for establishing a direct chat connection.

The server maintains a transient connection with the clients, closing the TCP connection after each request/response cycle.

## Client

Clients interact with the server using a set of terminal commands to register and bridge. They operate in two distinct modes:

1. `WAIT`: The client awaits contact from another peer.
2. `CHAT`: The client is engaged in a message exchange with a peer.

A client transitions to CHAT mode after completing the registration and bridge process, either upon receiving a chat request or by initiating a chat with the /chat command.

## Operation Details

The server program stores contact information upon a REGISTER request for later retrieval when a BRIDGE request is made. It must be run before the client program and specify its port number. An example of proper execution is as follows:

`python3 tcp-chat-server.py --port=5555`

The client program requires initial information such as client ID, port number, and server address to start. The server address is hardcoded as 127.0.0.2. An example of proper execution is as follows:

`python3 tcp-chat-client.py --id='user1' --port=3000 --server='127.0.0.2:5555'`

The chat session can be ended by either peer entering `/quit`, which terminates the TCP connection and the program.

## Terminal Commands

Clients should support the following terminal commands:

- `/id`: Display the user's id.
- `/register`: Send a REGISTER message to the server.
- `/bridge`: Request peer contact information from the server.
- `/chat`: Initiate a chat session with a peer.
- `/quit`: End the chat session and close the socket.

## Message Types

The message exchange between clients and the server resembles HTTP in style, with plain text request and response messages. The supported messages include REGISTER, BRIDGE, CHAT, QUIT for client requests, and REGACK, BRIDGEACK for server responses.

## Assumptions

For simplicity, the following assumptions are made:

- Only one TCP connection is open at any given time.
- Clients and servers maintain a transient connection, closing it after each request/response cycle.
- Peers alternate between writing and reading modes during a chat session.
- There are only two clients and one server.
- The chat is initiated by only one client, and only one user writes at a time.

## Terminal Output Messages

Both server and client programs provide feedback in the terminal to indicate their state and actions, such as listening for connections, receiving messages, and initiating chat requests.

## Example Usage

The program requires three terminal windows to simulate the server and the two clients. The operation sequence starts with the server, followed by the registration and bridging of the first client, and subsequently the second client who initiates the chat.

## Additional Notes

This program is a fundamental implementation of a TCP-based chat system, focusing on network programming concepts. The server and client components demonstrate the core functionalities of a networked communication application.
