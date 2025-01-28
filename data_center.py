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
    if len(data) >= 40:  # Check if we have enough data (10 floats * 4 bytes each = 40 bytes)
        # Unpack the entire packet
        values = struct.unpack('<10f', data[:40])  # Unpack 10 floats from the first 40 bytes
        
        # Displaying each value (you can store them in variables or display as needed)
        st.write("Accelerometer (Gs):", values[0], values[1], values[2])
        st.write("Gyroscope (°/s):", values[3], values[4], values[5])
        st.write("Voltages (V):", values[6], values[7], values[8], values[9])
