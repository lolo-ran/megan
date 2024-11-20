import numpy as np
#Leaving this segment for when we want to import new scode spaces

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
    return R_L_movements