import socket
import threading

# Dictionary to store known peers: {(IP, Port): "Peer Name"}
peer_list = {}
connected_peers = set()

# Threading lock for thread-safe access to shared resources
lock = threading.Lock()

# Fixed team name for this peer
TEAM_NAME = "DeCentrix"

# Mandatory IP and Port pairs to send messages to 
# MANDATORY_PEERS = [("10.206.4.122", 1255), ("10.206.5.228", 6555)]
MANDATORY_PEERS = []


def receive_messages(server_socket):
    """
    Listens for incoming messages from other peers and updates the peer list.
    """
    while True:
        try:
            # Accept a connection from a peer
            client, addr = server_socket.accept()
            message = client.recv(1024).decode()

            # Parse the message according to the standardized format
            try:
                sender_info, team_name, actual_message = message.split(" ", 2)
                sender_ip, sender_port = sender_info.split(":")
                sender_port = int(sender_port)

                # Add the sender to the peer list if not already present
                with lock:
                    if (sender_ip, sender_port) not in peer_list:
                        peer_list[(sender_ip, sender_port)] = team_name

                # Display the received message
                print(f"\n📩 Message from {sender_ip}:{sender_port} ({team_name}) → {actual_message}")
            except Exception as e:
                print("\n⚠️ Received malformed message:", message)
                print("Error:", e)

            # Close the connection
            client.close()
        except Exception as e:
            print("\n🚨 Error in receiving messages:", e)
            break


def send_messages(my_ip, my_port):
    """
    Handles sending messages to other peers and managing peer connections.
    """
    while True:
        # Display the menu
        print("\n" + "=" * 30)
        print("1. Send Message")
        print("2. Query Active Peers")
        print("3. Connect to Peers")
        print("4. Broadcast Message")
        print("5. Disconnect from Peer")
        print("0. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Send a message to a specific peer
            target_ip = input("Enter recipient's IP address: ")
            target_port = int(input("Enter recipient's port number: "))
            message = input("Enter your message: ")

            # Standardize the message format
            formatted_message = f"{my_ip}:{my_port} {TEAM_NAME} {message}"

            # Send the message to the target peer
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((target_ip, target_port))
                client.send(formatted_message.encode())
                print("✅ Message sent!")
            except Exception as e:
                print(f"❌ Connection failed: {e}")
            finally:
                client.close()

            # Send the same message to mandatory peers
            for ip, port in MANDATORY_PEERS:
                if (ip, port) != (my_ip, my_port):  # Avoid sending to self
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        client.connect((ip, port))
                        client.send(formatted_message.encode())
                        print(f"✅ Message sent to mandatory peer {ip}:{port}!")
                    except Exception as e:
                        print(f"❌ Failed to send message to mandatory peer {ip}:{port}: {e}")
                    finally:
                        client.close()

        elif choice == "2":
            # Display the list of active peers
            print("\n📜 Active Peers:")
            with lock:
                if peer_list:
                    for (ip, port), name in peer_list.items():
                        connection_status = " (Connected)" if (ip, port) in connected_peers else ""
                        print(f"🔗 {name} → {ip}:{port}{connection_status}")
                else:
                    print("No active peers yet.")

        elif choice == "3":
            # Connect to known peers
            print("\n🔗 Connecting to known peers...")
            with lock:
                for (ip, port) in peer_list.keys():
                    if (ip, port) not in connected_peers:
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        try:
                            client.connect((ip, port))
                            client.send(f"{my_ip}:{my_port} {TEAM_NAME} Hello, I am connecting!".encode())
                            connected_peers.add((ip, port))
                            print(f"✅ Connected to {ip}:{port}")
                        except Exception as e:
                            print(f"❌ Failed to connect to {ip}:{port}: {e}")
                        finally:
                            client.close()

        elif choice == "4":
            # Broadcast a message to all connected peers
            message = input("Enter your broadcast message: ")
            formatted_message = f"{my_ip}:{my_port} {TEAM_NAME} {message}"

            with lock:
                for (ip, port) in connected_peers:
                    if (ip, port) != (my_ip, my_port):  # Avoid sending to self
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        try:
                            client.connect((ip, port))
                            client.send(formatted_message.encode())
                            print(f"✅ Broadcast sent to {ip}:{port}!")
                        except Exception as e:
                            print(f"❌ Failed to send broadcast to {ip}:{port}: {e}")
                        finally:
                            client.close()

        elif choice == "5":
            # Disconnect from a specific peer
            target_ip = input("Enter peer's IP address to disconnect: ")
            target_port = int(input("Enter peer's port number to disconnect: "))

            with lock:
                if (target_ip, target_port) in connected_peers:
                    connected_peers.remove((target_ip, target_port))
                    print(f"🔌 Disconnected from {target_ip}:{target_port}")
                else:
                    print(f"⚠️ No active connection to {target_ip}:{target_port}")

        elif choice == "0":
            # Exit the program
            print("👋 Exiting chat. Goodbye!")
            break

        else:
            print("❌ Invalid choice! Please enter 1, 2, 3, 4, 5, or 0.")


def main():
    """
    Main function to start the peer-to-peer chat application.
    """
    # Get the IP address and port from the user
    my_ip = input("Enter your IP address: ")
    my_port = int(input("Enter your port number: "))

    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((my_ip, my_port))
    server_socket.listen(5)
    print(f"\n🚀 Server is listening on {my_ip}:{my_port}")

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(server_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    # Start the message sending function in the main thread
    send_messages(my_ip, my_port)


# Run the chat application
if __name__ == "__main__":
    main()
