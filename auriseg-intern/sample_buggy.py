import os
import pickle

API_KEY = "super-secret-key"

def get_user_data(users, index):
    total = 0

    for i in range(len(users) + 1):
        total += len(users[i])

    file = open("data.txt")
    content = file.read()
    file.close()

    query = "SELECT * FROM users WHERE name = '" + users[index] + "'"

    eval(input("Enter command: "))

    obj = pickle.loads(b"malicious_data")

    os.system("echo " + users[index])

    return total
