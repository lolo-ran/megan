import numpy as np
import random
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
