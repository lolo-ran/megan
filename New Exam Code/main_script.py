import numpy as np
import random
import tkinter as tk
from tkinter import ttk
import time
from tkinter import messagebox
from PIL import Image, ImageTk
#Leaving this segment for when we want to import new code spaces

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




def wait_for_start(test_number):
    start_input = input(f"Type 'Start test {test_number}' to begin: ")
    while start_input.strip().lower() != f"start test {test_number}":
        print("Incorrect input. Try again.")
        start_input = input(f"Type 'Start test {test_number}' to begin: ")

def recall_test():
    wait_for_start(1)

    letters = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 5)
    numbers = random.sample(range(10), 3)
    jumbled = letters + list(map(str, numbers))
    random.shuffle(jumbled)

    correct_order = sorted(jumbled, key=lambda x: (x.isdigit(), x.upper()))
    numbered_items = {item: str(i + 1) for i, item in enumerate(jumbled)}

    root = tk.Tk()
    root.title("Recall Test")
    root.configure(bg="#f5f5f5")

    default_font = ("Segoe UI", 14)
    small_font = ("Segoe UI", 12)

    style = ttk.Style()
    style.configure("TButton", font=default_font, padding=6)
    style.configure("TLabel", background="#f5f5f5", font=default_font)

    ttk.Label(root, text="Select the characters in ascending order (A–Z, then 0–9):").pack(pady=20)
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=20)

    selected_order = []
    final_results = {
        "score": None,
        "accuracy": None,
        "correct_count": None,
        "selected_order": [],
        "correct_order": correct_order
    }

    feedback_label = ttk.Label(root, text="", font=("Segoe UI", 14))
    feedback_label.pack(pady=10)

    def calculate_score(accuracy):
        if accuracy == 100:
            return 0
        elif accuracy >= 90:
            return 1
        elif accuracy >= 70:
            return 2
        elif accuracy >= 40:
            return 3
        else:
            return 4

    def select_item(item, button):
        if item not in selected_order and len(selected_order) < len(correct_order):
            selected_order.append(item)
            button.state(["disabled"])

            if len(selected_order) == len(correct_order):
                check_result()

    def check_result():
        correct_count = sum(1 for i, item in enumerate(selected_order) if item == correct_order[i])
        accuracy = (correct_count / len(correct_order)) * 100
        score = calculate_score(accuracy)

        final_results["score"] = score
        final_results["accuracy"] = accuracy
        final_results["correct_count"] = correct_count
        final_results["selected_order"] = selected_order.copy()

        feedback_label.config(text=f"Test complete. Thank you!", foreground="blue")
        root.after(3000, root.destroy)

    for item in jumbled:
        item_frame = ttk.Frame(button_frame)
        item_frame.pack(side=tk.LEFT, padx=12, pady=8)

        button = ttk.Button(item_frame, text=item)
        button.pack()
        button.config(command=lambda i=item, b=button: select_item(i, b))

        label = ttk.Label(item_frame, text=numbered_items[item], font=small_font)
        label.pack()

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.mainloop()

    return final_results

# Run the test
results = recall_test()

# Output for physician
print("\n=== RECALL TEST SUMMARY ===")
print(f"Entered order: {' '.join(results['selected_order'])}")
print(f"Correct order: {' '.join(results['correct_order'])}")
print(f"Accuracy: {results['accuracy']:.2f}%")
print(f"Correct selections: {results['correct_count']}/8")
print(f"Clinician Score (0–4): {results['score']}")

# Save to file
with open("New Exam Code/recall_results.txt", "a") as f:
    f.write("=== RECALL TEST SUMMARY ===\n")
    f.write(f"Entered order: {' '.join(results['selected_order'])}\n")
    f.write(f"Correct order: {' '.join(results['correct_order'])}\n")
    f.write(f"Accuracy: {results['accuracy']:.2f}%\n")
    f.write(f"Correct selections: {results['correct_count']}/8\n")
    f.write(f"Clinician Score (0–4): {results['score']}\n\n")



def wait_for_start(test_number):
    start_input = input(f"Type 'Start test {test_number}' to begin: ")
    while start_input.strip().lower() != f"start test {test_number}":
        print("Incorrect input. Try again.")
        start_input = input(f"Type 'Start test {test_number}' to begin: ")

def calculate_score(accuracy):
    if accuracy >= 90:
        return 0
    elif accuracy >= 80:
        return 1
    elif accuracy >= 60:
        return 2
    elif accuracy >= 40:
        return 3
    else:
        return 4

def stroop_test():
    wait_for_start(2)

    # GUI setup
    root = tk.Tk()
    root.title("Stroop Test")
    root.configure(bg="#f5f5f5")

    style = ttk.Style()
    style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 14))
    style.configure("TButton", font=("Segoe UI", 14), padding=6)

    # Define color mappings
    colors = ["RED", "BLUE", "GREEN", "BROWN"]
    text_colors = {"GREEN":"green", "RED": "red", "BLUE": "blue", "BROWN": "brown"}
    color_keys = {"g": "green", "r": "red", "b": "blue", "n": "brown"}

    # State
    test_data = {
        "current_phase": 0,  # 0 = matching, 1 = mismatching
        "current_word": "",
        "current_color": "",
        "score": 0,
        "total_attempts": 0,
        "start_time": None
    }

    correct_colors = []
    selected_colors = []

    # GUI elements
    instructions = ttk.Label(root, text="Say the COLOR of the text, not the word!")
    instructions.pack(pady=10)

    word_label = ttk.Label(root, text="", font=("Segoe UI", 32))
    word_label.pack(pady=20)

    start_button = ttk.Button(root, text="Start Test", command=lambda: start_stroop_test())
    start_button.pack(pady=10)

    def display_word():
        """Display a word with a color."""
        if test_data["current_phase"] == 0:
            word = random.choice(colors)
            color = text_colors[word]
        else:
            word = random.choice(colors)
            mismatched = [c for c in text_colors.values() if c != text_colors[word]]
            color = random.choice(mismatched)

        word_label.config(text=word, foreground=color)
        test_data["current_word"] = word
        test_data["current_color"] = color
        correct_colors.append(color)

    def start_stroop_test():
        """Start or restart the test."""
        test_data["score"] = 0
        test_data["total_attempts"] = 0
        test_data["start_time"] = time.time()
        correct_colors.clear()
        selected_colors.clear()

        test_data["current_phase"] = 0
        instructions.config(text="Phase 1: Word and color MATCH.")
        start_button.config(text="Next Phase", command=lambda: switch_phase())

        display_word()

    def switch_phase():
        if test_data["current_phase"] == 0:
            test_data["current_phase"] = 1
            instructions.config(text="Phase 2: Word and color DIFFER.")
            display_word()
        else:
            root.after(500, root.destroy)  # End test after slight delay

    def on_key_press(event):
        if test_data["current_phase"] < 2:
            key = event.char.lower()
            if key in color_keys:
                test_data["total_attempts"] += 1
                selected_color = color_keys[key]
                selected_colors.append(selected_color)
                if selected_color == test_data["current_color"]:
                    test_data["score"] += 1
                display_word()

    root.bind("<KeyPress>", on_key_press)

    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()

    # After GUI closes — results
    accuracy = (test_data["score"] / test_data["total_attempts"]) * 100 if test_data["total_attempts"] > 0 else 0
    score = calculate_score(accuracy)
    duration = time.time() - test_data["start_time"]

    print("\n=== STROOP TEST SUMMARY ===")
    print(f"Correct text colors: {' '.join(correct_colors)}")
    print(f"Participant responses: {' '.join(selected_colors)}")
    print(f"Score: {test_data['score']} / {test_data['total_attempts']}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Time Taken: {duration:.2f} seconds")
    print(f"Clinician Score (0–4): {score}")

    with open("New Exam Code/stroop_results.txt", "a") as f:
        f.write("=== STROOP TEST SUMMARY ===\n")
        f.write(f"Correct text colors: {' '.join(correct_colors)}\n")
        f.write(f"Participant responses: {' '.join(selected_colors)}\n")
        f.write(f"Score: {test_data['score']} / {test_data['total_attempts']}\n")
        f.write(f"Accuracy: {accuracy:.2f}%\n")
        f.write(f"Time Taken: {duration:.2f} seconds\n")
        f.write(f"Clinician Score (0–4): {score}\n\n")

# Run the test
stroop_test()


def wait_for_start(test_number):
    start_input = input(f"Type 'Start test {test_number}' to begin: ")
    while start_input.strip().lower() != f"start test {test_number}":
        print("Incorrect input. Try again.")
        start_input = input(f"Type 'Start test {test_number}' to begin: ")

def calculate_score(is_correct):
    return 0 if is_correct else 4



def odd_one_out_test():
    wait_for_start(3)
    # GUI setup
    root = tk.Tk()
    root.title("Odd One Out Test")
    root.configure(bg="#f5f5f5")

    style = ttk.Style()
    style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 14))

    # Load images
    image_paths = [
        "New Exam Code/test_1.jpg",
        "New Exam Code/test_2.png",  # This is the odd one
        "New Exam Code/test_3.png",
        "New Exam Code/test_4.png"
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

        with open("New Exam Code/odd_one_out_results.txt", "a") as f:
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
        
def wait_for_start(test_number):
    start_input = input(f"Type 'Start test {test_number}' to begin: ")
    while start_input.strip().lower() != f"start test {test_number}":
        print("Incorrect input. Try again.")
        start_input = input(f"Type 'Start test {test_number}' to begin: ")

def calculate_score(accuracy):
    if accuracy >= 90:
        return 0
    elif accuracy >= 80:
        return 1
    elif accuracy >= 60:
        return 2
    elif accuracy >= 40:
        return 3
    else:
        return 4

def action_fluency_test():
    wait_for_start(4)

    # Word setup
    action_words = ["run", "jump", "eat", "swim", "read", "write", "dance", "sing", "climb", "kick", 
                    "throw", "laugh", "cry", "hop", "shout"]
    distractor_words = ["chair", "table", "tooth", "cloud", "pencil", "shoe", "tree", "lamp", 
                        "pillow", "bottle", "bicycle", "bird", "phone", "clock", "window"]
    all_words = action_words + random.sample(distractor_words, 10)
    random.shuffle(all_words)

    selected_actions = []
    correct_selections = 0
    incorrect_selections = 0
    end_time = None  # ✅ Properly declared here

    root = tk.Tk()
    root.title("Action Fluency Test")
    root.configure(bg="#f5f5f5")

    style = ttk.Style()
    style.configure("TButton", font=("Segoe UI", 14), padding=6)
    style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 14))

    ttk.Label(root, text="Select as many ACTION words (verbs) as possible in 25 seconds!",
              wraplength=550).pack(pady=10)

    button_frame = ttk.Frame(root)
    button_frame.pack()

    timer_label = ttk.Label(root, text="Time Left: 25s")
    timer_label.pack(pady=5)

    start_time = time.time()

    def select_action(word, button):
        nonlocal correct_selections, incorrect_selections
        if word not in selected_actions:
            selected_actions.append(word)
            button.state(["disabled"])
            if word in action_words:
                correct_selections += 1
            else:
                incorrect_selections += 1

    def end_test():
        nonlocal end_time
        end_time = time.time()
        root.destroy()

    def update_timer():
        time_left = 25 - int(time.time() - start_time)
        if time_left > 0:
            timer_label.config(text=f"Time Left: {time_left}s")
            root.after(1000, update_timer)
        else:
            end_test()

    # Row/column labels
    for i in range(5):
        ttk.Label(button_frame, text=str(i+1)).grid(row=i+1, column=0, padx=5)
    for j in range(5):
        ttk.Label(button_frame, text=str(j+1)).grid(row=0, column=j+1, pady=5)

    buttons = []
    for i in range(5):
        for j in range(5):
            word = all_words[i * 5 + j]
            button = ttk.Button(button_frame, text=word, width=12,
                                command=lambda w=word, b=None: select_action(w, b))
            button.grid(row=i + 1, column=j + 1, padx=5, pady=5)
            buttons.append(button)
            buttons[-1].config(command=lambda w=word, b=buttons[-1]: select_action(w, b))

    # Center GUI
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    update_timer()
    root.mainloop()

    # Post-test output
    total_correct = len(action_words)
    accuracy = (correct_selections / total_correct) * 100
    score = calculate_score(accuracy)
    duration = end_time - start_time

    print("\n=== ACTION FLUENCY TEST SUMMARY ===")
    print(f"Selected words: {' '.join(selected_actions)}")
    print(f"Correct selections: {correct_selections}/{total_correct}")
    print(f"Incorrect selections: {incorrect_selections}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Time Taken: {duration:.2f} seconds")
    print(f"Clinician Score (0–4): {score}")

    with open("New Exam Code/action_fluency_results.txt", "a") as f:
        f.write("=== ACTION FLUENCY TEST SUMMARY ===\n")
        f.write(f"Selected words: {' '.join(selected_actions)}\n")
        f.write(f"Correct selections: {correct_selections}/{total_correct}\n")
        f.write(f"Incorrect selections: {incorrect_selections}\n")
        f.write(f"Accuracy: {accuracy:.2f}%\n")
        f.write(f"Time Taken: {duration:.2f} seconds\n")
        f.write(f"Clinician Score (0–4): {score}\n\n")
action_fluency_test()


# """
# Test-Specific Quantification Criteria:
# 1. Recall Test:
# 0: Correct sequence, perfect accuracy (100%).

# 1: Minor error or hesitation, accuracy ≥ 90%.

# 2: Several mistakes or noticeable hesitation, accuracy ≥ 70%.

# 3: Frequent errors or confusion, accuracy between 40%–69%.

# 4: Severe confusion or inability to sequence correctly, accuracy < 40%.

# 2. Stroop Test:
# Quantification based on accuracy and reaction speed:

# 0: Accurate and quick response (≥ 90% accuracy, rapid response without delay).

# 1: Slight delays or minimal errors (80-89% accuracy).

# 2: Noticeable slowing, moderate accuracy (60-79% accuracy).

# 3: Substantial slowing or frequent errors (40-59% accuracy).

# 4: Severe difficulty, frequent incorrect responses (<40% accuracy).

# 3. Odd One Out Test:
# Evaluation based on the participant’s ability to identify the odd image promptly:

# 0: Immediate correct identification.

# 1: Slight delay, but correct identification within a brief moment.

# 2: Noticeable hesitation, correct on second attempt.

# 3: Incorrect initially, correct after multiple attempts or considerable assistance.

# 4: Unable to identify or incorrect despite multiple attempts.

# 4. Action Fluency Test:
# Quantification based on selection accuracy and time management during the 25 seconds test:

# 0: High accuracy (≥90%), selections made promptly and confidently.

# 1: Slight delay or minor incorrect selections, overall accuracy between 80-89%.

# 2: Noticeable delays, several incorrect selections, accuracy between 60-79%.

# 3: Difficulty managing time, many incorrect choices, accuracy between 40-59%.

# 4: Severe difficulty, minimal correct selections, accuracy below 40%.

# Implementation:
# After each test, scores from 0 to 4 will be assigned based on the above criteria. The scores can then be summed for an overall cognitive performance score, allowing for comparison and tracking over time. This quantification method ensures clarity, consistency, and alignment with established clinical evaluation standards such as those provided by the MDS-UPDRS.


