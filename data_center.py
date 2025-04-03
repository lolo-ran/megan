import streamlit as st
import socket
import struct
import csv
from datetime import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Live Sensor Dashboard", layout="wide")
st.title("🔴 Live Sensor Dashboard")

# UDP Configuration
UDP_IP = "66.179.241.81"
UDP_PORT = 5005
BUFFER_SIZE = 114
CSV_FILE = "sensor_data.csv"
WINDOW_SIZE = 100

# Initialize session state
if "sock" not in st.session_state:
    st.session_state.sock = None
if "data_buffer" not in st.session_state:
    st.session_state.data_buffer = []
if "chart_data" not in st.session_state:
    st.session_state.chart_data = {
        "timestamps": [],
        "x_accel": [],
        "y_accel": [],
        "z_accel": [],
    }
if "logging" not in st.session_state:
    st.session_state.logging = False

# Sidebar for export
with st.sidebar:
    st.subheader("📤 Export")
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r") as f:
            st.download_button("Download CSV Log", data=f, file_name=CSV_FILE, mime="text/csv")
    else:
        st.info("No CSV file available yet.")

# Start / Stop buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Logging"):
        if not st.session_state.logging:
            st.session_state.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            st.session_state.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            st.session_state.sock.settimeout(0.1)
            st.session_state.sock.bind((UDP_IP, UDP_PORT))
            st.session_state.logging = True
            st.success("✅ Logging started.")

with col2:
    if st.button("⏹ Stop Logging"):
        if st.session_state.logging:
            st.session_state.logging = False
            if st.session_state.sock:
                st.session_state.sock.close()
                st.session_state.sock = None
            st.success("🛑 Logging stopped.")

# Live sensor display placeholders
accel_display = st.empty()
gyro_display = st.empty()
mag_display = st.empty()
grid_display = st.empty()
chart_display = st.empty()

# Data reading function
def read_udp_data():
    try:
        data, addr = st.session_state.sock.recvfrom(BUFFER_SIZE)
        if len(data) != BUFFER_SIZE:
            return

        # Unpack data
        x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro, x_mag, y_mag, z_mag = struct.unpack('<9h', data[:18])
        readings = struct.unpack('<24i', data[18:])
        row1 = readings[0:8]
        row2 = readings[8:16]
        row3 = readings[16:24]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append to CSV
        write_header = not os.path.exists(CSV_FILE)
        with open(CSV_FILE, mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            if write_header:
                csv_writer.writerow(
                    ["timestamp", "x_accel", "y_accel", "z_accel", "x_gyro", "y_gyro", "z_gyro",
                     "x_mag", "y_mag", "z_mag"] + [f"read_{i//8+1}_{i%8}" for i in range(24)]
                )
            csv_writer.writerow([timestamp, x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro,
                                 x_mag, y_mag, z_mag] + list(readings))

        # Update session chart data
        chart = st.session_state.chart_data
        chart["timestamps"].append(timestamp)
        chart["x_accel"].append(x_accel)
        chart["y_accel"].append(y_accel)
        chart["z_accel"].append(z_accel)

        for key in chart:
            chart[key] = chart[key][-WINDOW_SIZE:]

        # Display live values
        accel_display.markdown(f"**Accelerometer**: X: `{x_accel}` Y: `{y_accel}` Z: `{z_accel}`")
        gyro_display.markdown(f"**Gyroscope**: X: `{x_gyro}` Y: `{y_gyro}` Z: `{z_gyro}`")
        mag_display.markdown(f"**Magnetometer**: X: `{x_mag}` Y: `{y_mag}` Z: `{z_mag}`")
        grid_display.markdown(f"**Sensor Grid:**\n\n`{row1}`\n\n`{row2}`\n\n`{row3}`")

    except socket.timeout:
        pass
    except Exception as e:
        st.error(f"UDP read error: {e}")

# Run reader loop briefly on each rerun
if st.session_state.logging and st.session_state.sock:
    for _ in range(5):  # read a few packets per rerun
        read_udp_data()

    # Show chart
    df = pd.DataFrame({
        "Timestamp": st.session_state.chart_data["timestamps"],
        "X": st.session_state.chart_data["x_accel"],
        "Y": st.session_state.chart_data["y_accel"],
        "Z": st.session_state.chart_data["z_accel"],
    })

    if not df.empty:
        fig, ax = plt.subplots()
        ax.plot(df["Timestamp"], df["X"], label="X Accel")
        ax.plot(df["Timestamp"], df["Y"], label="Y Accel")
        ax.plot(df["Timestamp"], df["Z"], label="Z Accel")
        ax.legend()
        ax.set_title("Accelerometer - Live")
        ax.tick_params(axis='x', rotation=45)
        chart_display.pyplot(fig)

    # Auto-refresh
    time.sleep(0.2)
    st.rerun()
