import socket
import struct

UDP_IP = "66.179.241.81"  # Same as in Streamlit
UDP_PORT = 5005
BUFFER_SIZE = 114

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print(f"Received {len(data)} bytes from {addr}")
