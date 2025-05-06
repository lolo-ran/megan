import tkinter as tk
from tkinter import ttk
import random
import time

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

    with open("action_fluency_results.txt", "a") as f:
        f.write("=== ACTION FLUENCY TEST SUMMARY ===\n")
        f.write(f"Selected words: {' '.join(selected_actions)}\n")
        f.write(f"Correct selections: {correct_selections}/{total_correct}\n")
        f.write(f"Incorrect selections: {incorrect_selections}\n")
        f.write(f"Accuracy: {accuracy:.2f}%\n")
        f.write(f"Time Taken: {duration:.2f} seconds\n")
        f.write(f"Clinician Score (0–4): {score}\n\n")
action_fluency_test()
