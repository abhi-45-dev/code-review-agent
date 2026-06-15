import sqlite3


def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = (
        "SELECT * FROM users "
        "WHERE username='"
        + username
        + "' AND password='"
        + password
        + "'"
    )

    cursor.execute(query)

    return cursor.fetchone()


if __name__ == "__main__":
    user = input("Username: ")
    pwd = input("Password: ")

    print(login(user, pwd))
