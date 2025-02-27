import tkinter as tk
import time
import random
import tkinter as tk
import random



def action_fluency_test():
    """
    A cognitive test for action fluency where the subject selects as many single-word actions (verbs) as possible in 25 seconds.
    Some words are distractors (not verbs). Now includes row and column numbers (1-5).
    """

    # List of possible words (both verbs and non-verbs)
    action_words = ["run", "jump", "eat", "swim", "read", "write", "dance", "sing", "climb", "kick", 
                    "throw", "laugh", "cry", "hop", "shout"]
    distractor_words = ["chair", "table", "tooth", "cloud", "pencil", "shoe", "tree", "lamp", 
                        "pillow", "bottle", "bicycle", "bird", "phone", "clock", "window"]

    # Mix the action words with some distractors
    all_words = action_words + random.sample(distractor_words, 10)  # Ensure 25 total words
    random.shuffle(all_words)  # Shuffle the list

    # GUI Setup
    root = tk.Tk()
    root.title("Action Fluency Test")
    root.geometry("650x550")

    # Instructions
    instructions = tk.Label(root, text="Select as many ACTION words (verbs) as possible in 25 seconds!", 
                            font=("Times New Roman", 16), wraplength=600)
    instructions.pack(pady=10)

    # Frame for word buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Timer Label
    timer_label = tk.Label(root, text="Time Left: 25s", font=("Times New Roman", 14))
    timer_label.pack(pady=5)

    # Feedback Label
    feedback_label = tk.Label(root, text="", font=("Times New Roman", 14))
    feedback_label.pack(pady=10)

    # Selected actions list
    selected_actions = []
    correct_selections = 0
    incorrect_selections = 0
    start_time = time.time()

    def update_timer():
        """
        Updates the timer and ends the test when time runs out.
        """
        time_left = 25 - int(time.time() - start_time)
        if time_left > 0:
            timer_label.config(text=f"Time Left: {time_left}s")
            root.after(1000, update_timer)  # Update every second
        else:
            end_test()

    def select_action(word, button):
        """
        Handles the selection of words.
        """
        nonlocal correct_selections, incorrect_selections

        if word not in selected_actions:
            selected_actions.append(word)
            button.config(state=tk.DISABLED)  # Disable button after selection

            if word in action_words:
                correct_selections += 1
            else:
                incorrect_selections += 1

    def end_test():
        """
        Ends the test and shows the results.
        """
        accuracy = (correct_selections / len(action_words)) * 100

        result_message = (f"Test Over!\nYou selected {len(selected_actions)} words.\n"
                          f"Correct actions: {correct_selections}/{len(action_words)}\n"
                          f"Incorrect selections: {incorrect_selections}\n"
                          f"Accuracy: {accuracy:.2f}%")

        feedback_label.config(text=result_message, fg="blue")
        
        # Disable all buttons
        for button in buttons:
            button.config(state=tk.DISABLED)

    # Create labels for row and column numbers
    for i in range(5):  # Row numbers
        row_label = tk.Label(button_frame, text=str(i + 1), font=("Times New Roman", 20))
        row_label.grid(row=i + 1, column=0, padx=5, pady=5)  # Shift down by 1 to avoid overlap

    for j in range(5):  # Column numbers
        col_label = tk.Label(button_frame, text=str(j + 1), font=("Times New Roman", 20))
        col_label.grid(row=0, column=j + 1, padx=5, pady=5)  # Shift right by 1 to avoid overlap

    # Create buttons for available words in a 5x5 matrix
    buttons = []
    for i in range(5):  # Rows
        for j in range(5):  # Columns
            word = all_words[i * 5 + j]  # Get the word at index
            button = tk.Button(button_frame, text=word, font=("Times New Roman", 25),
                               width=10, height=2,
                               command=lambda w=word, btn=None: select_action(w, btn))
            button.grid(row=i + 1, column=j + 1, padx=5, pady=5)  # Offset by 1 to fit row/col numbers
            buttons.append(button)
            buttons[-1].config(command=lambda w=word, btn=buttons[-1]: select_action(w, btn))

    # Start the timer
    update_timer()

    # Run the GUI application
    root.mainloop()

# Run the test
action_fluency_test()
