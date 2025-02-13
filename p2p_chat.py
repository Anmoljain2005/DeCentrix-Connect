import socket
import threading
import sys

# Global variables
peers = {}  
server_socket = None
client_sockets = []
lock = threading.Lock()

def start_server(port):
    """Start a TCP server to listen for incoming connections."""
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            with lock:
                peers[f"{client_address[0]}:{client_address[1]}"] = client_socket
                client_sockets.append(client_socket)
            print(f"New connection from {client_address[0]}:{client_address[1]}")
            threading.Thread(target=receive_messages, args=(client_socket, client_address)).start()
        except Exception as e:
            print(f"Error accepting connection: {e}")
            break

def receive_messages(client_socket, client_address):
    """Receive messages from a connected peer and dynamically add the sender to the peers list."""
    sender_key = f"{client_address[0]}:{client_address[1]}"
    with lock:
        if sender_key not in peers:
            peers[sender_key] = client_socket
            print(f"Added {sender_key} to active peers.")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from {client_address[0]}:{client_address[1]}: {message}")
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

    with lock:
        if sender_key in peers:
            del peers[sender_key]
        if client_socket in client_sockets:
            client_sockets.remove(client_socket)
        client_socket.close()
        print(f"Connection closed with {client_address[0]}:{client_address[1]}")

def send_message():
    """Send a message to a specific peer."""
    ip = input("Enter peer IP: ")
    port = int(input("Enter peer port: "))
    message = input("Enter message: ")

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        client_socket.send(message.encode('utf-8'))
        with lock:
            peers[f"{ip}:{port}"] = client_socket
        print(f"Message sent to {ip}:{port}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def broadcast_message():
    """Broadcast a message to all connected peers."""
    message = input("Enter broadcast message: ")
    with lock:
        for peer, sock in list(peers.items()):
            try:
                sock.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Failed to send message to {peer}: {e}")

def query_peers():
    """Display the list of active peers."""
    with lock:
        if not peers:
            print("No active peers.")
        else:
            print("Active peers:")
            for peer in peers:
                print(peer)

def connect_to_peer():
    """Connect to an active peer and send a connection message."""
    ip = input("Enter peer IP: ")
    port = int(input("Enter peer port: "))

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        client_socket.send("Connection established".encode('utf-8'))
        with lock:
            peers[f"{ip}:{port}"] = client_socket
            client_sockets.append(client_socket)
        print(f"Connected to {ip}:{port}")
    except Exception as e:
        print(f"Failed to connect: {e}")

def disconnect_from_peer():
    """Disconnect from a specific peer."""
    ip = input("Enter peer IP to disconnect: ")
    port = int(input("Enter peer port to disconnect: "))
    peer_key = f"{ip}:{port}"

    with lock:
        if peer_key in peers:
            try:
                peers[peer_key].close()
                client_sockets.remove(peers[peer_key])
                del peers[peer_key]
                print(f"Disconnected from {peer_key}")
            except Exception as e:
                print(f"Failed to disconnect from {peer_key}: {e}")
        else:
            print(f"No active connection to {peer_key}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python p2p_chat.py <your_name> <your_port>")
        return

    name = sys.argv[1]
    port = int(sys.argv[2])

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()

    # Mandatory connections
    mandatory_peers = [("127.0.0.1", 5000)]
    for ip, port in mandatory_peers:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            client_socket.send(f"Connection from {name}".encode('utf-8'))
            with lock:
                peers[f"{ip}:{port}"] = client_socket
                client_sockets.append(client_socket)
            print(f"Connected to mandatory peer {ip}:{port}")
        except Exception as e:
            print(f"Failed to connect to mandatory peer {ip}:{port}: {e}")

    # Menu
    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Broadcast message")
        print("3. Query active peers")
        print("4. Connect to active peers")
        print("5. Disconnect from a peer")
        print("0. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            send_message()
        elif choice == "2":
            broadcast_message()
        elif choice == "3":
            query_peers()
        elif choice == "4":
            connect_to_peer()
        elif choice == "5":
            disconnect_from_peer()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

    # Cleanup
    with lock:
        for client_socket in client_sockets:
            client_socket.close()
        if server_socket:
            server_socket.close()
    print("Application shut down gracefully.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down...")
        with lock:
            for client_socket in client_sockets:
                client_socket.close()
            if server_socket:
                server_socket.close()
        sys.exit(0)
