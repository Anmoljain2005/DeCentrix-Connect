# DeCentrix P2P Chat Application

A peer-to-peer chat application built with Python that enables direct communication between multiple users across a network. The application supports both local testing with multiple terminals and deployment across different computers on a network.

## Features

- Direct messaging between peers
- Broadcasting messages to all connected peers
- Real-time peer discovery and connection management
- Support for mandatory message forwarding to specified peers
- Thread-safe operations for concurrent message handling
- Simple command-line interface with emoji feedback

## Prerequisites

- Python 3.x
- Basic understanding of networking concepts
- Knowledge of your system's IP address and available ports

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Anmoljain2005/DeCentrix-Connect.git
cd decentrix-chat
```

2. No additional dependencies are required as the application uses Python's standard library.

## Usage

### Local Testing (Multiple Terminals)

1. Open 3-4 terminal windows
2. In each terminal, run:
```bash
python p2p_chat.py
```
3. For local testing, use:
   - IP Address: `127.0.0.1`
   - Different port numbers for each instance (e.g., 5001, 5002, 5003)
4. Use the menu options to send messages between the instances

### Network Deployment (Multiple Computers)

#### Windows Firewall Configuration

Before running the application across different computers, configure the Windows Firewall:

1. Open Windows Firewall Settings:
   - Press Windows key + R
   - Type "wf.msc" and press Enter
   OR
   - Go to Control Panel → System and Security → Windows Defender Firewall

2. Create Inbound Rule for Python:
   - Click "Inbound Rules" → "New Rule..."
   - Select "Program"
   - Browse to Python executable (typically `C:\Users\YourUsername\AppData\Local\Programs\Python\Python3x\python.exe`)
   - Select "Allow the connection"
   - Check all network types (Domain, Private, Public)
   - Name the rule (e.g., "Python Chat Application")

3. Create Outbound Rule:
   - Repeat the above steps in "Outbound Rules"

#### Running the Application

1. On each computer:
   - Find your IP address:
     ```bash
     # Windows
     ipconfig
     
     # Linux/Mac
     ifconfig
     ```
   - Run the application:
     ```bash
     python p2p_chat.py
     ```
   - Enter your computer's IP address and a port number (e.g., 5001)

2. To connect to other peers:
   - Use option 1 to send direct messages
   - Use option 3 to connect to known peers
   - Use option 4 to broadcast messages

## Menu Options

1. **Send Message**: Send a direct message to a specific peer
2. **Query Active Peers**: View list of known peers and their connection status
3. **Connect to Peers**: Establish connections with known peers
4. **Broadcast Message**: Send a message to all connected peers
5. **Disconnect from Peer**: Remove connection with a specific peer
0. **Quit**: Exit the application

## Configuration

- `TEAM_NAME`: Set your team identifier in the code
- `MANDATORY_PEERS`: Configure IP:Port pairs that should receive copies of all messages

## Troubleshooting

1. **Connection Refused**:
   - Verify the target IP and port are correct
   - Ensure the target application is running
   - Check firewall settings

2. **Address Already in Use**:
   - Choose a different port number
   - Wait a few minutes for the previous connection to timeout
   - Check if another application is using the port

## Acknowledgments
- This Network Coding Assignment is a part of the course CS-216 Introduction to Blockchain under the guidance of Dr. Subhra Mazumdar.

---
