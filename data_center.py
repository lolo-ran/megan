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
    st.write(f"Received data from {addr}: {data.hex()}")  # Print raw data in hex for debugging
    if len(data) >= 28:  # Ensure enough bytes for 6 int16_t + 4 int values (6 * 2 bytes + 4 * 4 bytes = 28 bytes)
        try:
            # Unpack 6 int16_t values (each 2 bytes)
            accelerometer_gyro_data = struct.unpack('<6h', data[:12])  # Little-endian, 6 int16_t values
            
            # Unpack 4 int values (4 bytes each)
            voltage_data = struct.unpack('<4i', data[12:28])  # Little-endian, 4 int values (32-bit)

            # Extract individual values
            x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro = accelerometer_gyro_data
            read_1_0, read_1_1, read_2_0, read_2_1 = voltage_data

            # Now process these values as needed
            st.write("Accelerometer (Gs):", 2.0 * x_accel / 32768.0, 2.0 * y_accel / 32768.0, 2.0 * z_accel / 32768.0)
            st.write("Gyroscope (°/s):", 250.0 * x_gyro / 32768.0, 250.0 * y_gyro / 32768.0, 250.0 * z_gyro / 32768.0)
            st.write("Voltages (V):", 3.3 * read_1_0 / 4096.0, 3.3 * read_1_1 / 4096.0, 3.3 * read_2_0 / 4096.0, 3.3 * read_2_1 / 4096.0)
        except Exception as e:
            st.write(f"Error unpacking data: {e}")
    else:
        st.write("Received data is too short to unpack.")