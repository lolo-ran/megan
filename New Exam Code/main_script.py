import numpy as np
import random
import tkinter as tk
import time
from tkinter import messagebox
from PIL import Image, ImageTk
#Leaving this segment for when we want to import new code spaces

def co_movements():
    """
    Defines a set of coordinated movements for patients to perform. 
    Each movement includes a name and a simple descriptiom
    """
    R_L_movements = [
        {
            "name" : "Raise",
            "description": "Raise your hand and tap your nose"
        },
        {
            "name" : "lift",
            "description": "Raise your hand and tap your head"
        },
        {
            "name" : "circle",
            "description": "circle then midline"
        }

    ]
    print("Please perform the following movements:")
    for idx, R_L_movements in enumerate(R_L_movements, start=1):
        print(f"\nMovement {idx}: {R_L_movements['name']}")
        print(f"Description: {R_L_movements['description']}")
    
    Bilateral_movements = [
        {
            "name" : "Clock Creation",
            "description": "Using your hands.."
        },
        {
            "name" : "Clock Replication",
            "description": "Replicate the time ....pm"
        },
        {
            "name" : "Taichi",
            "description": "Certain form"
        },
        {
            "name" : "Tap Nose",
            "description": "Raise both hands and tap your nose"
        }
        
    ]
    return R_L_movements


#Cognitive Exam 
def recall_test():
    """
    A recall test where a patient is shown a jumbled-up sequence of letters and numbers.
    The patient must reorder them in ascending order by selecting them.
    """

    # Generate a random sequence of letters and numbers 
    letters = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 5)  # 5 random letters
    numbers = random.sample(range(10), 3)  # 3 random numbers
    jumbled = letters + list(map(str, numbers))
    random.shuffle(jumbled)  # Shuffle to create randomness

    # Correct order
    correct_order = sorted(jumbled, key=lambda x: (x.isdigit(), x.upper()))
    
    # GUI Setup
    root = tk.Tk()
    root.title("Recall Test")

    # Instructions
    instructions = tk.Label(root, text="Select the characters in ascending order.", font=("Helvetica", 14))
    instructions.pack(pady=10)

    # Frame to display buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Patient selection list
    selected_order = []

    # Feedback Label
    feedback_label = tk.Label(root, text="", font=("Helvetica", 12))
    feedback_label.pack(pady=10)

    def select_item(item, button):
        """
        Handles selection of items and disables buttons after selection.
        """
        if item not in selected_order and len(selected_order) < len(correct_order):
            selected_order.append(item)
            button.config(state=tk.DISABLED)  # Disable the button after selection

            # If all selections are made, check correctness
            if len(selected_order) == len(correct_order):
                check_result()

    def check_result():
        """
        Checks the selected order against the correct order and gives feedback.
        """
        correct_count = sum(1 for i, item in enumerate(selected_order) if item == correct_order[i])
        accuracy = (correct_count / len(correct_order)) * 100

        if selected_order == correct_order:
            feedback_label.config(text=f"Correct! Accuracy: {accuracy:.2f}%", fg="green")
        else:
            feedback_label.config(text=f"Incorrect. The correct order is: {' '.join(correct_order)}\n"
                                       f"Your accuracy: {accuracy:.2f}% ({correct_count}/{len(correct_order)} correct)",
                                  fg="red")

    # Create buttons for the jumbled characters
    buttons = []
    for item in jumbled:
        button = tk.Button(button_frame, text=item, font=("Helvetica", 14),
                           command=lambda item=item, button=None: select_item(item, button))
        button.pack(side=tk.LEFT, padx=5, pady=5)
        buttons.append(button)
        buttons[-1].config(command=lambda item=item, button=buttons[-1]: select_item(item, button))

    # Run the GUI application
    root.mainloop()

# Run the test
recall_test()


def stroop_test():
    """
    A stroop test where the subject/patient is asked to sat the color of the text, not the word itself.
    Initial test will have the color and text match, moves onto a mismatched vesion.
    """

    #Setting up root window
    root = tk.Tk()
    root.title("Stroop Test")

    #Define the colors and words
    colors = ["RED", "BLUE", "GREEN", "BROWN"]
    text_colors = {"GREEN":"green", "RED": "red", "BLUE": "blue", "BROWN": "brown"}

    # Create a label to display instructions
    instructions = tk.Label(root, text="Say the COLOR of the text, not the word!", font=("Helvetica", 16))
    instructions.pack(pady=10)

    # Create a label to display the text
    word_label = tk.Label(root, text="", font=("Helvetica", 32))
    word_label.pack(pady=20)

    # Create a start button
    start_button = tk.Button(root, text="Start Test", font=("Helvetica", 14), command=lambda: start_stroop_test())
    start_button.pack(pady=10)

    # Test state
    test_data = {
        "current_phase": 0,  # 0 = matching, 1 = mismatching
        "current_word": "",
        "current_color": "",
        "score": 0,
        "total_attempts": 0,
        "start_time": None
    }

    def display_word():
        """Display a word with a specific text color."""
        # Randomly select a word and a color
        if test_data["current_phase"] == 0:  # Matching phase
            word = random.choice(colors)
            color = text_colors[word]
        else:  # Mismatching phase
            word = random.choice(colors)
            color = random.choice([c for c in text_colors.values() if c != text_colors[word]])

        # Update the word label
        word_label.config(text=word, fg=color)

        # Save the current word and color for validation
        test_data["current_word"] = word
        test_data["current_color"] = color

    def start_stroop_test():
        """Start the Stroop test."""
        # Reset test state
        test_data["score"] = 0
        test_data["total_attempts"] = 0
        test_data["start_time"] = time.time()

        # Move to the matching phase
        test_data["current_phase"] = 0

        # Update the start button to switch phases
        start_button.config(text="Next Phase", command=lambda: switch_phase())

        # Display the first word
        display_word()

    def switch_phase():
        """Switch between matching and mismatching phases."""
        if test_data["current_phase"] == 0:
            test_data["current_phase"] = 1
            instructions.config(text="Now say the COLOR of the text, not the word!")
            display_word()
        else:
            # End the test and display results
            end_time = time.time()
            duration = end_time - test_data["start_time"]
            accuracy = (test_data["score"] / test_data["total_attempts"]) * 100 if test_data["total_attempts"] > 0 else 0
            result_message = f"Test Complete!\nScore: {test_data['score']} / {test_data['total_attempts']}\nAccuracy: {accuracy:.2f}%\nTime Taken: {duration:.2f} seconds"
            instructions.config(text=result_message)
            start_button.config(text="Restart Test", command=lambda: start_stroop_test())
            word_label.config(text="")

    # Bind key press events for responses
    def on_key_press(event):
        """Handle key presses to validate the user's input."""
        if test_data["current_phase"] < 2:
            # Match the color of the text to the user's response
            key = event.char.lower()
            color_keys = {"g": "green", "r": "red", "b": "blue", "n": "brown"}
            if key in color_keys:
                test_data["total_attempts"] += 1
                if color_keys[key] == test_data["current_color"]:
                    test_data["score"] += 1
                display_word()

    # Bind the key press event to the root window
    root.bind("<KeyPress>", on_key_press)

    # Run the application
    root.mainloop()

# Run the Stroop test
stroop_test()


def odd_one_out_test():
    """
    #A test where the subject selects the odd one out of a set of images
    """
    #setting up root window
    root = tk.Tk()
    root.title("Odd One Out Test")

    #Load images (Four different images in the same folder as the script)
    image_paths = [
    "test_1.jpg",
    "test_2.png",
    "test_3.png",
    "test_4.png"
]
    # image_paths = ["Test images"]
    images = [Image.open(path).resize((100,100)) for path in image_paths]
    photo_images = [ImageTk.PhotoImage(img) for img in images]

    #Randomize the positions of images 
    odd_one_index = random.randint(0, 3)
    randomized_indices = list(range(4))
    random.shuffle(randomized_indices)

    #Create a frame to hold images
    frame = tk.Frame(root)
    frame.pack(pady=20)

    #Function to handle the image click
    def on_image_click(index):
        if index == randomized_indices[odd_one_index]:

            messagebox.showinfo("Result","Correct! You found the odd one out")
        else:
            messagebox.info("Result", "Incorrect. Try again")
        root.destroy()  # Close the test after the choice

     # Display the images in a grid
    for i, idx in enumerate(randomized_indices):
        button = tk.Button(
            frame,
            image=photo_images[idx],
            command=lambda index=i: on_image_click(index)
        )
        button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

    # Add instructions
    instructions = tk.Label(root, text="Click on the odd one out!", font=("Helvetica", 16))
    instructions.pack(pady=10)

    # Run the application
    root.mainloop()
# Run the test
odd_one_out_test()

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
