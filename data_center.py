import streamlit as st
import socket

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
            st.session_state.received_data = received_float

# Start the UDP listener in a separate thread
if 'received_data' not in st.session_state:
    st.session_state.received_data = None  # Initialize session state variable

# Start the UDP listener thread
if 'listener_thread' not in st.session_state:
    listener_thread = threading.Thread(target=udp_listener, daemon=True)
    listener_thread.start()

# Show the received data
if st.session_state.received_data is not None:
    st.write(f"Received Float: {st.session_state.received_data}")
else:
    st.write("Waiting for data...")

# Keep the Streamlit app alive
while True:
    time.sleep(1)  # Sleep to avoid blocking the app
