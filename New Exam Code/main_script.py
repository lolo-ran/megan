import numpy as np
import random
import tkinter as tk
import time
#Leaving this segment for when we want to import new code spaces

def co_movements():
    """
    Defines a set of coordinated movements for patients to perform. 
    Each movement includes a name and a simple descriptiom
    """
    R_L_movements = [
        {
            "name" : "Riase",
            "description": "Raise yopur hand and tap your nose"
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

