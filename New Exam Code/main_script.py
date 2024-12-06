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
    A recall test where a patient is shown a jumbled up sequence of letters and numbers.
    the patient must reorder them in ascending order.
    """

    # Generate a random sequence of letters and numbers 
    letters = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 5) # Will pick 5 random letter
    numbers = random.sample(range(10), 3) #3 random numbers
    jumbled = letters + list(map(str, numbers))
    random.shuffle(jumbled)

    print("\n-- Recall Test--")
    print("Arrange the following characters in ascending order:")
    print("Jumbled sequence:", " ".join(jumbled))

    # Patient inputs their answer
    patient_input = input("\nEnter your answer (separate items with spaces): ")#.strip()
    patient_order = patient_input.split()
    
    #Create the correct answer
    correct_order = sorted(jumbled, key=lambda x: (x.isdigit(), x.upper()))

    # Create the correct answer
    total_items = len(correct_order)
    correct_count = sum(1 for i, item in enumerate(patient_order) if i < total_items and item == correct_order[i])
    accuracy = (correct_count / total_items) * 100

    # Check the patient's response
    if patient_order == correct_order:
        print("\nCorrect! Great job!")
    else:
        print("\nIncorrect. The correct order is:", " ".join(correct_order))
    print(f"Your accuracy: {accuracy:.2f}% ({correct_count}/{total_items} items correct)")

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


# def odd_one_out_test():
#     """
#     #A test where the subject selects the odd one out of a set of images
#     """
#     #setting up root window
#     root = tk.Tk()
#     root.title("Odd One Out Test")

#     #Load images (Four different images in the same folder as the script)
#     image_paths = []
#     images = [Image.open(path).resize((100,100)) for path in image_paths]
#     photo_images = [ImageTk.PhotoImage(img) for img in images]

#     #Randomize the positions of images 
#     odd_one_index = random.randit(0, 3)
#     randomized_indices = list(range(4))
#     random.shuffle(randomized_indices)

#     #Create a frame to hold images
#     frame = tk.Frame(root)
#     frame.pack(pady=20)

#     #Function to handle the image click
#     def on_image_click(index):
#         if index == randomized_indices[odd_one_index]:

#             messagebox.showinfo("Result","Correct! You found the odd one out")
#         else:
#             messagebox.info("Result", "Incorrect. Try again")
#         root.destroy()  # Close the test after the choice

#      # Display the images in a grid
#     for i, idx in enumerate(randomized_indices):
#         button = tk.Button(
#             frame,
#             image=photo_images[idx],
#             command=lambda index=i: on_image_click(index)
#         )
#         button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

#     # Add instructions
#     instructions = tk.Label(root, text="Click on the odd one out!", font=("Helvetica", 16))
#     instructions.pack(pady=10)

#     # Run the application
#     root.mainloop()
# # Run the test
# odd_one_out_test()

def action_fluency_test():
    """
    A cognitive test for action fluency where the subject names as many single-word actions as possible in 60 seconds.
    """

    print("\n--- Action Fluency Test ---")
    print("You will have 60 seconds to name as many single-word actions (verbs) as possible.")
    print("Example: run, jump, eat, etc.")
    input("\nPress Enter to start...")

    # Start the test
    start_time = time.time()
    responses = []

    print("\nStart naming actions! Type each one and press Enter:")
    
    while time.time() - start_time < 25:  # 60 seconds timer, but putting 25 to not waste time in testing
        action = input("Action: ").strip().lower()  # Capture the action
        if action:  # Only record non-empty inputs
            responses.append(action)

    # End the test
    print("\nTime's up!")
    print(f"\nYou named {len(responses)} actions in 60 seconds.")
    
    # Remove duplicates and display unique actions
    unique_responses = set(responses)
    print(f"\nUnique actions ({len(unique_responses)}): {', '.join(unique_responses)}")
    
    # Optional: Count duplicates
    duplicate_count = len(responses) - len(unique_responses)
    if duplicate_count > 0:
        print(f"Duplicate entries: {duplicate_count}")

# Run the test
action_fluency_test()

