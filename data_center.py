import streamlit as st
import socket
import struct

st.title('UDP Data Hub')
st.write('Received Messages:')

UDP_IP = "66.179.241.81"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Create an empty list to hold packet data
packet_data = []

# Function to decode packet
def decode_packet(data):
    # Define the structure of the packet: 6 int16_t values + 4 int values
    # 'h' for int16_t (2 bytes) and 'i' for int (4 bytes)
    format_string = '6h4i'  # 6 int16_t (h) and 4 int (i)
    
    # Unpack the data based on the format
    decoded_values = struct.unpack(format_string, data)
    
    return decoded_values

while True:
    # Receive data (choose a buffer size that matches the data you're receiving)
    data, addr = sock.recvfrom(28)  
    # Show received packet information in Streamlit (replaces print)
    st.write(f"Received packet from {addr}")
    
    # Decode the packet
    decoded_values = decode_packet(data)
    
    # Show decoded values in Streamlit (replaces print)
    st.write(f"Decoded values: {decoded_values}")

    # Optionally, you can store the decoded values in a list to display in a table
    packet_data.append(decoded_values)

    # Show the last few packets in a table
    if packet_data:
        st.subheader("Decoded Packet Values")
        st.dataframe(packet_data)

        
        