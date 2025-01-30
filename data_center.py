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
    data, addr = sock.recvfrom(28)  
    
    if len(data) == 94:
        st.write(f"Received packet from {addr}")
        
        # Unpack the data (we know the structure: 6 int16_t and 24 int)
        # First unpack the 2-byte int16_t values (6 values)
        x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro = struct.unpack('<6h', data[:12])
        # Then unpack the 4-byte int values (24 values)
        read_1_0, read_1_1, read_1_2, read_1_3, read_1_4, read_1_5, read_1_6, read_1_7, read_2_0, read_2_1, read_2_2, read_2_3, read_2_4, read_2_5, read_2_6, read_2_7, read_3_0, read_3_1, read_3_2, read_3_3, read_3_4, read_3_5, read_3_6, read_3_7 = struct.unpack('<24i', data[12:])
        
        # Print the unpacked data (you can process it as needed)
        st.write(f"x_accel: {x_accel}, y_accel: {y_accel}, z_accel: {z_accel}")
        st.write(f"x_gyro: {x_gyro}, y_gyro: {y_gyro}, z_gyro: {z_gyro}")
        st.write(f"read_1_0: {read_1_0}, read_1_1: {read_1_1}, read_1_2: {read_1_2}, read_1_3: {read_1_3}, read_1_4: {read_1_4}, read_1_5: {read_1_5}, read_1_6: {read_1_6}, read_1_7: {read_1_7}")
        st.write(f"read_2_0: {read_2_0}, read_2_1: {read_2_1}, read_2_2: {read_2_2}, read_2_3: {read_2_3}, read_2_4: {read_2_4}, read_2_5: {read_2_5}, read_2_6: {read_2_6}, read_2_7: {read_2_7}")
        st.write(f"read_3_0: {read_3_0}, read_3_1: {read_3_1}, read_3_2: {read_3_2}, read_3_3: {read_3_3}, read_3_4: {read_3_4}, read_3_5: {read_3_5}, read_3_6: {read_3_6}, read_3_7: {read_3_7}")
    else:
        st.write("Received packet of incorrect size")
