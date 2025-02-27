import streamlit as st
import socket
import struct
import csv
from datetime import datetime

st.title('UDP Data Hub')

# SET UP UDP SOCKET
UDP_IP = "66.179.241.81"
UDP_PORT = 5005
sock = None

# Initialize session state for logging control
if 'logging' not in st.session_state:
    st.session_state.logging = False

# Open CSV file in append mode, create if not exists
csv_filename = "sensor_data.csv"

# Button to start logging data
if st.button("Start Logging"):
    if not st.session_state.logging:
        if sock == None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable address reuse
            sock.bind((UDP_IP, UDP_PORT))
        st.session_state.logging = True
        st.success("Logging started.")
    else:
        st.warning("Logging already started.")

# Button to stop logging data
if st.button("Stop Logging"):
    if st.session_state.logging:
        st.session_state.logging = False
        st.success("Logging stopped.")
    else:
        st.warning("No logging in process.")

if st.session_state.logging:
    # Open CSV file in append mode, create if not exists
    with open(csv_filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
            
        # Write header if file is empty (to avoid duplicate headers)
        if csv_file.tell() == 0:
            csv_writer.writerow([
                "timestamp", "x_accel", "y_accel", "z_accel", "x_gyro", "y_gyro", "z_gyro", "x_mag", "y_mag", "z_mag",
                "read_1_0", "read_1_1", "read_1_2", "read_1_3", "read_1_4", "read_1_5", "read_1_6", "read_1_7",
                "read_2_0", "read_2_1", "read_2_2", "read_2_3", "read_2_4", "read_2_5", "read_2_6", "read_2_7",
                "read_3_0", "read_3_1", "read_3_2", "read_3_3", "read_3_4", "read_3_5", "read_3_6", "read_3_7"
            ])
    
        # Receive data (choose a buffer size that matches the data you're receiving)
        data, addr = sock.recvfrom(114)  
        
        while st.session_state.logging:
            if len(data) == 114:
                st.write(f"Received packet from {addr}")
                    
                # Unpack the data (we know the structure: 9 int16_t and 24 int)
                # First unpack the 2-byte int16_t values (9 values = 18 bytes)
                x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro, x_mag, y_mag, z_mag = struct.unpack('<9h', data[:18])
                # Then unpack the 4-byte int values (24 values = 96 bytes)
                read_1_0, read_1_1, read_1_2, read_1_3, read_1_4, read_1_5, read_1_6, read_1_7, read_2_0, read_2_1, read_2_2, read_2_3, read_2_4, read_2_5, read_2_6, read_2_7, read_3_0, read_3_1, read_3_2, read_3_3, read_3_4, read_3_5, read_3_6, read_3_7 = struct.unpack('<24i', data[18:])
            
                # Get current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
                # Write to CSV file
                csv_writer.writerow([timestamp, x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro, x_mag, y_mag, z_mag, read_1_0, read_1_1, read_1_2, read_1_3, read_1_4, read_1_5, read_1_6, read_1_7, read_2_0, read_2_1, read_2_2, read_2_3, read_2_4, read_2_5, read_2_6, read_2_7, read_3_0, read_3_1, read_3_2, read_3_3, read_3_4, read_3_5, read_3_6, read_3_7])
            else:
                st.write("Received packet of incorrect size")

    sock.close()
    sock = None
