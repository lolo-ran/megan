import streamlit as st
import socket
import struct

st.title('UDP Data Hub')
st.write('Received Messages:')

UDP_IP = "66.179.241.81"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if len(data) >= 4:
        received_float = struct.unpack('<f', data[:4])[0]  # <f for little-endian float
        # Store the value in Streamlit's session state to persist across reruns
        st.write(received_float)
