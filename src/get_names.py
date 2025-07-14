import os
import random

def get_name():
    """
    Get the name of the game from the environment variable or default to 'Fighter'.
    """
    with open(os.path.join(os.path.dirname(__file__), 'assets', 'name.txt'), 'r') as file:
        lines = file.readlines()
        if lines:
            return lines[random.randint(0, len(lines) - 1)].strip()
        else:
            return 'TestName123'

if __name__ == "__main__":
    print(get_name())