import tkinter as tk
import random

def recall_test():
    """
    A recall test where a patient is shown a 1x8 matrix of jumbled letters and numbers.
    The patient must select them in ascending order.
    """

    # Generate 4 random letters and 4 random numbers
    letters = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 4)  
    numbers = random.sample(range(10), 4)  
    jumbled = letters + list(map(str, numbers))
    random.shuffle(jumbled)  # Shuffle to create a mixed sequence

    # Create the correct order
    correct_order = sorted(jumbled, key=lambda x: (x.isdigit(), x.upper()))

    # Tkinter GUI setup
    root = tk.Tk()
    root.title("Recall Test")

    # Instructions
    instructions = tk.Label(root, text="Select the characters in ascending order.", font=("Helvetica", 14))
    instructions.pack(pady=10)

    # Frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    selected_order = []  # Stores the patient's selection
    selected_buttons = []  # Tracks the clicked buttons to disable them after selection

    # Function to handle button click
    def select_item(item, button):
        selected_order.append(item)
        selected_buttons.append(button)
        button.config(state="disabled")  # Disable button after selection
        
        # When 8 items are selected, check accuracy
        if len(selected_order) == 8:
            check_result()

    # Create buttons for the jumbled items
    buttons = []
    for item in jumbled:
        btn = tk.Button(button_frame, text=item, font=("Helvetica", 16), width=4,
                        command=lambda item=item, btn=btn: select_item(item, btn))
        btn.pack(side=tk.LEFT, padx=5)
        buttons.append(btn)

    # Feedback label
    feedback_label = tk.Label(root, text="", font=("Helvetica", 12))
    feedback_label.pack(pady=10)

    # Function to check the patient's response
    def check_result():
        correct_count = sum(1 for i in range(8) if selected_order[i] == correct_order[i])
        accuracy = (correct_count / 8) * 100

        if selected_order == correct_order:
            feedback_label.config(text="Correct! Great job!", fg="green")
        else:
            feedback_label.config(text=f"Incorrect! The correct order is: {' '.join(correct_order)}\n"
                                       f"Your accuracy: {accuracy:.2f}% ({correct_count}/8 correct)", fg="red")

    root.mainloop()

# Run the test
recall_test()
