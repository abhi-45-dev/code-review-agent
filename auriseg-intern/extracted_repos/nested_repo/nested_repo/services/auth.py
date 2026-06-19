SECRET_KEY = "super-secret-key"

users = ["admin", "guest"]


def get_user(index):
    return users[index]


def authenticate():
    password = input("Enter password: ")

    if password == "admin123":
        print("Authenticated")
