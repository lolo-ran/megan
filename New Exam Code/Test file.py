import numpy as np
import tkinter as tk
from tkinter import ttk
import time
from PIL import Image, ImageTk

def calculate_score(is_correct):
    return 4 if is_correct else 0

def odd_one_out_test():

    # GUI setup
    root = tk.Tk()
    root.title("Odd One Out Test")
    root.configure(bg="#f5f5f5")

    style = ttk.Style()
    style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 14))

    # Load images
    image_paths = [
        "test_1.jpg",
        "test_2.png",  # This is the odd one
        "test_3.png",
        "test_4.png"
    ]
    images = [Image.open(path).resize((120, 120)) for path in image_paths]
    photo_images = [ImageTk.PhotoImage(img) for img in images]

    # Fixed image order
    fixed_indices = [0, 1, 2, 3]
    odd_one_index = 1  # test_2.png is the odd one

    # Track result
    result_data = {
        "selected_index": None,
        "correct_index": odd_one_index,
        "start_time": time.time(),
        "end_time": None
    }

    ttk.Label(root, text="Click on the odd one out!").pack(pady=10)

    frame = ttk.Frame(root)
    frame.pack(pady=10)

    def on_image_click(index):
        result_data["selected_index"] = index
        result_data["end_time"] = time.time()

        is_correct = index == result_data["correct_index"]
        score = calculate_score(is_correct)
        duration = result_data["end_time"] - result_data["start_time"]

        # Close the GUI
        root.destroy()

        # Output
        print("\n=== ODD ONE OUT TEST SUMMARY ===")
        print(f"Correct image index: {result_data['correct_index']}")
        print(f"Selected image index: {result_data['selected_index']}")
        print(f"Time taken: {duration:.2f} seconds")
        print(f"Correct: {'Yes' if is_correct else 'No'}")
        print(f"Clinician Score (0–4): {score}")

        with open("odd_one_out_results.txt", "a") as f:
            f.write("=== ODD ONE OUT TEST SUMMARY ===\n")
            f.write(f"Correct image index: {result_data['correct_index']}\n")
            f.write(f"Selected image index: {result_data['selected_index']}\n")
            f.write(f"Time taken: {duration:.2f} seconds\n")
            f.write(f"Correct: {'Yes' if is_correct else 'No'}\n")
            f.write(f"Clinician Score (0–4): {score}\n\n")

    # Display images
    for i, idx in enumerate(fixed_indices):
        button = ttk.Button(
            frame,
            image=photo_images[idx],
            command=lambda index=idx: on_image_click(index)
        )
        button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()

# Run the test
odd_one_out_test()
