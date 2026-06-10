import sys

def calculate_factorial(n):
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n-1)

def PrintMessage(msg):
    print(f"Message: {msg}")

print(calculate_factorial(5))
