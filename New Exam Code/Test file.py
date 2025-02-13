import tkinter as tk
import time
import random

def action_fluency_test():
    """
    A cognitive test for action fluency where the subject selects as many single-word actions (verbs) as possible in 25 seconds.
    Some words are distractors (not verbs).
    """

    # List of possible words (both verbs and non-verbs)
    action_words = ["run", "jump", "eat", "swim", "read", "write", "dance", "sing", "climb", "kick", "throw", "laugh", "cry"]
    distractor_words = ["chair", "table", "tooth", "cloud", "pencil", "shoe", "tree", "lamp", "pillow", "bottle"]

    # Mix the action words with some distractors
    all_words = action_words + random.sample(distractor_words, 5)  # Add 5 random distractors
    random.shuffle(all_words)  # Shuffle the list

    # GUI Setup
    root = tk.Tk()
    root.title("Action Fluency Test")
    root.geometry("450x350")

    # Instructions
    instructions = tk.Label(root, text="Select as many ACTION words (verbs) as possible in 25 seconds!", 
                            font=("Helvetica", 14), wraplength=400)
    instructions.pack(pady=10)

    # Frame for word buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Timer Label
    timer_label = tk.Label(root, text="Time Left: 25s", font=("Helvetica", 12))
    timer_label.pack(pady=5)

    # Feedback Label
    feedback_label = tk.Label(root, text="", font=("Helvetica", 12))
    feedback_label.pack(pady=5)

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

    # Create buttons for available words
    buttons = []
    for word in all_words:
        button = tk.Button(button_frame, text=word, font=("Helvetica", 12),
                           command=lambda w=word, btn=None: select_action(w, btn))
        button.pack(side=tk.LEFT, padx=5, pady=5)
        buttons.append(button)
        buttons[-1].config(command=lambda w=word, btn=buttons[-1]: select_action(w, btn))

    # Start the timer
    update_timer()

    # Run the GUI application
    root.mainloop()

# Run the test
action_fluency_test()
