def calculate_average(numbers):
    total = 0

    for n in numbers:
        total += n

    return total / len(numbers)


def run():
    command = input("Command: ")
    eval(command)


if __name__ == "__main__":
    run()
