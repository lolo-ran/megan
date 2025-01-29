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
    # Receive data (choose a buffer size that matches the data you're receiving)
    data, addr = sock.recvfrom(1024)  # 1024 bytes buffer size (adjust as needed)
    st.write(data)
        
        