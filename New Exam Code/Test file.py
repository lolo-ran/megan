import tkinter as tk
from tkinter import ttk

def co_movements():
    # Define movement instructions
    R_L_movements = [
        {"name": "Raise", "description": "Raise your hand and tap your nose, "
        "return it to your side afterwards"},
        {"name": "Lift", "description": "Raise your hand and tap your head,"
        " return it to your sides afterwards"},
        {"name": "Circle", "description": "Draw a circle in the air with your hand,"
        " then return it to the center of your chest"}
    ]

    Bilateral_movements = [
        {"name": "Clock Creation", "description": "Use both hands to mimic drawing a clock face in the air, "
        "starting from the center and moving outward"},
        {"name": "Clock Replication", "description": "Using both hands, replicate the position of clock hands for a given time, "
        "starting from the center of your chest"},
        {"name": "Taichi", "description": "Perform a slow, flowing movement using both arms simultaneously, "
        "maintaining balance and fluidity"},
        {"name": "Tap Nose", "description": "Raise both hands and tap your nose simultaneously, "
        "returning hands to your sides after each tap"}
    ]

    # GUI setup
    root = tk.Tk()
    root.title("Coordinated Movement Instructions")
    root.configure(bg="#f0f0f0")

    # Title label
    title_label = tk.Label(root, text="Please perform the following movements:", font=("Segoe UI", 14, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    # Display R/L Movements
    rl_frame = ttk.LabelFrame(root, text="Right/Left Hand Movements")
    rl_frame.pack(padx=10, pady=5, fill="both", expand=True)
    for idx, movement in enumerate(R_L_movements, start=1):
        label = tk.Label(rl_frame, text=f"{idx}. {movement['name']}: {movement['description']}", font=("Segoe UI", 12), anchor="w", justify="left")
        label.pack(anchor="w", padx=10, pady=2)

    # Display Bilateral Movements
    bi_frame = ttk.LabelFrame(root, text="Bilateral Movements")
    bi_frame.pack(padx=10, pady=5, fill="both", expand=True)
    for idx, movement in enumerate(Bilateral_movements, start=1):
        label = tk.Label(bi_frame, text=f"{idx}. {movement['name']}: {movement['description']}", font=("Segoe UI", 12), anchor="w", justify="left")
        label.pack(anchor="w", padx=10, pady=2)

    root.mainloop()

co_movements()
