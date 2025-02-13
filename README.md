# Peer-to-Peer (P2P) Chat Application

## Overview
This Peer-to-Peer Chat Application is a Python-based program that facilitates direct communication between connected peers in a network. The application enables features like sending direct messages, broadcasting messages to all connected peers, managing peer connections, and querying active peers.

## Features
1. **Start a Local Server**: Hosts a TCP server that listens for incoming connections.
2. **Dynamic Peer Management**: Automatically adds peers upon connection and removes them upon disconnection.
3. **Send Messages**: Send a message to a specific peer by providing their IP and port.
4. **Broadcast Messages**: Send a message to all connected peers simultaneously.
5. **Query Active Peers**: View a list of all currently connected peers.
6. **Connect to New Peers**: Initiate connections to other peers manually.
7. **Disconnect from Peers**: Gracefully close the connection to a specific peer.
8. **Mandatory Peer Connections**: Connects to predefined peers on startup.

---

## Installation

### Prerequisites
- Python 3.7 or later

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/p2p-chat.git
   cd p2p-chat
   ```
2. Install any necessary Python packages (if applicable). For standard libraries, no extra dependencies are required.
3. Run the script:
   ```bash
   python p2p_chat.py <your_name> <your_port>
   ```
   Replace `<your_name>` with your identifier and `<your_port>` with the port number you want the server to run on.

---

## How to Use

### Starting the Application
Run the application using the command:
```bash
python p2p_chat.py <your_name> <your_port>
```

### Main Menu Options
1. **Send Message**
   - Input the IP and port of the target peer.
   - Type the message to send.
2. **Broadcast Message**
   - Type the message to broadcast to all connected peers.
3. **Query Active Peers**
   - Displays the list of all currently connected peers.
4. **Connect to a Peer**
   - Input the IP and port of the peer to establish a connection.
   - Automatically sends a connection confirmation message.
5. **Disconnect from a Peer**
   - Input the IP and port of the peer to disconnect.
6. **Quit**
   - Exits the application and closes all active connections.

---

## Code Explanation

### Modules
- **socket**: Manages TCP socket communication.
- **threading**: Handles concurrent threads for server and client operations.
- **sys**: Processes command-line arguments.

### Key Components
1. **Server**:
   - Starts a local TCP server on a user-specified port.
   - Listens for incoming connections and spawns threads to handle each client.
2. **Client**:
   - Enables outgoing connections to peers.
   - Sends and receives messages over established TCP connections.
3. **Thread-Safe Operations**:
   - Uses a threading lock to ensure synchronized access to shared resources like `peers` and `client_sockets`.

---

## Example Usage
1. Start the server on one machine:
   ```bash
   python p2p_chat.py Alice 5000
   ```
   Output:
   ```
   Server listening on port 5000
   ```

2. Connect from another machine:
   ```bash
   python p2p_chat.py Bob 5001
   ```
   Use the menu to connect to Alice's server:
   ```
   Enter peer IP: 127.0.0.1
   Enter peer port: 5000
   ```

3. Send a message from Bob to Alice:
   ```
   Enter peer IP: 127.0.0.1
   Enter peer port: 5000
   Enter message: Hello, Alice!
   ```

4. Alice receives:
   ```
   Received from 127.0.0.1:5001: Hello, Alice!
   ```

---

## Notes
- Mandatory peers can be configured in the `main()` function by modifying the `mandatory_peers` list.
- If a peer disconnects unexpectedly, the application automatically cleans up resources.
- Message size is currently limited to 1024 bytes. This can be adjusted in the `recv` method.

---



## Acknowledgments
- This Network Coding Assignment is a part of the course CS216 Introduction to Blockchain under the guidance of Dr. Subhra Mazumdar.

---
.

