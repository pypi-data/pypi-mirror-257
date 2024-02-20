import time
import colorama

class Animation:
    def __init__(self):
        pass

    def animate(self):
        text = "Hello, World!"

        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.1)  # Adjust the delay as needed
